from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode


def _make_slug(text: str) -> str:
    return slugify(unidecode(text))


def _unique_slug(model_class: type[models.Model], base_slug: str, exclude_pk: int | None = None) -> str:
    slug = base_slug
    counter = 1
    while model_class.objects.filter(slug=slug).exclude(pk=exclude_pk).exists():
        slug = f'{base_slug}-{counter}'
        counter += 1
    return slug


class Category(models.Model):
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('URL', max_length=200, unique=True, blank=True)
    description = models.TextField('Описание', blank=True)
    image = models.ImageField('Изображение', upload_to='categories/', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'<Category #{self.pk}: {self.name}>'

    def save(self, *args: object, **kwargs: object) -> None:
        if not self.slug:
            self.slug = _unique_slug(type(self), _make_slug(self.name), self.pk)
        elif type(self).objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            self.slug = _unique_slug(type(self), self.slug, self.pk)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse('catalog:category', kwargs={'slug': self.slug})


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name='products', verbose_name='Категория',
    )
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('URL', max_length=200, unique=True, blank=True)
    description = models.TextField('Описание', blank=True)
    image = models.ImageField('Изображение', upload_to='products/', blank=True, null=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    weight = models.CharField('Вес', max_length=50, blank=True, help_text='например: 50 г, 100 г')
    origin = models.CharField('Страна происхождения', max_length=200, blank=True)
    in_stock = models.BooleanField('В наличии', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'<Product #{self.pk}: {self.name}>'

    def save(self, *args: object, **kwargs: object) -> None:
        if not self.slug:
            self.slug = _unique_slug(type(self), _make_slug(self.name), self.pk)
        elif type(self).objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            self.slug = _unique_slug(type(self), self.slug, self.pk)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse('catalog:product_detail', kwargs={'slug': self.slug})
