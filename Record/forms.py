from django import forms
from .models import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms
from .models import Payment
from django import forms


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
        widgets = {
            'date_paid': forms.DateInput(attrs={'type': 'date'}),
        }

class tenants_databaseForm(forms.ModelForm):
    class Meta:
        model = tenants_database
        fields = '__all__'  # You can specify fields explicitly if needed
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }



class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    identification_number = forms.CharField(max_length=20)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        identification_number = cleaned_data.get('identification_number')

        if username and identification_number:
            try:
                staff = tenants_database.objects.get(username=username, identification_number=identification_number)
            except tenants_database.DoesNotExist:
                raise ValidationError('The provided username (Surname) and ID dont match.')

        return cleaned_data


class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = '__all__'  # or specify fields you want to update




class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['description']


class ResponseForm(forms.Form):
    response = forms.CharField(label='Your Response', widget=forms.Textarea)


class TenatForm(ModelForm):
    class Meta:
        model = Tenant
        fields = '__all__'
     
class TenatRegisterDatabaseForm(ModelForm):
    class Meta:
        model = tenants_database
        fields = '__all__'
     

class HouseForm(ModelForm):
    class Meta:
        model = House
        fields = '__all__'
     