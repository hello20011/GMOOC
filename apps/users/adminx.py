import xadmin
from xadmin import views

from users.models import EmailVerifyRecord, Banner


# xadmin全局的基础设置
class BaseSetting(object):
    enable_themes = True  # 开启xadmin的主题功能
    use_bootswatch = True  # 开启bootswatch主题包


class GlobalSetting(object):
    site_title = "慕学后台管理系统"  # 设置后台网站的标题(左上角的文字)
    site_footer = "慕学在线网"  # 设置后台的页脚文字
    menu_style = "accordion"  # 设置后台左侧菜单栏的样式(折叠样式)


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']

    # 更改后台左边每个model选项卡前的图标(font-awesome)
    model_icon = 'fa fa-envelope'

    # 不能修改的字段
    readonly_fields = ['send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index']

    # 更改后台左边每个model选项卡前的图标(font-awesome)
    model_icon = 'fa fa-picture-o'

    # 不能修改的字段
    readonly_fields = ['add_time']


# BaseAdminView需要注册到BaseSetting
xadmin.site.register(views.BaseAdminView, BaseSetting)
# CommAdminView需要注册到GlobalSetting
xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
