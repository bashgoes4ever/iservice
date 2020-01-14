# coding=utf-8
from django.urls import path
from .views import *


urlpatterns = [
    path('adverts/<str:id>', AdvertSingle.as_view(), name='advert_single'),
    path('phone/<str:id>', Phone.as_view(), name='get_phone'),
    path('user_adverts/<int:id>', UserAdverts.as_view(), name='user_adverts'),
    path('delete_advert/<int:id>', DeleteAdvert.as_view(), name='delete_advert'),
    path('update_advert/<int:id>', UserAdverts.as_view(), name='update_advert'),
    path('categories/', Categories.as_view()),
    path('products/', Products.as_view()),
    path('adverts/', Adverts.as_view()),
    path('register/', Register.as_view()),
    path('login/', Login.as_view()),
    path('get_user/', GetUser.as_view()),
    path('prices/', Prices.as_view()),

]