from django.contrib import admin

from shop.models import Image, Product


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
