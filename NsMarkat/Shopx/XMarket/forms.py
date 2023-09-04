from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserChangeForm , UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('first_name' , 'last_name' , 'email' , 'username' , 'password' , 'dob' , 'is_staff' , 'is_superuser' , 'number' , 'address' , 'gender',)

class Password_Reset_form(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email']
        
class Password_Confirm_form(forms.ModelForm):
    Confirm_Password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ['password']
        widgets = {
            'password' : forms.PasswordInput
        }
        
        
    
