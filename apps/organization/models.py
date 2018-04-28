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


class CourseOrg(models.Model):
    name = models.CharField(max_length=100, verbose_name='机构名称')
    desc = models.TextField(verbose_name='描述信息')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    image = models.ImageField(upload_to='org/%Y/%m', verbose_name='封面图')
    address = models.CharField(max_length=150, verbose_name='机构名称')
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING, verbose_name='所在城市')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, on_delete=models.DO_NOTHING, verbose_name='所属机构')
    name = models.CharField(max_length=50, verbose_name='教师名称')
    work_years = models.IntegerField(default=0, verbose_name='工作年限')
    work_company = models.CharField(max_length=50, verbose_name='就职公司')
    work_position = models.CharField(max_length=50, verbose_name='公司职位')
    points = models.CharField(max_length=50, verbose_name='教学特点')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name
