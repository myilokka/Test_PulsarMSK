import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from shop.models import Product, Image


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def product_factory():
    def factory(*args, **kwargs):
        return baker.make(Product, *args, **kwargs)
    return factory


@pytest.fixture()
def image_factory():
    def factory(*args, **kwargs):
        return baker.make(Image, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_retrieve_product(client, product_factory):
    product = product_factory()
    url = f'/api/products/{str(product.id)}/'

    response = client.get(url)
    data = response.json()

    assert data['title'] == product.title
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_products(client, product_factory):
    products = product_factory(_quantity=5)
    url = '/api/products/'

    response = client.get(url)
    data = response.json()

    assert len(data) == len(products)
    for k, p in enumerate(products):
        assert p.title == data[k]['title']
    assert response.status_code == 200


@pytest.mark.django_db
def test_product_status_filter(client, product_factory):
    products = product_factory(_quantity=5, status="IN STOCK")
    url = f'/api/products/?status=IN STOCK'

    response = client.get(url)
    data = response.json()
    for k, product in enumerate(products):
        assert data[k]['status'] == product.status
    assert response.status_code == 200


@pytest.mark.django_db
def test_course_title_filter(client, product_factory):
    products = product_factory(_quantity=5)
    url = f'/api/products/?title={str(products[0].title)}'

    response = client.get(url)
    data = response.json()

    assert data[0]['id'] == products[0].id
    assert data[0]['title'] == products[0].title
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_product(client, image_factory):
    url = '/api/products/'
    image = image_factory(id=1)
    body = {"title": "34534",
            "vendor_code": "73453",
            "price": 354,
            "status": "IN STOCK",
            "image": 1}

    response = client.post(url, data=body)
    data = response.json()
    assert data['title'] == '34534'
    assert data['image'] == image
    assert response.status_code == 201


@pytest.mark.django_db
def test_update_product(client, product_factory):
    product = product_factory()
    url = f'/api/products/{str(product.id)}/'
    body = {"title": "course"}

    response = client.patch(url, body)
    data = response.json()
    assert data['title'] == 'course'
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_product(client, product_factory):
    product = product_factory()
    url = f'/api/products/{str(product.id)}/'

    first_response = client.delete(url)
    second_response = client.get(url)

    assert first_response.status_code == 204
    assert second_response.status_code == 404
