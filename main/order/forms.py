from django import forms

from order.models import Order


# class CreateOrderForm(forms.Form):
#   # RESIPIENT_CHOICE = (
#   #   ("myself", "Я сам"),
#   #   ("another-man", "Другой человек"),
#   # )
#   # who_get_bouqets = forms.ChoiceField(widget=forms.RadioSelect, choices=RESIPIENT_CHOICE, required=False)
#   first_name = forms.CharField(required=False)
#   last_name = forms.CharField(required=False)
#   email = forms.CharField(required=False)
#   phone_number = forms.CharField(required=False)
#   first_name_human = forms.CharField(required=False)
#   phone_number_human = forms.CharField(required=False)
#   surprise = forms.CharField(required=False)
#   anonymous = forms.CharField(required=False)
#   delivery_address = forms.CharField(required=False)

class CreateOrderForm(forms.ModelForm):
   class Meta:
      model = Order
      fields = ['first_name', 'phone', 'email', 'delivery_address']