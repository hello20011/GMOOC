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
from django.views.static import serve

import xadmin
from GMOOC.settings import MEDIA_ROOT
# from GMOOC.settings import STATIC_ROOT

from users.views import IndexView, LoginView, RegisterView, VerifyEmailView, ForgetPwdView, ResetPwdView, LoginoutView

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('', IndexView.as_view(), name="index"),
    path('login/', LoginView.as_view(), name="login"),
    path('loginout/', LoginoutView.as_view(), name='logout'),
    path('captcha/', include('captcha.urls')),
    path('register/', RegisterView.as_view(), name="register"),
    path('verify/', VerifyEmailView.as_view(), name="verify_email"),
    path('forgetpwd/', ForgetPwdView.as_view(), name="forgetpwd"),
    path('reset/', ResetPwdView.as_view(), name="resetpwd"),
    path('org/', include('organization.urls', namespace='org')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    # re_path(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
    path('course/', include('course.urls', namespace='course')),
    path('users/', include('users.urls', namespace='users')),
]

hander404 = 'users.views.page_not_found'
hander500 = 'users.views.server_error'
