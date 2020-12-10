from django.contrib import admin
from .models import Task,TaskStatus,Script,Tool,Ap,ApBorrowHistory,Driver,Module
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

@admin.register(Script)
class ScriptAdmin(admin.ModelAdmin):
    list_display = [ field.name for field in Script._meta.fields]
    list_editable = list_display.copy()
    list_editable.remove('id')
    list_editable.remove('create_time')

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