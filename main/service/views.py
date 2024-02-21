from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.db.models import Q

from service.models import Service

def service(request):
  services = Service.objects.filter(status=True)
  
  context = {
    "services": services
  }
  return render(request, "pages/service/service.html", context)

def service_detail(request, slug):
  service = Service.objects.get(slug=slug)
  
  context = {
    "service": service
  }
  
  return render(request, "pages/service/service_detail.html", context)