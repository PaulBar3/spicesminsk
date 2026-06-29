from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render


def health_check(request: HttpRequest) -> HttpResponse:
    return JsonResponse({'status': 'ok'})


def handler404(request: HttpRequest, exception: Exception | None = None) -> HttpResponse:
    return render(request, '404.html', status=404)


def handler500(request: HttpRequest) -> HttpResponse:
    return render(request, '500.html', status=500)
