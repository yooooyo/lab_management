from django.contrib import admin
from .models import Task,TaskStatus,Script,Tool,Ap,ApBorrowHistory,Driver,Module,PowerState,TaskFunction,TaskIssue
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
    list_editable = list_display.copy()
    list_editable.remove('id')