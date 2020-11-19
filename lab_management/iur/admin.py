from django.contrib import admin,messages
from django.contrib.auth.models import Group,User
from django.http import request
from django.utils.html import format_html
from django.utils.translation import ngettext
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.db.models import Q
from .models import Uut,Platform,UutBorrowHistory,UutPhase,Member,UutStatus
from django import forms
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
    list_display = ('id','uut','member','purpose','rent_time','back_time')
    fields = ('uut','member','back_time','purpose')
    search_fields=('member__usernameincompany','uut__sn',)
    raw_id_fields = ('uut','member')
    autocomplete_fields=('uut','member')
    list_filter = ('rent_time','back_time')
    date_hierarchy ='rent_time'
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

    actions = ['mark_scrap','mark_unscrap','rent_back','edit_uuts_action','borrow_and_transfer_action']



    def mark_scrap(self,request,queryset):
        if request.user.is_superuser:
            be_updated = queryset.update(scrap = True)
            self.message_user(request,ngettext(f'{be_updated} item was mark scrap',f'{be_updated} items were mark scrap',be_updated),messages.SUCCESS)
    mark_scrap.short_description = 'Scrap'

    def mark_unscrap(self,request,queryset):
        if request.user.is_superuser:
            be_updated = queryset.update(scrap = False)
            self.message_user(request,ngettext(f'{be_updated} item was mark unscrap',f'{be_updated} items were mark unscrap',be_updated),messages.SUCCESS)
    mark_unscrap.short_description = 'UnScrap'

    def rent_back(self,request,queryset):
        if request.user.is_superuser:
            self.rent_back_uuts(queryset)
    rent_back.short_description = 'Rent Back'

    def edit_uuts_action(self,request,queryset):
        # self.list_editable = ()
        if request.user.is_superuser:
            if queryset:
                ids = '&'.join([ f'id={q.id}' for q in queryset])
                return HttpResponseRedirect(f'edit/?{ids}')
    edit_uuts_action.short_description = 'Edit UUTs'

    def borrow_and_transfer_action(self,request,queryset):
        # self.list_editable = ()
        if request.user.is_superuser:
            if queryset:
                ids = '&'.join([ f'id={q.id}' for q in queryset])
                return HttpResponseRedirect(f'borrow/?{ids}')
    borrow_and_transfer_action.short_description = 'Borrow UUTs'

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
        def exclude_borrower_has_returned_uut(qs,term):
            _qs = qs
            member_lookup = Member.objects.filter(usernameincompany__search=term)
            if member_lookup.count()>0:
                for uut in qs:
                    u = uut.uutborrowhistory_set.filter(member__usernameincompany__search=term).filter(back_time__isnull=True).last()
                    if not u:
                        _qs = _qs.exclude(sn=uut.sn)
            return _qs
        qs ,use_distinct = super().get_search_results(request,queryset,term)

        if term:            
            qs = exclude_borrower_has_returned_uut(qs,term)
        return qs,use_distinct

    saved_dropdown_dict = dict()


    def advance_search_dropdown_filter(self,qs):
        class Dropdown:
            template=''
            default=[]
            saved=[]
            def __init__(self,buttonName,dataList,default=[]):
                self.buttonName = buttonName
                self.dataList = dataList
                self.default = default

            
            def format_html(self):
                if self.dataList:
                    for Id,data in self.dataList:
                        if str(Id) in self.saved or data in self.default:
                            self.template += f'<li class="active" value={data}><label><input type="checkbox" name="select{self.buttonName}" value="{Id}" checked> {data}</label></li>'
                        else:
                            self.template += f'<li value={data}><label><input type="checkbox" name="select{self.buttonName}" value="{Id}"> {data}</label></li>'
                    return format_html(self.template)
            
            def keep_filter_list(self,selected_list):
                if not selected_list and self.saved:
                    return self.saved


        platform = qs.order_by('platform__codename').values_list('platform','platform__codename').distinct()
        platform = Dropdown('Platform',platform)
        self.saved_dropdown_dict.update({'platform':platform})

        borrower = qs.order_by('uutborrowhistory__member__usernameincompany').filter(Q(uutborrowhistory__back_time__isnull=True)).values_list('uutborrowhistory__member','uutborrowhistory__member__usernameincompany').distinct()
        borrower = Dropdown('Borrower',borrower)
        self.saved_dropdown_dict.update({'borrower':borrower})

        group = qs.values_list('platform__group','platform__group').distinct()
        group = Dropdown('Group',group)
        self.saved_dropdown_dict.update({'group':group})

        target = qs.order_by('platform__target').values_list('platform__target','platform__target').distinct()
        target = Dropdown('Target',target)
        self.saved_dropdown_dict.update({'target':target})

        cycle = qs.order_by('platform__cycle').values_list('platform__cycle','platform__cycle').distinct()
        cycle = Dropdown('Cycle',cycle)
        self.saved_dropdown_dict.update({'cycle':cycle})

        phase = qs.order_by('phase__phase_text').values_list('phase','phase__phase_text').distinct()
        phase = Dropdown('Phase',phase)
        self.saved_dropdown_dict.update({'phase':phase})

        sku = qs.order_by('sku').values_list('sku','sku').distinct()
        sku = Dropdown('SKU',sku)
        self.saved_dropdown_dict.update({'sku':sku})

        status = qs.order_by('status__status_text').values_list('status','status__status_text').distinct()
        status = Dropdown('Status',status)
        self.saved_dropdown_dict.update({'status':status})

        scrap = qs.values_list('scrap','scrap').distinct()
        scrap = Dropdown('Scrap',scrap,[False,])
        self.saved_dropdown_dict.update({'scrap':scrap})

        position = qs.order_by('position').values_list('position','position').distinct()
        position = Dropdown('Position',position)
        self.saved_dropdown_dict.update({'position':position})
        
        return [platform,borrower,phase,group,target,cycle,sku,status,scrap,position]

    def changelist_view(self, request, extra_context=None):
        
        if not request.user.is_superuser:
            self.actions = []
        qs = self.get_queryset(request)
        

        
        dropdown = self.advance_search_dropdown_filter(qs)
        extra_context = dropdown={'dropdown':dropdown}
        changelist_view = super().changelist_view(request, extra_context)
        if hasattr(changelist_view,'context_data'):
            changelist_view.context_data['title'] = 'IUR'
        # changelist_view.context_data.update(dropdown)


        # if request.POST.get('search-adv',False):

        #     selected_platform_id = request.POST.getlist('selectPlatform',None)
        #     selected_borrower_id = request.POST.getlist('selectBorrower',None)
        #     if selected_platform_id:
        #         qs = qs.filter(platform__in=selected_platform_id)
        #         if selected_borrower_id:
        #             qs = qs.intersection(qs.filter(Q(uutborrowhistory__isnull=False)&Q(uutborrowhistory__back_time__isnull=True)&Q(uutborrowhistory__member__in=selected_borrower_id)))
        #         if qs:
        #             self.list_per_page = 1000
        # else:
        #     self.list_per_page = 20
        #     selectPlatform_saved = []

        return changelist_view

    def get_changelist(self, request, **kwargs):
        from django.contrib.admin.views.main import ChangeList
        return ChangeList

    # def get_changelist_instance(self, request):
    #     change_instance = super().get_changelist_instance(request)
    #     # change_instance.result_list = change_instance.result_list.filter(pk=2)
    #     return change_instance

    def response_add(self, request, obj, post_url_continue=None):
        add = super().response_add(request, obj, post_url_continue=post_url_continue) 
        
        return add
    
    def advance_search_dropdown_filter_query(self,request,qs):
        if request.POST.get('search-adv',False):
            
            selected_platform_id = request.POST.getlist('selectPlatform',None)
            selected_borrower_id = request.POST.getlist('selectBorrower',None)
            selected_group = request.POST.getlist('selectGroup',None)
            selected_target = request.POST.getlist('selectTarget',None)
            selected_cycle = request.POST.getlist('selectCycle',None)
            selected_phase_id = request.POST.getlist('selectPhase',None)
            selected_sku = request.POST.getlist('selectSKU',None)
            selected_status_id = request.POST.getlist('selectStatus',None)
            selected_scrap = request.POST.getlist('selectScrap',None)
            selected_position = request.POST.getlist('selectPosition',None)

            # if not selected_platform_id and self.selectPlatform_saved:
            #     selected_platform_id = self.selectPlatform_saved
            selected = False
            if selected_platform_id:
                # self.selectPlatform_saved = selected_platform_id
                selected = True
                b =self.saved_dropdown_dict.get('platform',None)
                if b: b.saved = selected_platform_id
                qs = qs.filter(platform__in=selected_platform_id)

            if selected_borrower_id:
                selected = True
                b =self.saved_dropdown_dict.get('borrower',None)
                if b: b.saved = selected_borrower_id
                if 'None' in selected_borrower_id:
                    selected_borrower_id.remove('None')
                    qs = qs.filter(uutborrowhistory__isnull=True)
                if selected_borrower_id:
                    qs = qs.filter(Q(uutborrowhistory__back_time__isnull=True)&Q(uutborrowhistory__member__in=selected_borrower_id))
            if selected_group:
                selected = True
                b =self.saved_dropdown_dict.get('group',None)
                if b: b.saved = selected_borrower_id
                if 'None' in selected_group:
                    selected_group.remove('None')
                    qs = qs.filter(platform__group__isnull=True)
                if selected_group:
                    qs = qs.filter(platform__group__in=selected_group)
            if selected_target:
                selected = True
                b =self.saved_dropdown_dict.get('target',None)
                if b: b.saved = selected_target
                if 'None' in selected_target:
                    selected_target.remove('None')
                    qs = qs.filter(platform__target__isnull=True)
                if selected_target:
                    qs = qs.filter(platform__target__in=selected_target)
            if selected_cycle:
                selected = True
                b =self.saved_dropdown_dict.get('cycle',None)
                if b: b.saved = selected_cycle
                if 'None' in selected_cycle:
                    selected_cycle.remove('None')
                    qs = qs.filter(platform__cycle__isnull=True)
                if selected_cycle:
                    qs = qs.filter(platform__cycle__in=selected_cycle)
            if selected_phase_id:
                selected = True
                b =self.saved_dropdown_dict.get('phase',None)
                if b: b.saved = selected_phase_id
                if 'None' in selected_phase_id:
                    selected_phase_id.remove('None')
                    qs = qs.filter(phase__isnull=True)
                if selected_phase_id:
                    qs = qs.filter(phase__in=selected_phase_id)
            if selected_sku:
                selected = True
                b =self.saved_dropdown_dict.get('sku',None)
                if b: b.saved = selected_sku
                if 'None' in selected_sku:
                    selected_sku.remove('None')
                    qs = qs.filter(sku__isnull=True)
                if selected_sku:
                    qs = qs.filter(sku__in = selected_sku)
            if selected_status_id:
                selected = True
                b =self.saved_dropdown_dict.get('status',None)
                if b: b.saved = selected_status_id
                if 'None' in selected_status_id:
                    selected_status_id.remove('None')
                    qs = qs.filter(status__isnull=True)
                if selected_status_id:
                    qs = qs.filter(status__in=selected_status_id)
            if selected_scrap:
                selected = True
                b =self.saved_dropdown_dict.get('scrap',None)
                if b: b.saved = selected_scrap
                if selected_scrap:
                    qs = qs.filter(scrap__in=selected_scrap)

            if selected_position:
                selected = True
                b =self.saved_dropdown_dict.get('position',None)
                if b: b.saved = selected_position
                if 'None' in selected_position:
                    selected_position.remove('None')
                    qs = qs.filter(position__isnull=True)
                if selected_position:
                    qs = qs.filter(position__in=selected_position)

            selected_sn = request.POST.getlist('selectSn',None)
            selected_sn = list(set(selected_sn))
            selected_sn.remove('')
            if selected_sn :
                selected = True
                qs = qs.filter(sn__in=selected_sn)

            if qs.count() > 20 and selected:
                self.list_per_page = qs.count()
        else:
            if self.saved_dropdown_dict:
                for filter in self.saved_dropdown_dict.values():
                    filter.saved=[]
            self.list_per_page = 20

        return qs

    

    def get_queryset(self, request):
        # initial load UUT
        qs = super().get_queryset(request)

        qs = self.advance_search_dropdown_filter_query(request,qs)

        return qs

    def get_urls(self):
        # add custome url here
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('edit/', self.admin_site.admin_view(self.edit_uuts)),
            path('borrow/', self.admin_site.admin_view(self.borrow_uuts)),
        ]
        custom_urls+=urls
        # print(urls)
        return custom_urls

    class borrow_transfer_form(forms.ModelForm):

        class Meta:
            model = UutBorrowHistory
            fields=['member','purpose']

    def borrow_uuts(self,request):
        if request.user.is_superuser:
            uuts = request.GET.getlist('id')
            form = self.borrow_transfer_form()
            if uuts:
                uuts = Uut.objects.filter(id__in = uuts)

            if request.method=='POST':
                borrowRentRadios = request.POST.get('borrowRentRadios')
                if borrowRentRadios == 'back':
                    self.rent_back_uuts(uuts)
                elif borrowRentRadios == 'borrow':
                    member = request.POST.get('member',None)
                    purpose = request.POST.get('purpose','')
                    self.borrow_or_transfer(member,uuts,purpose)
                
            context = {
                'form':form,
                'uuts':uuts,
            }
            return TemplateResponse(request,'admin/borrow_uut_template.html',context=context)
    
    def borrow_or_transfer(self,member,uuts,purpose):
        
        member = Member.objects.get(pk=member)
        for uut in uuts:
            last_record = uut.uutborrowhistory_set.filter(back_time__isnull=True).last()
            if last_record and last_record.member != member:
                last_record = self.rent_back_uut(uut,last_record)
            if not last_record or last_record.back_time:
                new_record = uut.uutborrowhistory_set.create(
                    member = member,
                    purpose = purpose
                )   
                new_record.save()
                uut.status = UutStatus.objects.get(status_text__icontains='rent')
                uut.save()

    def rent_back_uuts(self,uuts):
        filter_not_borrowed = uuts.filter(uutborrowhistory__isnull=False).filter(uutborrowhistory__back_time__isnull=True)
        for uut in filter_not_borrowed:
            self.rent_back_uut(uut)

    def rent_back_uut(self,uut,record = None):
            last_record = uut.uutborrowhistory_set.last()
            if record :
                last_record = record
            if not last_record.back_time:
                from datetime import datetime
                last_record.back_time = datetime.now()
                uut.status = Uut.status_default
                uut.save()
                last_record.save()
                return last_record
    

    class edit_uut_form(forms.ModelForm):
        # borrower = forms.ModelChoiceField(queryset=Member.objects.all().order_by('usernameincompany'),required=False)
        status = forms.ModelChoiceField(queryset=UutStatus.objects.all().order_by('status_text'),required=False)
        class Meta:
            model = Uut
            fields=['platform','phase','sku','status','scrap','position','cpu','remark']
            # widgets={
            #     'platform':forms.Select(attrs={'class':'form-control'}),
            #     'phase':forms.Select(attrs={'class':'form-control'}),
            #     'sku':forms.TextInput(attrs={'class':'form-control'})
            # }
        

    def edit_uuts(self,request):
        if request.user.is_superuser:
            uuts = request.GET.getlist('id')
            form = self.edit_uut_form()
            if uuts:
                uuts = Uut.objects.filter(id__in = uuts)

            if request.method == 'POST':
                platform = request.POST.get('platform',None)
                phase = request.POST.get('phase',None)
                sku = request.POST.get('sku',None)
                # borrower = request.POST.get('borrower')
                status = request.POST.get('status',None)
                scrap = request.POST.get('scrap',False)
                position = request.POST.get('position',None)
                cpu = request.POST.get('cpu',None)
                remark = request.POST.get('remark',None)
                
                if platform: uuts.update(platform = platform)
                if scrap: uuts.update(scrap = True)
                else: uuts.update(scrap = scrap)
                if phase: uuts.update(phase = phase)
                if sku: uuts.update(sku = sku)
                if status: uuts.update(status = status)
                if position: uuts.update(position = position)
                if cpu: uuts.update(cpu = cpu)
                if remark: uuts.update(remark = remark)

            return TemplateResponse(request,'admin/edit_uut_template.html',context={'uuts':uuts,'form':form})







    



    





    
