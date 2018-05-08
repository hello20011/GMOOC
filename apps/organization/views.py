import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .models import CourseOrg, City, Teacher
from .forms import UserAskForm
from course.models import Course
from operation.models import UserFavourite

from pure_pagination import Paginator, PageNotAnInteger


class OrgView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        all_city = City.objects.all()
        top_orgs = CourseOrg.objects.order_by('-click_nums')[:5]

        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=city_id)

        cate = request.GET.get('ct', '')
        if cate:
            all_orgs = all_orgs.filter(category=cate)

        sort = request.GET.get('sort')
        if sort == 'students':
            all_orgs = all_orgs.order_by('-students')
        elif sort == 'courses':
            all_orgs = all_orgs.order_by('-course_num')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 5, request=request)
        orgs = p.page(page)

        all_orgs_count = all_orgs.count()

        return render(request, 'org-list.html', {
            'all_orgs': orgs,
            'all_city': all_city,
            'all_orgs_count': all_orgs_count,
            'city_id': city_id,
            'cate': cate,
            'top_orgs': top_orgs,
            'sort': sort,
        })


class UserAskView(View):
    def post(self, request):
        user_ask_form = UserAskForm(request.POST)
        if user_ask_form.is_valid():
            user_ask_form.save(commit=True)
            return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '添加错误'}), content_type='application/json')


class OrgHomeView(View):
    def get(self, request, org_id):
        org = CourseOrg.objects.get(pk=int(org_id))
        org.click_nums += 1
        org.save()
        courses = org.course_set.all()[:3]
        teachers = org.teacher_set.all()[:1]
        is_faved = False
        if request.user.is_authenticated:
            if UserFavourite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                is_faved = True
        return render(request, 'org-detail-homepage.html', {
            'page_name': 'home',
            'org': org,
            'courses': courses,
            'teachers': teachers,
            'is_faved': is_faved,
        })


class OrgCourseView(View):
    def get(self, request, org_id):
        org = CourseOrg.objects.get(pk=int(org_id))
        courses = org.course_set.all()
        is_faved = False
        if request.user.is_authenticated:
            if UserFavourite.objects.filter(user=request.user, fav_id=org.pk, fav_type=2):
                is_faved = True
        return render(request, 'org-detail-course.html', {
            'page_name': 'course',
            'org': org,
            'courses': courses,
            'is_faved': is_faved,
        })


class OrgDescView(View):
    def get(self, request, org_id):
        org = CourseOrg.objects.get(pk=org_id)
        is_faved = False
        if request.user.is_authenticated:
            if UserFavourite.objects.filter(user=request.user, fav_id=org.pk, fav_type=2):
                is_faved = True
        return render(request, 'org-detail-desc.html', {
            'page_name': 'desc',
            'org': org,
            'is_faved': is_faved,
        })


class OrgTeachersView(View):
    def get(self, request, org_id):
        org = CourseOrg.objects.get(pk=org_id)
        teachers = Teacher.objects.filter(org_id=org_id)
        is_faved = False
        if request.user.is_authenticated:
            if UserFavourite.objects.filter(user=request.user, fav_id=org.pk, fav_type=2):
                is_faved = True
        return render(request, 'org-detail-teachers.html', {
            'page_name': 'teachers',
            'org': org,
            'teachers': teachers,
            'is_faved': is_faved,
        })


class AddFavView(View):
    def post(self, request):
        try:
            fav_id = int(request.POST.get('fav_id'))
            fav_type = int(request.POST.get('fav_type'))
        except Exception as ret:
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '参数错误'}), content_type="application/json")
        else:
            if request.user.is_authenticated:
                user = request.user
                if UserFavourite.objects.filter(user=user, fav_id=fav_id, fav_type=fav_type).count() == 0:
                    user_fav = UserFavourite()
                    user_fav.user = user
                    user_fav.fav_id = fav_id
                    user_fav.fav_type = fav_type
                    user_fav.save()
                    return HttpResponse(json.dumps({'status': 'success', 'msg': '已收藏'}), content_type="application/json")
                else:
                    user_fav = UserFavourite.objects.get(user=user, fav_id=fav_id, fav_type=fav_type)
                    user_fav.delete()
                    return HttpResponse(json.dumps({'status': 'success', 'msg': '收藏'}), content_type="application/json")
            else:
                return HttpResponse(json.dumps({'status': 'fail', 'msg': '用户未登录'}), content_type="application/json")


class TeachersListView(View):
    def get(self, request):
        teachers = Teacher.objects.all()
        top_teachers = Teacher.objects.all().order_by('-click_nums')[:3]
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            teachers = teachers.order_by('-click_nums')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(teachers, 5, request=request)
        teachers = p.page(page)

        teachers_num = teachers.object_list.count()

        return render(request, 'teachers-list.html', {
            'teachers': teachers,
            'top_teachers': top_teachers,
            'teachers_num': teachers_num,
            'sort': sort,
        })


class TeachersDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(pk=teacher_id)
        teacher.click_nums += 1
        teacher.save()
        teacher_courses = teacher.get_all_courses()
        top_teachers = Teacher.objects.all().order_by('-click_nums')[:5]
        is_faved_teacher = False
        is_faved_org = False
        if request.user.is_authenticated:
            if UserFavourite.objects.filter(fav_id=teacher_id, fav_type=3):
                is_faved_teacher = True
            if UserFavourite.objects.filter(fav_id=teacher.org.pk, fav_type=2):
                is_faved_org = True
        return render(request, 'teacher-detail.html', {
                'teacher': teacher,
                'teacher_courses': teacher_courses,
                'top_teachers': top_teachers,
                'is_faved_teacher': is_faved_teacher,
                'is_faved_org': is_faved_org,
            })
