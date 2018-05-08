from django.urls import path

from .views import CourseListView, CourseDetailView, CourseVideoView, CourseCommentView

app_name = 'course'

urlpatterns = [
    path('list/', CourseListView.as_view(), name='list'),
    path('detail/<int:course_id>/', CourseDetailView.as_view(), name='detail'),
    path('video/<int:course_id>/', CourseVideoView.as_view(), name='video'),
    path('comment/<int:course_id>/', CourseCommentView.as_view(), name='comment'),
]