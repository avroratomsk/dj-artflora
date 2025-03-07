from django import forms
from home.models import HomeTemplate
from shop.models import Category,Product

class CallbackForm(forms.Form):
  name = forms.CharField(widget=forms.TextInput(
    attrs={
      'placeholder': 'Ваше имя',
      'class': 'form__controls'
      }
  ))

  phone = forms.CharField(widget=forms.TextInput(
    attrs={
      'placeholder': 'Ваш номер телефона',
      'class': 'form__controls'
      }
  ))
  
class ContactForm(forms.Form):
  name = forms.CharField(widget=forms.TextInput(
    attrs={
      'placeholder': 'Ваше имя',
      'class': 'form__controls'
      }
  ))

  phone = forms.CharField(widget=forms.TextInput(
    attrs={
      'placeholder': 'Ваш номер телефона',
      'class': 'form__controls'
      }
  ))
  
  message = forms.CharField(widget=forms.TextInput(
    attrs={
      'placeholder': 'Ваше сообщение',
      'class': 'form__controls',
      'rows': 15
      }
  ))
