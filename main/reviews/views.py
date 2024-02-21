from django.http import HttpResponse
from django.shortcuts import render

def reviews(request):
  return HttpResponse("Страница отзывов")

def reviews_detail(requset, slug):
  return HttpResponse(f"{slug} - отзыв")
