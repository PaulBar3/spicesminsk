from django import template
from django.utils.safestring import mark_safe
from django.templatetags.static import static

register = template.Library()


@register.filter
def byn(value):
    svg_url = static('catalog/img/byn-symbol.svg')
    return mark_safe(
        f'{value} '
        f'<img src="{svg_url}" class="byn-symbol" alt="Br" '
        f'width="14" height="17" loading="lazy">'
    )
