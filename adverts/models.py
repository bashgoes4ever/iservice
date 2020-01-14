from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os


class Category(models.Model):
    name = models.CharField(max_length=128, verbose_name=u"Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"Категория"
        verbose_name_plural = u"Категории"


class Product(models.Model):
    category = models.ForeignKey(Category, blank=False, on_delete=models.CASCADE, verbose_name=u"Категория", related_name='products')
    name = models.CharField(max_length=128, verbose_name=u"Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"Продукт"
        verbose_name_plural = u"Продукты"


class Advert(models.Model):
    category = models.ForeignKey(Category, blank=False, on_delete=models.CASCADE, verbose_name=u"Категория")
    product = models.ForeignKey(Product, blank=False, on_delete=models.CASCADE, verbose_name=u"Продукт")
    title = models.CharField(max_length=64, verbose_name=u"Заголовок")
    description = models.TextField(max_length=512, verbose_name=u"Описание", blank=True)
    price = models.IntegerField(verbose_name=u"Цена")
    phone = models.CharField(max_length=16, verbose_name=u"Телефон")
    imei = models.CharField(max_length=64, verbose_name=u"IMEI или S/N", blank=True)
    is_active = models.BooleanField(verbose_name=u"Активно?", default=True)
    moderated = models.BooleanField(verbose_name=u"Прошло модерацию?", default=False)
    is_deleted = models.BooleanField(verbose_name=u"Удалено пользователем?", default=False)
    created = models.DateTimeField(editable=False, default=now)
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, verbose_name=u"Пользователь")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u"Объявление"
        verbose_name_plural = u"Объявления"

    def save(self, *args, **kwargs):
        images = self.images.all()
        counter = 0
        last_main_img = {}
        for img in images:
            if img.is_main == True:
                counter += 1
                last_main_img = img
        if counter > 1:
            for img in images:
                img.is_main = False
                img.save()
            last_main_img.is_main = True
            last_main_img.save()
        if images and counter == 0:
            images[0].is_main = True
            images[0].save()
        super(Advert, self).save(*args, **kwargs)


class AdvertImage(models.Model):
    product = models.ForeignKey(Advert, blank=False, on_delete=models.CASCADE, verbose_name=u"Фото", related_name='images')
    image = models.ImageField(upload_to='static/img/products/', verbose_name=u"Изображение", blank=True)
    image_thumb = models.ImageField(upload_to='static/img/products/', blank=True, editable=False)
    is_main = models.BooleanField(default=False, verbose_name=u"Главное")

    def save(self, *args, **kwargs):
        if not make_thumbnail(self.image, self.image_thumb):
            raise Exception('Could not create thumbnail - is the file type valid?')
        super(AdvertImage, self).save(*args, **kwargs)


def make_thumbnail(img, thumb):
    if img:
        """
        Create and save the thumbnail for the photo (simple resize with PIL).
        """
        max_width = 370
        max_height = 225

        image = Image.open(img)
        w, h = image.size
        if w > h:
            width = round(max_height/(h/w))
            thumb_size = (width, max_height)
        else:
            height = round(max_width/(w/h))
            thumb_size = (max_width, height)
        image.thumbnail(thumb_size, Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(img.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False    # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        thumb.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

    return True