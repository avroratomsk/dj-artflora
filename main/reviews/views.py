from django.http import HttpResponse
from django.shortcuts import render

def reviews(request):
  
  return render(request, "pages/reviews/reviews.html")

def reviews_detail(requset, slug):
  return HttpResponse(f"{slug} - отзыв")
