from django import forms

class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    street_address = forms.CharField(max_length=100)
    house_number = forms.CharField(max_length=10)
    postal_code = forms.CharField(max_length=20)
    phone = forms.CharField(max_length=20)
    city = forms.CharField(max_length=20)
    state = forms.CharField(max_length=20)
    country  = forms.CharField(max_length=20)
    emale  = forms.CharField(max_length=20)
    
