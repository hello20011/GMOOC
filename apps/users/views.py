import json

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from organization.models import CourseOrg, Teacher
from utils.send_email import send_register_email
from users.forms import LoginForm, RegisterForm, ForgetPwdForm, ResetPwdForm, UserUploadForm, UserResetEmailForm, UserUpdateForm
from users.models import UserProfile, EmailVerifyRecord
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse, UserFavourite, UserMessage
from course.models import Course

from pure_pagination import Paginator, PageNotAnInteger


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


class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter-info.html')

    def post(self, request):
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        if user_update_form.is_valid():
            user_update_form.save()
            return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_update_form.errors), content_type='application/json')


class UserUploadView(LoginRequiredMixin, View):
    def post(self, request):
        user_upload_form = UserUploadForm(request.POST, request.FILES, instance=request.user)
        if user_upload_form.is_valid():
            user_upload_form.save()
            return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'fail'}), content_type='application/json')


class UserResetPwdView(LoginRequiredMixin, View):
    def post(self, request):
        reset_pwd_form = ResetPwdForm(request.POST)
        if reset_pwd_form.is_valid():
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 != password2:
                return HttpResponse(json.dumps({'status': 'fail', 'msg':'两次密码输入不一致'}), content_type='application/json')
            user = request.user
            user.password = make_password(password1)
            user.save()
            return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps(reset_pwd_form.errors), content_type='application/json')


class UserResetEmailCodeView(LoginRequiredMixin, View):
    def post(self, request):
        user_reset_email_form = UserResetEmailForm(request.POST)
        if user_reset_email_form.is_valid():
            email = request.POST.get('email')
            if not UserProfile.objects.filter(email=email):
                if send_register_email(email, 'reset_email'):
                    return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')
                else:
                    return HttpResponse(json.dumps({'status': 'failure'}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'status': 'failure', 'msg': '邮箱已经被注册'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'failure'}), content_type='application/json')


class UserResetEmailCodeVerifyView(LoginRequiredMixin, View):
    def post(self, request):
        email = request.POST.get('email')
        code = request.POST.get('code')
        email_verify_record = EmailVerifyRecord.objects.filter(email=email, code=code)
        if email_verify_record:
            user = request.user
            user.email = email
            user.save()
            email_verify_record.delete()
            return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'fail'}), content_type='application/json')


class UserMyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'user_courses': user_courses,
        })


class UserFavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        all_fav_objs = UserFavourite.objects.filter(user=request.user, fav_type=2)
        fav_org_ids = [all_fav_obj.fav_id for all_fav_obj in all_fav_objs]
        fav_orgs = CourseOrg.objects.filter(pk__in=fav_org_ids)
        return render(request, 'usercenter-fav-org.html', {
            'fav_orgs': fav_orgs
        })


class UserFavTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        all_fav_objs = UserFavourite.objects.filter(user=request.user, fav_type=3)
        fav_teacher_ids = [all_fav_obj.fav_id for all_fav_obj in all_fav_objs]
        fav_teachers = Teacher.objects.filter(pk__in=fav_teacher_ids)
        return render(request, 'usercenter-fav-teacher.html', {
            'fav_teachers': fav_teachers,
        })


class UserFavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        all_fav_objs = UserFavourite.objects.filter(user=request.user, fav_type=1)
        fav_course_ids = [fav_obj.fav_id for fav_obj in all_fav_objs]
        fav_courses = Course.objects.filter(pk__in=fav_course_ids)
        return render(request, 'usercenter-fav-course.html', {
            'fav_courses': fav_courses
        })


class UserMessageView(LoginRequiredMixin, View):
    def get(self, request):
        all_user_messages = UserMessage.objects.filter(user=request.user.pk)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_user_messages, 5, request=request)
        all_user_messages = p.page(page)

        return render(request, 'usercenter-message.html', {
            'all_user_messages': all_user_messages
        })