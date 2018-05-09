import xadmin

from .models import Course, Lesson, Video, CourseResource, CourseBanner


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums',
                    'add_time', 'go_to']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums',
                   'add_time']

    # ordering = ['-click_nums'] 打开页面后默认的排序字段

    # 更改后台左边每个model选项卡前的图标(font-awesome)
    model_icon = 'fa fa-book'

    # 对后台数据(queryset)的显示进行过滤，只显示不是banner的课程
    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    # 在后台保存课程数据的时候统计所有该机构下课程的数量并保存到相应机构的course_num字段中
    def save_models(self):
        obj = self.org_obj  # debug看了下这里是org_obj
        obj.save()
        if obj.course_org:
            course_org = obj.course_org
            course_org.course_num = Course.objects.filter(course_org=course_org).count()
            course_org.save()


class CourseBannerAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums',
                    'add_time', 'go_to']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums',
                   'add_time']

    # 只读字段(在后台页面只能查看的字段，不能进行修改)
    readonly_fields = ['click_nums', 'fav_nums', 'add_time']

    # exclude = ['fav_nums'] 让管理页面不显示这个字段
    # (同一个字段不能同时在readonly_fields和exclude中，否则会产生冲突)

    # ordering = ['-click_nums'] 打开页面后默认的排序字段

    # 更改后台左边每个model选项卡前的图标（font-awesome）
    model_icon = 'fa fa-picture-o'

    # 对后台数据(queryset)的显示进行过滤，只显示是banner的课程
    def queryset(self):
        qs = super(CourseBannerAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs

    # 在后台保存课程数据的时候统计所有该机构下课程的数量并保存到相应机构的course_num字段中
    def save_models(self):
        obj = self.org_obj
        obj.save()
        if obj.course_org:
            course_org = obj.course_org
            course_org.course_num = Course.objects.filter(course_org=course_org).count()
            course_org.save()


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course__name', 'name']
    list_filter = ['course__name', 'name', 'add_time']

    # 更改后台左边每个model选项卡前的图标（font-awesome）
    model_icon = 'fa fa-book'


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson__name', 'name']
    list_filter = ['lesson__name', 'name']

    # 更改后台左边每个model选项卡前的图标（font-awesome）
    model_icon = 'fa fa-video-camera'


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course__name', 'download', 'name']
    list_filter = ['course__name', 'name', 'download', 'add_time']

    # 更改后台左边每个model选项卡前的图标（font-awesome）
    model_icon = 'fa fa-folder'


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(CourseBanner, CourseBannerAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
