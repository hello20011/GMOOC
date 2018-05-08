from django import forms

from .models import UserProfile

from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={'invalid': '验证码输入错误'})


class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码输入错误'})


class ResetPwdForm(forms.Form):
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)
    password1 = password2


class UserUploadForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UserResetEmailForm(forms.Form):
    email = forms.EmailField(required=True)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'birthday', 'gender', 'address', 'mobile']
