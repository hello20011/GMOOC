from datetime import datetime

from django.db import models

# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=20, verbose_name='城市')
    desc = models.CharField(max_length=150, verbose_name='描述')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=100, verbose_name='机构名称')
    desc = models.TextField(verbose_name='描述信息')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    image = models.ImageField(upload_to='org/%Y/%m', verbose_name='封面图')
    address = models.CharField(max_length=150, verbose_name='机构地址')
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING, verbose_name='所在城市')
    add_time = models.DateTimeField(default=datetime.now)
    students = models.IntegerField(default=0, verbose_name='学习人数')
    course_num = models.IntegerField(default=0, verbose_name='课程')
    category = models.CharField(choices=(('pxjg', '培训机构'), ('gx', '高校'), ('gr', '个人')), max_length=4, default='pxjg', verbose_name='机构类别')

    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, on_delete=models.DO_NOTHING, verbose_name='所属机构')
    name = models.CharField(max_length=50, verbose_name='教师名称')
    age = models.CharField(max_length=3, default='20', verbose_name='教师年龄')
    work_years = models.IntegerField(default=0, verbose_name='工作年限')
    work_company = models.CharField(max_length=50, verbose_name='就职公司')
    work_position = models.CharField(max_length=50, verbose_name='公司职位')
    points = models.CharField(max_length=50, verbose_name='教学特点')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    add_time = models.DateTimeField(default=datetime.now)
    image = models.ImageField(default='', upload_to='teacher/%Y/%m', verbose_name='教师头像')

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    def get_all_courses(self):
        return self.course_set.all()

    def __str__(self):
        return self.name
