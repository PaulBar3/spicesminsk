import pytest

from catalog.models import Category, Product


@pytest.mark.django_db
class TestCategory:
    def test_create_category(self) -> None:
        cat = Category.objects.create(name='Test', slug='test')
        assert cat.slug == 'test'
        assert str(cat) == 'Test'

    def test_auto_slug(self) -> None:
        cat = Category.objects.create(name='Острая смесь')
        assert cat.slug == 'ostraia-smes'

    def test_unique_slug_collision(self) -> None:
        cat1 = Category.objects.create(name='Ostraya', slug='ostraya')
        cat2 = Category.objects.create(name='Ostraya copy', slug='ostraya')
        assert cat1.slug == 'ostraya'
        assert cat2.slug == 'ostraya-1'

    def test_unique_slug_auto(self) -> None:
        Category.objects.create(name='Ostraya')
        cat2 = Category.objects.create(name='Ostraya')
        assert cat2.slug == 'ostraya-1'

    def test_repr(self) -> None:
        cat = Category.objects.create(name='Test', slug='test')
        assert repr(cat) == f'<Category #{cat.pk}: Test>'

    def test_products_count(self) -> None:
        cat = Category.objects.create(name='Travy', slug='travy')
        assert cat.products.count() == 0
        Product.objects.create(
            category=cat, name='Bazilik',
            price=3.50, slug='bazilik',
        )
        assert cat.products.count() == 1


@pytest.mark.django_db
class TestProduct:
    def test_create_product(self) -> None:
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

    def test_default_in_stock(self) -> None:
        cat = Category.objects.create(name='Specii', slug='specii')
        product = Product.objects.create(
            category=cat, name='Imbir', slug='imbir', price=4.00,
        )
        assert product.in_stock is True

    def test_product_ordering(self) -> None:
        cat = Category.objects.create(name='Specii', slug='specii')
        a = Product.objects.create(
            category=cat, name='Anis', slug='anis', price=5.00,
        )
        b = Product.objects.create(
            category=cat, name='Badyan', slug='badyan', price=6.00,
        )
        assert list(Product.objects.all()) == [a, b]

    def test_unique_slug_collision(self) -> None:
        cat = Category.objects.create(name='Specii', slug='specii')
        p1 = Product.objects.create(
            category=cat, name='Kurkuma', price=5.00, slug='kurkuma',
        )
        p2 = Product.objects.create(
            category=cat, name='Kurkuma', price=6.00, slug='kurkuma',
        )
        assert p1.slug == 'kurkuma'
        assert p2.slug == 'kurkuma-1'

    def test_repr(self) -> None:
        cat = Category.objects.create(name='Specii', slug='specii')
        product = Product.objects.create(
            category=cat, name='Kurkuma', price=5.00, slug='kurkuma',
        )
        assert repr(product) == f'<Product #{product.pk}: Kurkuma>'
