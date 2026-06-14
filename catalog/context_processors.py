from django.core.cache import cache

from .models import Category


def categories(request):
    cats = cache.get('all_categories')
    if cats is None:
        cats = list(Category.objects.all())
        cache.set('all_categories', cats, 3600)
    return {'all_categories': cats}
