from collections import namedtuple
import json
from django.contrib import admin
from .models import Task,TaskStatus,Script,Tool,Ap,ApBorrowHistory,Driver,Module,PowerState,TaskFunction,TaskIssue,GeneralQueryString
from django.utils.html import format_html
import re
from django.utils.safestring import SafeString
# Register your models here.
@admin.register(TaskStatus)
class TaskStatusAdmin(admin.ModelAdmin):
    list_display = [ field.name for field in TaskStatus._meta.fields]
    list_editable = list_display.copy()
    list_editable.remove('id')
@admin.register(TaskIssue)
class TaskIssueAdmin(admin.ModelAdmin):
    list_display = [ field.name for field in TaskIssue._meta.fields]
    list_editable = ['title','description']
    list_filter = ['title','level']
    search_fields = ['task__uut__sn','title']
    
class TaskIssueInline(admin.TabularInline):
    model = TaskIssue
    extra = 2
    fieldsets = (
        (None, {
            "fields": (
                'title','level','power_state','device_driver','description','add_time'
            ),
            
        }),
    )

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
    list_editable.remove('uut_info')
    list_editable.remove('log')
    list_editable.remove('power_cycle_info')    


    list_display.remove('log')
    list_display.remove('group_uuid')
    list_display.remove('uut_info')
    list_display.remove('uut_uuid')
    list_display.remove('assigner')
    list_display.remove('power_cycle_info')
    list_display.insert(1,'platform_with_link')
    list_display.insert(3,'borrower_to_assigner')
    list_display.insert(3,'display_modules')
    list_display.insert(5,'display_cycles')
    list_display.insert(5,'display_issues')

    list_filter = ('status','start_time','finish_time','ap')
    search_fields = ('uut__platform_phase__platform__codename','uut__sn','script__name','group_name')
    inlines=[TaskIssueInline]

    hardwareid_query = GeneralQueryString.objects.get(name='hardwareid').query

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

    def display_cycles(self,obj):
        if obj.power_cycle_info:
            template=[]
            for state,cycle in obj.power_cycle_info.items():
                template.append(
                    f'<b>{state}</b> <span>{cycle}</span><br>'
                )
            return format_html('<hr>'.join(template))
        return None
    display_cycles.short_description = 'CYCLES'

    def display_modules(self,obj):
        modules = self.classify_module_driver(obj)
        info = self.format_os_cs_bios(obj)
        template = []
        if info:
            template.extend(
                [f'<b>Model</b><br><span>{info.model}</span>',
                f'<b>Build ID</b><br><span>{info.buildid}</span>',
                f'<b>SKU</b><br><span>{info.sku}</span>',
                f'<b>BIOS</b><br><span>{info.bios}</span>',
                f'<b>OS</b><br><span>{info.os}</span>',
                f'<b>ARCH</b><br><span>{info.arch}</span>',
                f'<b>Error</b><br><span>{info.error}</span><br>',]
            )
            for m in modules:
                template.append(
                    f'<b>{m.belong}</b><br><span>{m.name}</span><br><small>{m.dri_ver}</small>'
                )
            template = '<hr>'.join(template)
            return format_html(template)
        else: return None
    display_modules.short_description = 'INFO'

    def display_issues(self,obj):
        template =[]
        issues = obj.taskissue_set.all()
        if len(issues):
            for issue in issues:
                template.append(
                    f'<a href="/cat/taskissue/{issue.id}/change/">{issue.title}</a>'
                )
            template = '<br>'.join(template)
            return format_html(template)
        return '-'
    display_issues.short_description = 'ISSUES'

    def classify_module_driver(self,obj):
        class mod_dri:
            belong=''
            name=''
            hardwareid=''
            dri_ver=''

            def __init__(self,belong=None,name=None,hardwareid=None,dri_ver=None) -> None:
                self.belong = belong
                self.name = name
                self.hardwareid = hardwareid
                self.dri_ver = dri_ver

        show_modules = []
        uutinfo = obj.uut_info
        module_fields = ['lan','wlan','bt','wwan','nfc','rfid']
        if uutinfo:
            for module_types in module_fields:
                modules = uutinfo.get(module_types,None)
                if modules:
                    if type(modules) is list:
                        for module in modules:
                            hardwareID = module.get('HardWareID',None)
                            deviceName = module.get('DeviceName',None)
                            description = module.get('Description',None)
                            friendlyName = module.get('FriendlyName',None)
                            driverVersion = module.get('DriverVersion',None)
                            if hardwareID:
                                frieldly_name = description or deviceName or friendlyName
                                re_hardwardID = re.search(self.hardwareid_query,hardwareID)
                                if re_hardwardID:
                                    re_hardwardID =  re_hardwardID.groupdict()
                                    m,created = Module.objects.get_or_create(vender_id =re_hardwardID.get('ven',None),device_id = re_hardwardID.get('dev',None),subsys_vender_id = re_hardwardID.get('subsys',None),deliverable_name = frieldly_name)
                                    frieldly_name = m.short_name or frieldly_name 
                                    show_modules.append(mod_dri(module_types,frieldly_name,hardwareID,driverVersion))
                    else:
                        for wwan_submodule,wwan_submodules in modules.items():
                            if wwan_submodules:
                                if type(wwan_submodules) is list:
                                    for module in wwan_submodules:
                                        hardwareID = module.get('HardWareID',None)
                                        deviceName = module.get('DeviceName',None)
                                        description = module.get('Description',None)
                                        friendlyName = module.get('FriendlyName',None)
                                        driverVersion = module.get('DriverVersion',None)
                                        if hardwareID:
                                            frieldly_name = description or deviceName or friendlyName
                                            re_hardwardID = re.search(self.hardwareid_query,hardwareID)
                                            if re_hardwardID:
                                                re_hardwardID =  re_hardwardID.groupdict()
                                                m,created = Module.objects.get_or_create(vender_id =re_hardwardID.get('ven',None),device_id = re_hardwardID.get('dev',None),subsys_vender_id = re_hardwardID.get('subsys',None),deliverable_name = frieldly_name)
                                                frieldly_name = m.short_name or frieldly_name
                                                show_modules.append(mod_dri(wwan_submodule,frieldly_name,hardwareID,driverVersion))
                                elif type(wwan_submodules) is str:
                                    show_modules.append(mod_dri(wwan_submodule,wwan_submodules))

        return show_modules
    def format_os_cs_bios(self,obj):
        class osinfo:
            def __init__(self,model=None,buildid=None,sku=None,bios=None,os=None,arch=None) -> None:
                self.model = model
                self.buildid = buildid
                self.sku = sku
                self.bios = bios
                self.os = os
                self.arch = arch
                self.error = None
        info = obj.uut_info
        if info:
            cs = info.get('cs',None)
            bios = info.get('bios',None)
            os = info.get('os',None)
            try:
                buildid = None
                for oemstr in cs[0]['OEMStringArray']:
                    buildid = re.search('BUILDID#?(?P<buildid>.*);?',oemstr)
                    if buildid: 
                        buildid = buildid.groupdict()['buildid'] 
                        break
                info = osinfo(cs[0].get('Model',None),buildid,cs[0].get('SystemSKUNumber',None),bios[0].get('Caption',None), \
                            os[0].get('Version',None),os[0].get('OSArchitecture',None))
            except Exception as e:
                info = osinfo()
                info.error = e
        return info


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



@admin.register(GeneralQueryString)
class GeneralQueryStringAdmin(admin.ModelAdmin):
    list_display = [ field.name for field in GeneralQueryString._meta.fields]
    list_editable = list_display.copy()
    list_editable.remove('id')
