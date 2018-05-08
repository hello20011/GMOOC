from django.urls import path
from .views import OrgView, UserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeachersView, AddFavView
from .views import TeachersListView, TeachersDetailView

app_name = 'organization'
urlpatterns = [
    path('list/', OrgView.as_view(), name="list"),
    path('add_user_ask/', UserAskView.as_view(), name="user_ask"),
    path('home/<int:org_id>/', OrgHomeView.as_view(), name="home"),
    path('course/<int:org_id>/', OrgCourseView.as_view(), name="course"),
    path('desc/<int:org_id>/', OrgDescView.as_view(), name="desc"),
    path('teachers/<int:org_id>/', OrgTeachersView.as_view(), name="teachers"),
    path('add_fav/', AddFavView.as_view(), name="add_fav"),
    # 授课教师相关的url配置
    path('teacher/list/', TeachersListView.as_view(), name="teachers_list"),
    path('teacher/detail/<int:teacher_id>/', TeachersDetailView.as_view(), name="teachers_detail"),
]