from django.contrib import admin,messages
from django.contrib.auth.models import Group,User
from django.utils.html import format_html
from django.utils.translation import ngettext
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.db.models import Q
from .models import Uut,Platform,UutBorrowHistory,UutPhase,Member,UutStatus
# Register your models here.

admin.site.site_header = 'Lab Admin'
admin.site.site_title  = 'Lab_Admin'
admin.site.enable_nav_sidebar = True

# admin.site.unregister(User)
# admin.site.unregister(Group)

@admin.register(UutStatus)
class UutStatusAdmin(admin.ModelAdmin):
    pass

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    search_fields = ('usernameincompany',)
    pass

@admin.register(UutPhase)
class UutPhaseAdmin(admin.ModelAdmin):
    pass

class UutInline(admin.TabularInline):
    model = Uut
    extra = 2
    fieldsets = (
        (None, {
            "fields": (
                'sn','phase','sku','cpu','position','status',
            ),
            
        }),
    )

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    search_fields = ('codename','marketing_name')
    list_filter = ('series','codename')
    list_display = ('codename','chipset','group','target','cycle','series','marketing_name','odm')

    # inlines = [
    #     UutInline,
    # ]

    fieldsets = (
        ('Solid info', {
            "fields": (
                'codename','chipset','group','target','cycle','series','marketing_name','odm'
            ),
        }),
        ('Plan info', {
            "fields": (
                'content','behavior','development_center','forecast_cycle','forecast_series','sepm','pdm'
            ),
            # "classes":('wide','extrapretty'),
            "classes":('collapse',),
            # "description":'<code> UUT storage information </code>',
        }),
    )

@admin.register(UutBorrowHistory)
class UutBorrowHistoryAdmin(admin.ModelAdmin):
    list_display = ('uut','member','rent_time','back_time')
    fields = ('uut','member','back_time','purpose')
    search_fields=('member__usernameincompany','uut__sn',)
    raw_id_fields = ('uut','member')
    autocomplete_fields=('uut','member')
    pass

@admin.register(Uut)
class UutAdmin(admin.ModelAdmin):

    #### settings
    # using = 'labpostgres' 

    ###  settings list objects
    # list_max_show_all = 50
    list_per_page = 20
    list_display = ('id','platform_with_link','platform_group_display','platform_target_display','platform_cycle_display','phase','sku','sn','borrower_display','status','scrap','position','cpu','remark','keyin_time')
    # list_editable = ('position','cpu','remark')
    list_filter = ('scrap','phase','status','platform__group','platform__target','position')
    date_hierarchy ='keyin_time'
    list_display_links = ('sn',)
    search_fields = ('sn','platform__codename','uutborrowhistory__member__usernameincompany')
    # search_fields = ('sn','platform__codename',)

    show_full_result_count = True
    # radio_fields = {"phase":admin.VERTICAL}

    ###  setting change list
    # raw_id_fields = ('platform',)
    list_select_related =  ('platform',)
    autocomplete_fields = ['platform',]
    # readonly_fields = ('sn',)
    fieldsets = (
        # ('UUT info', {
        #     "fields": (
        #         'sn','sku','phase','platform',
            # ),
            # "classes": (
            #     'wide','extrapretty'
            # ),
        # }),
        # ('STORAGE info', {
        #     "fields": (
        #         'position',
        #     ),
            # "classes":('wide','extrapretty'),
            # "classes":('collapse',),
            # "description":'<code> UUT storage information </code>',
        # }),
        (None,{
            "fields":(
                'phase','platform','status'
            )
        }),
    )


    def colored_phase(self,obj):
        
        return format_html(f'<span style="color: blue">{obj.phase}</span>')
    colored_phase.short_description = 'PHASE'
    colored_phase.admin_order_field = 'phase'

    def borrower_display(self,obj):
        borrower = obj.uutborrowhistory_set.filter(back_time__isnull=True).last()
        if borrower: 
            template = f'{borrower.member.usernameincompany}<br><small style="color:gray;">{borrower.rent_time}</small>'
            return format_html(template)
        return '-'
    borrower_display.short_description = 'BORROWER'
    # borrower_display.admin_order_field = 'uutborrowhistory__member__name'

    def platform_with_link(self,obj):
        if obj.platform:
            template = f'<b><a href="/iur/platform/{obj.platform.id}/change/">{obj.platform.codename}</a></b>'
            return format_html(template)
        else:
            return '-'
    platform_with_link.short_description='PLATFORM'
    platform_with_link.admin_order_field='platform'

    def platform_group_display(self,obj):
        if obj.platform:
            return obj.platform.group
        else:
            return '-'
    platform_group_display.short_description = 'GROUP'
    platform_group_display.admin_order_field='platform__group'

    def platform_target_display(self,obj):
        if obj.platform:
            return obj.platform.target
        else:
            return '-'
    platform_target_display.short_description = 'TARGET'
    platform_target_display.admin_order_field='platform__target'

    def platform_cycle_display(self,obj):
        if obj.platform:
            return obj.platform.cycle
        else:
            return '-'
    platform_cycle_display.short_description = 'CYCLE'
    platform_cycle_display.admin_order_field='platform__cycle'

    #override
    # def save_model(self, request, obj, form, change):
    #     # Tell Django to save objects to the 'other' database.
    #     obj.save(using=self.using)

    # def delete_model(self, request, obj):
    #     # Tell Django to delete objects from the 'other' database
    #     obj.delete(using=self.using)

    # def get_queryset(self, request):
    #     # Tell Django to look for objects on the 'other' database.
    #     return super().get_queryset(request).using(self.using).select_related('platform').order_by('-keyin_time')

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     # Tell Django to populate ForeignKey widgets using a query
    #     # on the 'other' database.
    #     return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     # Tell Django to populate ManyToMany widgets using a query
    #     # on the 'other' database.
    #     return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


    # actions
    actions = ['mark_scrap','mark_unscrap','edit_uuts']

    def mark_scrap(self,request,queryset):
        be_updated = queryset.update(scrap = True)
        self.message_user(request,ngettext(f'{be_updated} item was mark scrap',f'{be_updated} items were mark scrap',be_updated),messages.SUCCESS)
        
    mark_scrap.short_description = 'Scrap'

    def mark_unscrap(self,request,queryset):
        be_updated = queryset.update(scrap = False)
        self.message_user(request,ngettext(f'{be_updated} item was mark unscrap',f'{be_updated} items were mark unscrap',be_updated),messages.SUCCESS)
    mark_unscrap.short_description = 'UnScrap'

    # def edit_uuts(self,request,queryset):
    #     # self.list_editable = ()
    #     return HttpResponse('edit/',{'uut':queryset})
    # edit_uuts.short_description = 'Edit UUTs'
    # custom view

    add_form_template = 'admin/add_uut_template.html'

    def save_model(self, request, obj, form, change):
        if request.method == 'POST' and 'uut-save' in request.POST:
            if not obj.platform or not obj.phase:
                messages.error(request,'Platform or phase empty !')
            else:
                sn_list = request.POST.getlist('sn')
                sku_list = request.POST.getlist('sku')
                position_list = request.POST.getlist('position')
                for sn,sku,position in zip(sn_list,sku_list,position_list):
                    if sn:
                        Uut.objects.create(sn = sn,sku=sku,position=position,phase = obj.phase,platform=obj.platform)
                    else:
                        messages.error(request,'SN empty !')
            return
            # self.message_user(request,f'{len(sn_list)} uut be added.',messages.SUCCESS)
        if self.list_editable:
            self.list_editable = None
        return super().save_model(request, obj, form, change)

    change_list_template = 'admin/uut_changelist_template.html'      
    def get_search_results(self,request,queryset,term):
        print('get_search_results')
        def exclude_borrower_has_returned_uut(qs,term):
            _qs = qs
            member_lookup = Member.objects.filter(usernameincompany__search=term)
            if member_lookup.count()>0:
                for uut in qs:
                    u = uut.uutborrowhistory_set.filter(member__usernameincompany__search=term).filter(back_time__isnull=True).last()
                    if not u:
                        _qs = _qs.exclude(sn=uut.sn)
            return _qs
        # self.get_search_results(request,queryset)
        qs ,use_distinct = super().get_search_results(request,queryset,term)
        qs = exclude_borrower_has_returned_uut(qs,term)
        return qs,use_distinct

    def changelist_view(self, request, extra_context=None):

        changelist_view = super().changelist_view(request, extra_context)
        if hasattr(changelist_view,'context_data'):
            changelist_view.context_data['title'] = 'IUR'
            
            class Dropdown:
                self.buttonName=''
                self.dataList=list()
                def __init__(self,buttonName,dataList):
                    self.buttonName = buttonName
                    self.dataList = dataList


            platform = changelist_view.context_data['cl'].queryset.order_by('platform__codename').values_list('platform','platform__codename').distinct()
            platform = Dropdown('Platform',platform)
            borrower = changelist_view.context_data['cl'].queryset.order_by('uutborrowhistory__member__usernameincompany').filter(Q(uutborrowhistory__isnull=False)&Q(uutborrowhistory__back_time__isnull=True)).values_list('uutborrowhistory__member','uutborrowhistory__member__usernameincompany').distinct()
            borrower = Dropdown('Borrower',borrower)
            dropdown={'dropdown':[platform,borrower]}

            changelist_view.context_data.update(dropdown)
        
        return changelist_view

    # def get_changelist_instance(self, request):
    #     change_instance = super().get_changelist_instance(request)
    #     # change_instance.result_list = change_instance.result_list.filter(pk=2)
    #     return change_instance

    def response_add(self, request, obj, post_url_continue=None):
        add = super().response_add(request, obj, post_url_continue=post_url_continue) 
        
        return add

    def get_queryset(self, request):
        # initial load UUT
        qs = super().get_queryset(request)
        request.GET = request.GET.copy()
        selected_platform_id = request.GET.pop('selectPlatform',None)
        if selected_platform_id:
            qs = qs|qs.filter(platform__in=selected_platform_id)
        # if 'search_adv' in request.GET:
        #     # can't remember last query
        #     selected_platform_id = request.GET.getlist('selectPlatform',None)
        #     selected_platform_id = request.GET.getlist('selectBorrower',None)
        #     p = qs.filter(platform__in=selected_platform_id)
        #     b = qs.filter(Q(uutborrowhistory__isnull=False)&Q(uutborrowhistory__back_time__isnull=True)&Q(uutborrowhistory__member__in=selected_borrower_id))
        #     qs = p|b
        print(f'get queryset {len(qs)}')
        return qs

    def get_urls(self):
        # add custome url here
        print('get_urls')
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('edit/', self.admin_site.admin_view(self.edit_uut)),
        ]
        print(urls)
        return custom_urls+urls

    

    def edit_uut(self,request):
        
        return TemplateResponse(request,'admin/uut_base_site.html')





    



    





    
