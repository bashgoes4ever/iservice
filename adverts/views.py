from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import *
from django.core.paginator import Paginator
from django.contrib.auth.models import User
import re
import random, string
from .smsc_api import *
from django.contrib.auth import authenticate, login
from django.db.models import Max, Min
from rest_framework.authtoken.models import Token


class Categories(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        objs = Category.objects.all()
        serializer = CategorySerializer(objs, many=True)
        return Response(serializer.data)


class Products(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        objs = Product.objects.all()
        serializer = ProductSerializer(objs, many=True)
        return Response(serializer.data)


class Adverts(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        filters = {}
        # get filters
        if request.GET.get('price__gte'):
            try:
                filters['price__gte'] = int(request.GET.get('price__gte'))
            except:
                pass
        if request.GET.get('price__lte'):
            try:
                filters['price__lte'] = int(request.GET.get('price__lte'))
            except:
                pass
        if request.GET.get('category'):
            try:
                filters['category__name'] = request.GET.get('category')
            except:
                pass
        if request.GET.get('product'):
            try:
                filters['product__name'] = request.GET.get('product')
            except:
                pass

        if filters:
            objs = Advert.objects.filter(**filters, is_active=True, moderated=True, is_deleted=False).order_by('-created')
        else:
            objs = Advert.objects.filter(is_active=True, moderated=True, is_deleted=False).order_by('-created')

        paginator = Paginator(objs, 6)
        page_num = request.GET.get('page', 1)
        objs = paginator.get_page(page_num)
        serializer = AdvertSerializer(objs, many=True)
        page_next = objs.next_page_number() if objs.has_next() else 0
        return Response({
            'data': serializer.data,
            'next_page': page_next
        })

    def post(self, request):
        fields = {}
        fields['category'] = Category.objects.get(name=request.POST.get('current_category'))
        fields['product'] = Product.objects.get(name=request.POST.get('current_product'))
        fields['title'] = request.POST.get('title')
        fields['description'] = request.POST.get('description')
        fields['price'] = request.POST.get('price')
        fields['imei'] = request.POST.get('imei')
        fields['phone'] = request.POST.get('phone')
        fields['user'] = User.objects.get(id=request.POST.get('user_id'))
        advert = Advert(**fields)
        advert.save()
        for i, file in enumerate(request.FILES):
            pos = str(i+1)
            is_main = False if request.POST.get('is_main{}'.format(pos)) == 'false' else True
            image = AdvertImage(product_id=advert.id, image=request.FILES[file], is_main=is_main)
            image.save()
        advert.save()
        return Response({'status': '201'})


class AdvertSingle(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request, id):
        advert = Advert.objects.get(id=id, is_deleted=False)
        serializer = AdvertSerializer(advert, many=False)
        try:
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            user = Token.objects.get(key=token).user
            if user.id == advert.user.id:
                return Response(serializer.data)
        except:
            if advert.moderated is True and advert.is_active is True:
                return Response(serializer.data)
            else:
                return Response({'status': 'error'})


class Register(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        phone = re.sub(r'\D', '', request.POST.get('phone'))
        if len(phone) != 11 or (phone[0] != '7' and phone[0] != '8' and phone[0] != '+'):
            return Response({'error': 'Проверьте правильность ввода номера.', 'code': 2})
        if int(phone[0]) == 8:
            phone = list(phone)
            phone[0] = '7'
            phone = ''.join(phone)
        try:
            user = User.objects.get(username=str(phone))
        except User.DoesNotExist:
            user = None
        if user is None:
            password = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=6))
            user = User.objects.create_user(username=str(phone), password=password)
            smsc = SMSC()
            r = smsc.send_sms(str(phone), "{}".format(password))
            return Response({'registration': 'success', 'code': 0})
        else:
            return Response({'error': 'Пользователь с таким номером телефона уже зарегистрирован.', 'code': 1})


class Login(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        phone = re.sub(r'\D', '', request.POST.get('phone'))
        if len(phone) != 11 or (phone[0] != '7' and phone[0] != '8' and phone[0] != '+'):
            return Response({'error': 'Проверьте правильность ввода номера.', 'code': 2})
        if int(phone[0]) == 8:
            phone = list(phone)
            phone[0] = '7'
            phone = ''.join(phone)
        user = authenticate(username=str(phone), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return Response({'login': 'success', 'code': 0})
        else:
            return Response({'error': 'Неправильный номер телефона или пароль.', 'code': 1})


class GetUser(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = Token.objects.get(key=request.META.get('HTTP_AUTHORIZATION')).user
        print(request.META.get('HTTP_AUTHORIZATION'))
        return Response({'username': ''})


class Prices(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        adverts = Advert.objects.filter(is_deleted=False, is_active=True, moderated=True)
        price_min = adverts.aggregate(Min('price'))['price__min']
        price_max = adverts.aggregate(Max('price'))['price__max']
        return Response({'min': price_min, 'max': price_max})


class Phone(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, id):
        advert = Advert.objects.get(id=id)
        phone = advert.phone
        return Response({'phone': phone})


class UserAdverts(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, id):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        user = Token.objects.get(key=token).user
        if user.id == id:
            adverts = Advert.objects.filter(user__id=id, is_deleted=False).order_by('-created')
            serializer = AdvertSerializer(adverts, many=True)
            return Response({'data': serializer.data, 'status': 'success'})
        else:
            return Response({'status': 'error'})
    def put(self, request, id):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        user = Token.objects.get(key=token).user
        advert = Advert.objects.get(id=id)
        if user.id == advert.user.id:
            fields = {}
            fields['category'] = Category.objects.get(name=request.POST.get('current_category'))
            fields['product'] = Product.objects.get(name=request.POST.get('current_product'))
            fields['title'] = request.POST.get('title')
            fields['description'] = request.POST.get('description')
            fields['price'] = request.POST.get('price')
            fields['imei'] = request.POST.get('imei')
            fields['phone'] = request.POST.get('phone')
            fields['moderated'] = False
            for i in range(0, int(request.POST.get('images_old'))):
                is_delete = False if request.POST.get('old_is_delete{}'.format(i)) == 'false' else True
                if is_delete:
                    AdvertImage.objects.get(id=request.POST.get('old_image{}'.format(i))).delete()
                is_main = False if request.POST.get('old_is_main{}'.format(i)) == 'false' else True
                if not is_delete:
                    image = AdvertImage.objects.get(id=request.POST.get('old_image{}'.format(i)))
                    image.is_main = is_main
                    image.save(update_fields=['is_main'])
            for i, file in enumerate(request.FILES):
                pos = str(i+1)
                is_main = False if request.POST.get('is_main{}'.format(pos)) == 'false' else True
                image = AdvertImage(product_id=advert.id, image=request.FILES[file], is_main=is_main)
                image.save()
            for attr, value in fields.items():
                setattr(advert, attr, value)
            advert.save()
            return Response({'status': 'updated'})
        else:
            return Response({'status': 'error'})



class DeleteAdvert(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, id):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        user = Token.objects.get(key=token).user
        advert = Advert.objects.get(id=id)
        if user.id == advert.user.id:
            advert.is_deleted = True
            advert.save()
            return Response({'status': 'deleted'})
        else:
            return Response({'status': 'error'})




