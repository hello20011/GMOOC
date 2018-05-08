import json

from django.db.models import Q
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from .models import Course
from operation.models import UserCourse, UserFavourite, CourseComments
from organization.models import CourseOrg
from utils.mixin_utils import LoginRequiredMixin

from pure_pagination import Paginator, PageNotAnInteger


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        top_courses = Course.objects.all().order_by('-click_nums')[:3]
        sort = request.GET.get('sort')

        keywords = request.GET.get('keywords')
        if keywords:
            all_courses = all_courses.filter(Q(name__contains=keywords)|Q(desc__contains=keywords))

        if sort:
            if sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')
            elif sort == 'students':
                all_courses = all_courses.order_by('-students')
        else:
            sort = ''

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 6, request=request)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            'courses': courses,
            'top_courses': top_courses,
            'sort' : sort,
        })


class CourseDetailView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        students = UserCourse.objects.filter(course_id=course_id)[:5]
        related_courses = Course.objects.filter(~Q(pk=course_id), tag=course.tag,)[:3]
        course.click_nums += 1
        course.save()
        is_faved_course = False
        is_faved_org = False
        if UserFavourite.objects.filter(user=request.user, fav_id=course.pk, fav_type=1):
            is_faved_course = True
        if UserFavourite.objects.filter(user=request.user, fav_id=course.course_org.pk, fav_type=2):
            is_faved_org = True
        return render(request, 'course-detail.html', {
            'course': course,
            'students': students,
            'related_courses': related_courses,
            'is_faved_course': is_faved_course,
            'is_faved_org': is_faved_org,
        })


class CourseVideoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        lessons = course.lesson_set.all()
        course_resources = course.get_resources()
        student_users = course.get_student_users()

        # 判断用户是否学习了这门课程，若没有学习则标记为已经开始学习
        if not UserCourse.objects.filter(user=request.user, course=course):
            user_course = UserCourse()
            user_course.user = request.user
            user_course.course = course
            user_course.save()
            course.students += 1
            course.save()

        # 循环遍历出此门课程学生的id
        stu_user_ids = [student_user.user_id for student_user in student_users]
        # 查出学过此门课程的学生学过的其他课程的id
        also_learnt_course_ids = [user_course_obj.course_id for user_course_obj in UserCourse.objects.filter(user_id__in=stu_user_ids)]
        # 在查出的结果中删掉本身的这门课程（防止重复）
        also_learnt_course_ids.remove(course_id)
        # 查出学过此门课程的学生学过的其他课程，取出其中点击量最高的五个
        also_learnt_courses = Course.objects.filter(pk__in=also_learnt_course_ids).order_by('-click_nums')[:5]

        return render(request, 'course-video.html', {
            'course': course,
            'lessons': lessons,
            'course_resources': course_resources,
            'also_learnt_courses': also_learnt_courses,
        })


class CourseCommentView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        course_resources = course.get_resources()
        student_users = course.get_student_users()
        comments = course.get_comments().order_by('-add_time')

        # 循环遍历出此门课程学生的id
        stu_user_ids = [student_user.user_id for student_user in student_users]
        # 查出学过此门课程的学生学过的其他课程的id
        also_learnt_course_ids = [user_course_obj.course_id for user_course_obj in UserCourse.objects.filter(user_id__in=stu_user_ids)]
        # 在查出的结果中删掉本身的这门课程（防止重复）
        also_learnt_course_ids.remove(course_id)
        # 查出学过此门课程的学生学过的其他课程，取出其中点击量最高的五个
        also_learnt_courses = Course.objects.filter(pk__in=also_learnt_course_ids).order_by('-click_nums')[:5]
        
        return render(request, 'course-comment.html', {
            'course': course,
            'course_resources': course_resources,
            'also_learnt_courses': also_learnt_courses,
            'comments': comments,
        })

    def post(self, request, course_id):
        course_comments = CourseComments()
        comments = request.POST.get('comments')
        if request.user.is_authenticated:
            course_comments.user = request.user
            course_comments.course_id = course_id
            course_comments.comments = comments
            course_comments.save()
            return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '用户未登录'}), content_type='application/json')
