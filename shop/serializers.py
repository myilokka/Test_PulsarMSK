from rest_framework import serializers

from shop.models import Product, Image


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['id', 'path', 'formats']


class ProductSerializer(serializers.ModelSerializer):

    image = ImageSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'vendor_code', 'price', 'status', "image"]

    def create(self, validated_data):
        validated_data['image'] = Image.objects.get(id=self.initial_data['image'])
        return super().create(validated_data)

