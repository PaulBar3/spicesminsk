from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Category, Product


def index(request):
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

    def get_queryset(self):
        qs = Product.objects.filter(in_stock=True)
        category_slug = self.request.GET.get('category')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.request.GET.get('category')
        context['current_category'] = None
        if category_slug:
            context['current_category'] = get_object_or_404(Category, slug=category_slug)
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = Product.objects.filter(
            category=self.object.category, in_stock=True
        ).exclude(id=self.object.id)[:4]
        return context


def about(request):
    return render(request, 'catalog/about.html')


def contacts(request):
    return render(request, 'catalog/contacts.html')
