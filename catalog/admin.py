from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'products_count', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('created_at',)

    def products_count(self, obj: Category) -> int:
        return obj.products.count()
    products_count.short_description = 'Товаров'

    fieldsets = [
        ('Основное', {'fields': [('name', 'slug'), 'description']}),
        ('Изображение', {'fields': ['image'], 'classes': ['wide']}),
    ]


class InlineProduct(admin.TabularInline):
    model = Product
    extra = 1
    fields = ('name', 'price', 'weight', 'in_stock')
    show_change_link = True


@admin.action(description='Отметить как "в наличии"')
def mark_in_stock(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet) -> None:
    queryset.update(in_stock=True)


@admin.action(description='Отметить как "нет в наличии"')
def mark_out_of_stock(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet) -> None:
    queryset.update(in_stock=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'category', 'price', 'weight', 'origin', 'in_stock', 'created_at')
    list_display_links = ('name',)
    list_filter = ('category', 'in_stock', 'origin', 'created_at')
    search_fields = ('name', 'description', 'origin')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'in_stock')
    date_hierarchy = 'created_at'
    actions = [mark_in_stock, mark_out_of_stock]
    save_on_top = True

    def image_preview(self, obj: Product) -> str:
        if obj.image:
            return format_html(
                '<img src="{}" style="width:48px;height:48px;object-fit:cover;border-radius:4px;" />',
                obj.image.url,
            )
        return format_html('<span style="color:#999">—</span>')
    image_preview.short_description = 'Фото'

    fieldsets = [
        ('Основное', {
            'fields': [('name', 'slug'), 'category'],
        }),
        ('Описание', {
            'fields': ['description'],
            'classes': ['wide'],
        }),
        ('Цена и вес', {
            'fields': [('price', 'weight'), 'origin'],
        }),
        ('Наличие', {
            'fields': ['in_stock'],
        }),
        ('Изображение', {
            'fields': ['image'],
            'classes': ['wide'],
        }),
    ]
