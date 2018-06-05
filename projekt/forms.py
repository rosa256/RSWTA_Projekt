from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate, get_user_model, login, logout
from captcha.fields import CaptchaField
from .models import Oferta,Aplikant

from django.core.validators import EmailValidator

class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    captcha = CaptchaField()
    class Meta:
        model = User
        fields = ['username', 'password1','password2','email',]

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class OfertaForm(forms.ModelForm):
    class Meta:
        model = Oferta
        fields = ['branza','lokalizacja','wakat','wynagrodzenie','opis','data_utworzenia']

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class CvForm(forms.ModelForm):
    class Meta:
        model = Aplikant
        fields = ('cv',)

User = get_user_model()
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args,**kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        #user_qs = User.objects.filter(username=username)
        #user = user_qs.first()

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist.")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password.")
            if not user.is_active:
                raise forms.ValidationError("This user is not longer activate.")
        return super(UserLoginForm,self).clean(*args,**kwargs)



