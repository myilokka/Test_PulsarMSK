from PIL import Image as I
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from django.db import models
import uuid


from shop.fields import WEBPField


shop_image_file = 'shop_photos/'


def image_folder(instance, filename):
    name = uuid.uuid4().hex
    return f'{shop_image_file}/{name}.{filename.split(".")[1]}'


def image_folder_webp(instance, filename):
    name = uuid.uuid4().hex
    return f'{shop_image_file}/{name}.webp'


class ProductStatusChoices(models.TextChoices):

    IN_STOCK = "IN STOCK", "В наличии"
    ON_ORDER = "ON_ORDER", "Под заказ"
    EXPECTED_TO_ARRIVE = "EXPECTED TO ARRIVE", "Ожидается поступление"
    NOT_AVAILABLE = "NOT AVAILABLE", "Нет в наличии"
    NOT_PRODUCED = "NOT PRODUCED", "Не производится"


class Image(models.Model):

    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')

    image = models.ImageField(verbose_name=_('image'), upload_to=image_folder, blank=True)
    image_webp = WEBPField(verbose_name=_('image_webp'), upload_to=image_folder_webp)
    path = models.TextField(_('image_path'), max_length=200, default=f"/media/{shop_image_file}")
    formats = ArrayField(verbose_name=_('image_formats'), base_field=models.CharField(max_length=10, blank=True), size=2, default='webp')


class Product(models.Model):

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

        ordering = ['title']

    title = models.CharField(_('title'), max_length=60)
    vendor_code = models.CharField(_('vendor_code'), max_length=20)
    price = models.DecimalField(_('price'), max_digits=12, decimal_places=2)
    status = models.TextField(_('status'),
                              choices=ProductStatusChoices.choices,
                              default=ProductStatusChoices.EXPECTED_TO_ARRIVE)
    image = models.ForeignKey(verbose_name=_('image'), to=Image, on_delete=models.CASCADE, related_name='product', null=True)

    def __str__(self):
        return self.title
