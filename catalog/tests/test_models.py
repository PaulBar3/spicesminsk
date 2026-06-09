import pytest
from django.db import IntegrityError

from catalog.models import Category, Product


@pytest.mark.django_db
class TestCategory:
    def test_create_category(self):
        cat = Category.objects.create(name='Test', slug='test')
        assert cat.slug == 'test'
        assert str(cat) == 'Test'

    def test_unique_slug(self):
        Category.objects.create(name='Ostraya', slug='ostraya')
        with pytest.raises(IntegrityError):
            Category.objects.create(name='Ostraya copy', slug='ostraya')

    def test_products_count(self):
        cat = Category.objects.create(name='Travy', slug='travy')
        assert cat.products.count() == 0
        Product.objects.create(
            category=cat, name='Bazilik',
            price=3.50, slug='bazilik'
        )
        assert cat.products.count() == 1


@pytest.mark.django_db
class TestProduct:
    def test_create_product(self):
        cat = Category.objects.create(name='Specii', slug='specii')
        product = Product.objects.create(
            category=cat,
            name='Kurkuma',
            slug='kurkuma',
            price=5.00,
            weight='50 g',
            origin='India',
        )
        assert product.slug == 'kurkuma'
        assert product.in_stock is True
        assert str(product) == 'Kurkuma'

    def test_default_in_stock(self):
        cat = Category.objects.create(name='Specii', slug='specii')
        product = Product.objects.create(
            category=cat, name='Imbir', slug='imbir', price=4.00
        )
        assert product.in_stock is True

    def test_product_ordering(self):
        cat = Category.objects.create(name='Specii', slug='specii')
        a = Product.objects.create(
            category=cat, name='Anis', slug='anis', price=5.00
        )
        b = Product.objects.create(
            category=cat, name='Badyan', slug='badyan', price=6.00
        )
        products = list(Product.objects.all())
        assert products == [a, b]
