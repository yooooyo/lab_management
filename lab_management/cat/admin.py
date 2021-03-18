from django.contrib import admin
from .models import Task,TaskStatus,Script,Tool,Ap,ApBorrowHistory,Driver,Module,PowerState,TaskFunction,TaskIssue
from django.utils.html import format_html
# Register your models here.
@admin.register(TaskStatus)
class TaskStatusAdmin(admin.ModelAdmin):
    list_display = [ field.name for field in TaskStatus._meta.fields]
    list_editable = list_display.copy()
    list_editable.remove('id')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [ field.name for field in Task._meta.fields]


    list_editable = list_display.copy()
    list_editable.remove('id')
    list_editable.remove('start_time')
    list_editable.remove('add_time')
    list_editable.remove('finish_time')
    list_editable.remove('uut')
    list_editable.remove('assigner')
    list_editable.remove('group_uuid')
    list_editable.remove('group_series')
    list_editable.remove('script')
    list_editable.remove('uut_uuid')

    list_display.remove('group_uuid')
    list_display.remove('uut_uuid')
    list_display.remove('assigner')
    list_display.insert(1,'platform_with_link')
    list_display.insert(3,'borrower_to_assigner')

    list_filter = ('status','start_time','finish_time','ap')
    search_fields = ('uut__platform_phase__platform__codename','uut__sn','script__name')

    def platform_with_link(self,obj):
        if obj.uut:
            template = f'<b><a href="/iur/platform/{obj.uut.platform_phase.platform.id}/change/">{obj.uut.platform_phase.platform.codename}</a></b>'
            return format_html(template)
        else:
            return '-'
    platform_with_link.short_description='PLATFORM'

    def borrower_to_assigner(self,obj):
        return obj.uut.borrower
    borrower_to_assigner.short_description='ASSIGNER'

@admin.register(Script)
class ScriptAdmin(admin.ModelAdmin):
    list_display = [ field.name for field in Script._meta.fields]
    list_editable = list_display.copy()
    list_editable.remove('id')
    list_editable.remove('add_time')

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = [ field.name for field in Tool._meta.fields]
    list_editable = list_display.copy()
    list_editable.remove('id')

@admin.register(Ap)
class ApAdmin(admin.ModelAdmin):
    list_display = [ field.name for field in Ap._meta.fields]
    list_editable = list_display.copy()
    list_editable.remove('id')

@admin.register(ApBorrowHistory)
class ApBorrowHistoryAdmin(admin.ModelAdmin):
    list_display = [ field.name for field in ApBorrowHistory._meta.fields]
    list_editable = list_display.copy()
    list_editable.remove('id')

@admin.register(Driver) 
class DriverAdmin(admin.ModelAdmin):
    list_display = [ field.name for field in Driver._meta.fields]
    list_editable = list_display.copy()
    list_editable.remove('id') 

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = [ field.name for field in Module._meta.fields]
    list_editable = list_display.copy()
    list_editable.remove('id')

@admin.register(PowerState)
class PowerStateAdmin(admin.ModelAdmin):
    list_display = [ field.name for field in PowerState._meta.fields]
    list_editable = list_display.copy()
    list_editable.remove('id')

@admin.register(TaskFunction)
class TaskFunctiondmin(admin.ModelAdmin):
    list_display = [ field.name for field in TaskFunction._meta.fields]
    list_editable = list_display.copy()
    list_editable.remove('id')

@admin.register(TaskIssue)
class TaskIssueAdmin(admin.ModelAdmin):
    list_display = [ field.name for field in TaskIssue._meta.fields]
    list_editable = ['title','description']
