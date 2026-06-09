import pytest
from django.conf import settings
from django.urls import reverse


@pytest.mark.django_db
class TestAdminAccess:
    def test_login_required(self, client):
        response = client.get(reverse('admin:index'))
        assert response.status_code == 302
        assert f'/{settings.ADMIN_URL}/login/' in response.url

    def test_admin_login(self, client, django_user_model):
        django_user_model.objects.create_superuser(
            'admin', 'admin@test.by', 'admin'
        )
        client.login(username='admin', password='admin')
        response = client.get(reverse('admin:index'))
        assert response.status_code == 200


@pytest.mark.django_db
class TestCategoryAdmin:
    def test_category_list(self, client, django_user_model):
        django_user_model.objects.create_superuser(
            'admin', 'admin@test.by', 'admin'
        )
        client.login(username='admin', password='admin')
        response = client.get(
            reverse('admin:catalog_category_changelist')
        )
        assert response.status_code == 200


@pytest.mark.django_db
class TestProductAdmin:
    def test_product_list(self, client, django_user_model):
        django_user_model.objects.create_superuser(
            'admin', 'admin@test.by', 'admin'
        )
        client.login(username='admin', password='admin')
        response = client.get(
            reverse('admin:catalog_product_changelist')
        )
        assert response.status_code == 200
