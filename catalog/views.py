from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Category, Product


def index(request: HttpRequest) -> HttpResponse:
    categories = Category.objects.all()
    products = Product.objects.filter(in_stock=True)[:8]
    return render(request, 'catalog/index.html', {
        'categories': categories,
        'products': products,
    })


class CatalogView(ListView):
    model = Product
    template_name = 'catalog/catalog.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self) -> QuerySet:
        qs = Product.objects.filter(in_stock=True).select_related('category')
        category_slug = self.request.GET.get('category')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        return qs

    def get_context_data(self, **kwargs: object) -> dict[str, object]:
        context = super().get_context_data(**kwargs)
        category_slug = self.request.GET.get('category')
        context['current_category'] = None
        if category_slug:
            context['current_category'] = Category.objects.filter(slug=category_slug).first()
        return context


class CategoryView(ListView):
    model = Product
    template_name = 'catalog/catalog.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self) -> QuerySet:
        return Product.objects.filter(
            category__slug=self.kwargs['slug'], in_stock=True,
        ).select_related('category')

    def get_context_data(self, **kwargs: object) -> dict[str, object]:
        context = super().get_context_data(**kwargs)
        context['current_category'] = Category.objects.filter(slug=self.kwargs['slug']).first()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs: object) -> dict[str, object]:
        context = super().get_context_data(**kwargs)
        context['related_products'] = Product.objects.filter(
            category=self.object.category, in_stock=True,
        ).exclude(id=self.object.id)[:4]
        return context


def about(request: HttpRequest) -> HttpResponse:
    return render(request, 'catalog/about.html')


def contacts(request: HttpRequest) -> HttpResponse:
    return render(request, 'catalog/contacts.html')
