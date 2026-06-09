import pytest
from django.urls import reverse

from catalog.models import Category, Product


@pytest.mark.django_db
class TestIndexView:
    def test_status_code(self, client):
        response = client.get(reverse('catalog:index'))
        assert response.status_code == 200

    def test_template(self, client):
        response = client.get(reverse('catalog:index'))
        assert 'catalog/index.html' in [t.name for t in response.templates]

    def test_context_categories(self, client):
        cat = Category.objects.create(name='Test', slug='test')
        response = client.get(reverse('catalog:index'))
        assert cat in response.context['categories']

    def test_context_products(self, client):
        cat = Category.objects.create(name='Test', slug='test')
        p = Product.objects.create(
            category=cat, name='Test', slug='test-prod', price=1.00
        )
        response = client.get(reverse('catalog:index'))
        assert p in response.context['products']

    def test_hides_out_of_stock(self, client):
        cat = Category.objects.create(name='Test', slug='test')
        p = Product.objects.create(
            category=cat, name='Net', slug='net',
            price=1.00, in_stock=False
        )
        response = client.get(reverse('catalog:index'))
        assert p not in response.context['products']


@pytest.mark.django_db
class TestCatalogView:
    url = reverse('catalog:catalog')

    def test_status_code(self, client):
        response = client.get(self.url)
        assert response.status_code == 200

    def test_template(self, client):
        response = client.get(self.url)
        assert 'catalog/catalog.html' in [t.name for t in response.templates]

    def test_pagination(self, client):
        cat = Category.objects.create(name='Test', slug='test')
        for i in range(15):
            Product.objects.create(
                category=cat, name=f'Tovar {i}',
                slug=f'tovar-{i}', price=1.00
            )
        response = client.get(self.url)
        assert len(response.context['products']) == 12

    def test_category_filter(self, client):
        cat1 = Category.objects.create(name='A', slug='a')
        cat2 = Category.objects.create(name='B', slug='b')
        p1 = Product.objects.create(
            category=cat1, name='Iz A', slug='iz-a', price=1.00
        )
        Product.objects.create(
            category=cat2, name='Iz B', slug='iz-b', price=1.00
        )
        response = client.get(self.url, {'category': cat1.slug})
        assert list(response.context['products']) == [p1]


@pytest.mark.django_db
class TestProductDetailView:
    def test_status_code(self, client):
        cat = Category.objects.create(name='Test', slug='test')
        product = Product.objects.create(
            category=cat, name='Test', slug='test-prod', price=1.00
        )
        response = client.get(product.get_absolute_url())
        assert response.status_code == 200

    def test_404(self, client):
        response = client.get(
            reverse('catalog:product_detail', kwargs={'slug': 'nonexistent'})
        )
        assert response.status_code == 404

    def test_context(self, client):
        cat = Category.objects.create(name='Test', slug='test')
        product = Product.objects.create(
            category=cat, name='Test', slug='test-prod', price=1.00
        )
        response = client.get(product.get_absolute_url())
        assert response.context['product'] == product


@pytest.mark.django_db
class TestAboutView:
    def test_status_code(self, client):
        response = client.get(reverse('catalog:about'))
        assert response.status_code == 200

    def test_template(self, client):
        response = client.get(reverse('catalog:about'))
        assert 'catalog/about.html' in [t.name for t in response.templates]


@pytest.mark.django_db
class TestContactsView:
    def test_status_code(self, client):
        response = client.get(reverse('catalog:contacts'))
        assert response.status_code == 200

    def test_template(self, client):
        response = client.get(reverse('catalog:contacts'))
        assert 'catalog/contacts.html' in [t.name for t in response.templates]
