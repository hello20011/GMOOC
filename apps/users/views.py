from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from utils.send_email import send_register_email

from users.forms import LoginForm, RegisterForm, ForgetPwdForm, ResetPwdForm
from users.models import UserProfile, EmailVerifyRecord


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as ret:
            return None


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = UserProfile()
            user.username = request.POST.get('email')
            if UserProfile.objects.filter(email=request.POST.get('email')):
                return render(request, 'register.html', {'msg': '用户已经存在'})
            user.email = request.POST.get('email')
            user.password = make_password(request.POST.get('password'))
            user.save()
            user.is_active = False
            send_status = send_register_email(user.username, 'register')
            if send_status:
                return render(request, 'login.html')
            else:
                return HttpResponse('邮件发送失败')
        else:
            return render(request, 'register.html', {'register_form': register_form})


class VerifyEmailView(View):
    def get(self, request):
        email = request.GET.get('email')
        token = request.GET.get('token')
        all_records = EmailVerifyRecord.objects.filter(code=token)
        if all_records:
            for record in all_records:
                if email == record.email:
                    user = UserProfile.objects.get(email=email)
                    user.is_active = True
            return render(request, 'login.html')
        else:
            return HttpResponse('激活失败')


class ForgetPwdView(View):
    def get(self, request):
        forgetpwd_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forgetpwd_form': forgetpwd_form})

    def post(self, request):
        forgetpwd_form = ForgetPwdForm(request.POST)
        if forgetpwd_form.is_valid():
            email = request.POST.get('email')
            if UserProfile.objects.filter(email=email):
                send_status = send_register_email(email, "forget")
                if send_status:
                    return HttpResponse('密码重置邮件已发送，请查收')
                else:
                    return HttpResponse('邮件发送失败')
            else:
                return render(request, 'forgetpwd.html', {'msg': '该邮箱未注册'})
        else:
            return render(request, 'forgetpwd.html', {'forgetpwd_form': forgetpwd_form})


class ResetPwdView(View):
    def get(self, request):
        email = request.GET.get('email')
        token = request.GET.get('token')
        return render(request, 'password_reset.html', {'email': email, 'token': token})

    def post(self, request):
        resetpwd_form = ResetPwdForm(request.POST)
        if resetpwd_form.is_valid():
            email = request.POST.get('email')
            token = request.POST.get('token')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 != password2:
                return render(request, 'password_reset.html', {'email': email, 'token': token, 'msg': '两次密码输入不一致'})
            if EmailVerifyRecord.objects.get(email=email, code=token):
                user = UserProfile.objects.get(email=email)
                user.password = make_password(password1)
                user.save()
                return render(request, 'login.html')
            else:
                return HttpResponse("重置密码链接有误")
        else:
            return render(request, 'password_reset.html', {'resetpwd_form': resetpwd_form})
