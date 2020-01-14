from django.contrib import admin
from .models import *


admin.site.register(Category)
admin.site.register(Product)


class AdvertImageInline(admin.TabularInline):
    model = AdvertImage
    extra = 0


class AdvertAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Advert._meta.fields]
    inlines = [AdvertImageInline]

    class Meta:
        model = Advert


admin.site.register(Advert, AdvertAdmin)
