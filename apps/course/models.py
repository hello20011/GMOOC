from datetime import datetime

from django.db import models

from organization.models import CourseOrg, Teacher


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='课程所属机构')
    teacher = models.ForeignKey(Teacher, default=1, on_delete=models.DO_NOTHING, verbose_name='课程讲师')
    name = models.CharField(max_length=50, verbose_name='课程名')
    desc = models.CharField(max_length=300, verbose_name='课程描述')
    detail = models.TextField(verbose_name='课程详情')
    degree = models.CharField(choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), max_length=2, verbose_name='难度')
    learn_times = models.IntegerField(default=0, verbose_name='学习时常(分钟)')
    students = models.IntegerField(default=0, verbose_name='学生人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    image = models.ImageField(upload_to='courses/%Y/%m', verbose_name='课程封面图', max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    category = models.CharField(default='hdkf', max_length=6, choices=(('qdkf', '前端开发'), ('hdkf', '后端开发'), ('uisj', 'UI设计')), verbose_name='课程类型')
    tag = models.CharField(max_length=10, null=True, blank=True, verbose_name='标签')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    note = models.CharField(max_length=100, default='', verbose_name='课程须知')
    told = models.CharField(max_length=200, default='', verbose_name='老师告诉你能学到什么')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def get_lesson_num(self):
        return self.lesson_set.count()

    def get_resources(self):
        return self.courseresource_set.all()

    def get_student_users(self):
        return self.usercourse_set.all()

    def get_comments(self):
        return self.coursecomments_set.all()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def get_videos(self):
        return self.video_set.all()

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.DO_NOTHING, verbose_name='章节')
    name = models.CharField(max_length=100, verbose_name='视频名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='名称')
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name='资源文件')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
