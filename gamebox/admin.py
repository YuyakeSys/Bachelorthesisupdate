from django.contrib import admin

# Register your models here.
from django.http import HttpResponse
from openpyxl import Workbook

from .models import *


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ("name", 'age', 'email', 'status')

    list_editable = ['email']

    list_per_page = 6

    list_filter = ['status']

    search_fields = ['name']

    '''Replacement value for empty field'''
    empty_value_display = 'NA'

    actions = ["export_as_excel"]

    def export_as_excel(self, request, queryset):
        print("queryset", queryset)
        meta = self.model._meta  # 用于定义文件名, 格式为: app名.模型类名
        print("meta", meta)
        field_names = [field.name for field in meta.fields]  # 模型所有字段名

        response = HttpResponse(content_type='application/msexcel')  # 定义响应内容类型
        response['Content-Disposition'] = f'attachment; filename={meta}.xlsx'  # 定义响应数据格式
        wb = Workbook()  # 新建Workbook
        ws = wb.active  # 使用当前活动的Sheet表
        ws.append(field_names)  # 将模型字段名作为标题写入第一行
        for obj in queryset:  # 遍历选择的对象列表
            print(obj)
            for field in field_names:
                data = [f'{getattr(obj, field)}' for field in field_names]  # 将模型属性值的文本格式组成列表

            ws.append(data)  # 写入模型属性值
        wb.save(response)  # 将数据存入响应内容
        return response

    export_as_excel.short_description = 'export Excel'


admin.site.register(UserInfo, UserInfoAdmin)


class GameAdmin(admin.ModelAdmin):
    list_display = ("name", 'price', 'label', 'discount', 'views')

    list_editable = ['discount']

    list_per_page = 15

    list_filter = ['label']

    search_fields = ['name']

    '''Replacement value for empty field'''
    empty_value_display = 'NA'


class ListAdmin(admin.ModelAdmin):
    list_display = ("id", 'date_ordered', 'complete', 'customer_id', 'cost')

    list_per_page = 15

    ordering = ('date_ordered',)

    search_fields = ['customer_id']

    '''Replacement value for empty field'''
    empty_value_display = 'NA'


# for test only
class ListItemAdmin(admin.ModelAdmin):
    list_display = ("id", 'List_id', 'quantity', 'game_id')

    list_per_page = 15

    '''Replacement value for empty field'''
    empty_value_display = 'NA'


class AppealAdmin(admin.ModelAdmin):
    list_display = ("id", 'date', 'title', 'issue', 'user_id', 'solved')

    list_editable = ['solved']

    list_per_page = 15

    ordering = ('date', )

    list_filter = ['solved']

    search_fields = ['title']

    '''Replacement value for empty field'''
    empty_value_display = 'NA'


class CommentAdmin(admin.ModelAdmin):
    list_display = ("game_id", 'user_id', 'date', 'attitude', 'comment',)

    list_per_page = 15

    ordering = ('date', )

    list_filter = ['game_id']

    search_fields = ['game_id']

    '''Replacement value for empty field'''
    empty_value_display = 'NA'


admin.site.register(Game, GameAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(List, ListAdmin)
admin.site.register(ListItem, ListItemAdmin)
admin.site.register(Appeal, AppealAdmin)
