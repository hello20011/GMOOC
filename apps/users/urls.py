from django.urls import path

from .views import UserInfoView, UserUploadView, UserResetPwdView, UserResetEmailCodeView, UserResetEmailCodeVerifyView, UserMyCourseView, UserFavOrgView, UserFavTeacherView, UserFavCourseView, UserMessageView

app_name = 'users'

urlpatterns = [
    path('info/', UserInfoView.as_view(), name='info'),
    path('upload/', UserUploadView.as_view(), name='upload'),
    path('reset_pwd/', UserResetPwdView.as_view(), name='reset_pwd'),
    path('reset_email/', UserResetEmailCodeView.as_view(), name='reset_email'),
    path('reset_email_code_verify/', UserResetEmailCodeVerifyView.as_view(), name='reset_email_code_verify'),
    path('my_course/', UserMyCourseView.as_view(), name='my_course'),
    path('my_fav_org/', UserFavOrgView.as_view(), name='my_fav_org'),
    path('my_fav_teacher/', UserFavTeacherView.as_view(), name='my_fav_teacher'),
    path('my_fav_course/', UserFavCourseView.as_view(), name='my_fav_course'),
    path('my_message/', UserMessageView.as_view(), name='my_message'),
]