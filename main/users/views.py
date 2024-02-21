from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse
from users.forms import UserLoginForm

def login(request):
  
  if request.method == "POST":
    form = UserLoginForm(data=request.POST)
    if form.is_valid:
      username = request.POST["username"]
      password = request.POST["password"]
      user = auth.authenticate(username=username, password=password)
      if user:
        auth.login(request, user)
        return HttpResponseRedirect(reverse("home:index"))
  else:
    form = UserLoginForm()
  
  context = {
    "title": "Страница авторизации",
    "form":form,
  }
  
  return render(request, 'pages/users/login.html', context)

def register(request):
  context = {
    "title": "Страница регистрации",
    
  }
  
  return render(request, 'pages/users/register.html', context)

def profile(request):
  context = {
    "title": "Личный кабинет",
  }
  
  return render(request, 'pages/users/profile.html', context)

def logout(request):
  pass