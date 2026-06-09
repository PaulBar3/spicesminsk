from django.urls import path

from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.CatalogView.as_view(), name='catalog'),
    path('catalog/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
]
