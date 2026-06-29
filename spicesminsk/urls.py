from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    path(f'{settings.ADMIN_URL}/', admin.site.urls),
    path('', include('catalog.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'spicesminsk.views.handler404'
handler500 = 'spicesminsk.views.handler500'
