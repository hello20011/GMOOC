"""GMOOC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve

import xadmin
from GMOOC.settings import MEDIA_ROOT

from users.views import LoginView, RegisterView, VerifyEmailView, ForgetPwdView, ResetPwdView

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name="index"),
    path('login/', LoginView.as_view(), name="login"),
    path('captcha/', include('captcha.urls')),
    path('register/', RegisterView.as_view(), name="register"),
    path('verify/', VerifyEmailView.as_view(), name="verify_email"),
    path('forgetpwd/', ForgetPwdView.as_view(), name="forgetpwd"),
    path('reset/', ResetPwdView.as_view(), name="resetpwd"),
    path('org/', include('organization.urls', namespace='org')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    path('course/', include('course.urls', namespace='course')),
    path('users/', include('users.urls', namespace='users')),
]
