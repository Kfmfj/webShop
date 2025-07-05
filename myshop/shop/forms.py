
from django import forms

class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=100, required=True)
    phone = forms.CharField(max_length=20, required=True)
    street_address = forms.CharField(max_length=255, required=True)
    house_number = forms.CharField(max_length=10, required=False)
    postal_code = forms.CharField(max_length=20, required=True)
    city = forms.CharField(max_length=100, required=True)
    state = forms.CharField(max_length=100, required=False)
    country = forms.CharField(max_length=100, required=True)