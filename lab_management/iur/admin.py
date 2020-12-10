import re
from typing import List
from O365.utils import token
from O365 import Account
from django import forms
from django.contrib import admin,messages
from django.contrib.auth.models import Group,User
from django.forms import widgets
from django.http import request
from django.http.request import HttpRequest
from django.utils.html import format_html
from django.utils.translation import ngettext
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse
from django.db.models import Q,Count
from django.core.files.uploadhandler import MemoryFileUploadHandler,TemporaryFileUploadHandler
from django.core.files.storage import FileSystemStorage
from .models import Uut,Platform,UutBorrowHistory,UutPhase,Member,UutStatus,PlatformPhase,PlatformConfig


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
    list_display = ['id','usernameincompany','email']
    search_fields = ('usernameincompany',)
    

@admin.register(UutPhase)
class UutPhaseAdmin(admin.ModelAdmin):
    list_display=['id','phase_text']
    search_fields=['phase_text']
    

class UutInline(admin.TabularInline):
    model = Uut
    extra = 2
    fieldsets = (
        (None, {
            "fields": (
                'platform_phase','sn','sku','cpu','position','status',
            ),
            
        }),
    )
@admin.register(PlatformConfig)
class PlatformConfigAdmin(admin.ModelAdmin):
    list_display=('id','config_name','config_url')
    search_fields=('config_name',)

@admin.register(PlatformPhase)
class PlatformPhaseAdmin(admin.ModelAdmin):
    list_display=['id','platform','phase','config']
    list_editable = ['platform','phase','config']

    search_fields=['platform__codename']
    list_select_related =  ('platform','phase')
    autocomplete_fields = ['platform','phase','config']

class PlatformPhaseInline(admin.TabularInline):
    model = PlatformPhase
    extra = 2
    autocomplete_fields = ('config',)
    fieldsets = (
        (None, {
            "fields": (
                'phase','config'
            ),
            
        }),
    )
    

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    search_fields = ('codename','marketing_name')
    list_filter = ('series','codename')
    list_display = ('codename','chipset','group','target','cycle','series','marketing_name','odm')

    inlines = [
        PlatformPhaseInline
    ]

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
    list_display = ('id','platform_with_link','uut_phase','platform_target','platform_group','sku','sn','borrower_display','status','scrap','position','cpu','remark','keyin_time')
    # list_editable = ('position','cpu','remark')
    list_filter = ('scrap','uutborrowhistory__rent_time','status','platform_phase__phase','platform_phase__platform__group','platform_phase__platform__target','position')
    date_hierarchy ='keyin_time'
    list_display_links = ('sn',)
    search_fields = ('sn','platform_phase__platform__codename','uutborrowhistory__member__usernameincompany')

    show_full_result_count = True
    # radio_fields = {"phase":admin.VERTICAL}

    ###  setting change list
    # raw_id_fields = ('platform',)
    # list_select_related =  ('platform',)
    autocomplete_fields = ['platform_phase',]
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
                'platform_phase','status'
            )
        }),
    )


    def borrower_display(self,obj):
        borrower = obj.uutborrowhistory_set.filter(back_time__isnull=True).first()
        if borrower: 
            template = f'{borrower.member.usernameincompany}<br><small style="color:gray;">{borrower.rent_time}</small>'
            return format_html(template)
        return '-'
    borrower_display.short_description = 'BORROWER'

    def platform_with_link(self,obj):
        if obj.platform_phase.platform:
            template = f'<b><a href="/iur/platform/{obj.platform_phase.platform.id}/change/">{obj.platform_phase.platform.codename}</a></b>'
            return format_html(template)
        else:
            return '-'
    platform_with_link.short_description='PLATFORM'
    platform_with_link.admin_order_field='platform_phase__platform'


    # actions

    actions = ['mark_scrap','mark_unscrap','return_back','return_8F','edit_uuts_action','borrow_and_transfer_action','machine_arrive_action']

    def mark_scrap(self,request,queryset):
        if request.user.is_superuser:
            be_updated = queryset.update(scrap = True,status=UutStatus.SCRAP())
            self.message_user(request,ngettext(f'{be_updated} item was mark scrap',f'{be_updated} items were mark scrap',be_updated),messages.SUCCESS)
    mark_scrap.short_description = 'Scrap'

    def mark_unscrap(self,request,queryset):
        if request.user.is_superuser:
            be_updated = queryset.update(scrap = False,status=UutStatus.KEEPON)
            self.message_user(request,ngettext(f'{be_updated} item was mark unscrap',f'{be_updated} items were mark unscrap',be_updated),messages.SUCCESS)
    mark_unscrap.short_description = 'UnScrap'

    def return_back(self,request,queryset):
        if request.user.is_superuser:
            r_records = self.rent_back_uuts(queryset)
            self.send_rent_borrowed_mail(return_records=r_records)
    return_back.short_description = 'Return'

    def return_8F(self,request,queryset):
        if request.user.is_superuser:
            queryset.update(status = UutStatus.RETURN8F())
    return_8F.short_description = 'Return 8F'

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

    def machine_arrive_action(self,request,queryset):
        # self.list_editable = ()
        if request.user.is_superuser:
            if queryset:
                ids = '&'.join([ f'id={q.id}' for q in queryset])
                return HttpResponseRedirect(f'machine_arrive/?{ids}')
    machine_arrive_action.short_description = 'Send Machine Arrive Mail'

    # custom view

    add_form_template = 'admin/add_uut_template.html'

    class add_uut_form(forms.ModelForm):
        platform = forms.ModelChoiceField(queryset=Platform.objects.all().order_by('codename'),required=False)
        phase = forms.ModelChoiceField(queryset=UutPhase.objects.all().order_by('phase_text'),required=False)
        config_name = forms.CharField()
        config_url = forms.URLField()
        class Meta:
            model = Uut
            fields=['platform','phase','config_name','config_url']

    def add_view(self, request):
        form = self.add_uut_form()
        return super().add_view(request,extra_context={'form':form})

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
                    u = uut.uutborrowhistory_set.filter(member__usernameincompany__search=term).filter(back_time__isnull=True).first()
                    if not u:
                        _qs = _qs.exclude(sn=uut.sn)
            return _qs
        qs ,use_distinct = super().get_search_results(request,queryset,term)

        if term:            
            qs = exclude_borrower_has_returned_uut(qs,term)
        return qs,use_distinct

    saved_dropdown_dict = dict()

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

    def advance_search_dropdown_filter(self,qs):
        platform = qs.order_by('platform_phase__platform__codename').values_list('platform_phase__platform__id','platform_phase__platform__codename').distinct()
        platform = self.Dropdown('Platform',platform)
        self.saved_dropdown_dict.update({'platform':platform})

        borrower = qs.order_by('uutborrowhistory__member__usernameincompany').filter(Q(uutborrowhistory__back_time__isnull=True)).values_list('uutborrowhistory__member','uutborrowhistory__member__usernameincompany').distinct()
        borrower = self.Dropdown('Borrower',borrower)
        self.saved_dropdown_dict.update({'borrower':borrower})

        group = qs.values_list('platform_phase__platform__group','platform_phase__platform__group').distinct()
        group = self.Dropdown('Group',group)
        self.saved_dropdown_dict.update({'group':group})

        target = qs.order_by('platform_phase__platform__target').values_list('platform_phase__platform__target','platform_phase__platform__target').distinct()
        target = self.Dropdown('Target',target)
        self.saved_dropdown_dict.update({'target':target})

        cycle = qs.order_by('platform_phase__platform__cycle').values_list('platform_phase__platform__cycle','platform_phase__platform__cycle').distinct()
        cycle = self.Dropdown('Cycle',cycle)
        self.saved_dropdown_dict.update({'cycle':cycle})

        phase = qs.order_by('platform_phase__phase__phase_text').values_list('platform_phase__phase__id','platform_phase__phase__phase_text').distinct()
        phase = self.Dropdown('Phase',phase)
        self.saved_dropdown_dict.update({'phase':phase})

        sku = qs.order_by('sku').values_list('sku','sku').distinct()
        sku = self.Dropdown('SKU',sku)
        self.saved_dropdown_dict.update({'sku':sku})

        status = qs.order_by('status__status_text').values_list('status','status__status_text').distinct()
        status = self.Dropdown('Status',status)
        self.saved_dropdown_dict.update({'status':status})

        scrap = qs.values_list('scrap','scrap').distinct()
        scrap = self.Dropdown('Scrap',scrap,[False,])
        self.saved_dropdown_dict.update({'scrap':scrap})

        position = qs.order_by('position').values_list('position','position').distinct()
        position = self.Dropdown('Position',position)
        self.saved_dropdown_dict.update({'position':position})
        
        return [platform,borrower,phase,group,target,cycle,sku,status,scrap,position]

    saved_actions = []
    def changelist_view(self, request, extra_context=None):
        
        if not request.user.is_superuser:
            if not self.saved_actions:
                self.saved_actions = self.actions
                self.actions=None
        else:
            if not self.actions:
                self.actions = self.saved_actions
                self.saved_actions = None
        
        qs = self.get_queryset(request)
        
        dropdown = self.advance_search_dropdown_filter(qs)
        extra_context = dropdown={'dropdown':dropdown}
        changelist_view = super().changelist_view(request, extra_context)
        if hasattr(changelist_view,'context_data'):
            changelist_view.context_data['title'] = 'IUR'

        return changelist_view
    
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
                qs = qs.filter(platform_phase__platform__in=selected_platform_id)

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
                    qs = qs.filter(platform_phase__=True)
                if selected_phase_id:
                    qs = qs.filter(platform_phase__phase__in=selected_phase_id)
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
            if '' in selected_sn:
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
            path('machine_arrive/', self.admin_site.admin_view(self.machineArrive)),
            # path('sign_in/',self.admin_site.admin_view(self.auth_Office_step_one)),
            # path('sign_in_/',self.admin_site.admin_view(self.auth_Office_step_two)),
        ]
        custom_urls+=urls
        # print(custom_urls)
        return custom_urls

    scopes = ['basic','message_all']
    saved_state = None
    @property
    def get_365_account(self):

        from O365 import FileSystemTokenBackend,MSOffice365Protocol,MSGraphProtocol,Connection
        import json
        token_backend = FileSystemTokenBackend(token_path='.',token_filename='o365_token.txt')
        credentials = tuple()
        with open('credentials.json','r') as f:
             data = json.load(f)
             credentials = (data['appid'],data['secret'])
        protocal   = MSGraphProtocol(api_version='beta')
        account = Account(credentials,token_backend = token_backend,protocol=protocal)
        return account

    def save_attachments_to_cloud(self,attachments) :
        '''
        save attachments to default onedrive and return list of urls
        '''
        att_files=[]
        root_folder = self.get_365_account.storage().get_default_drive().get_root_folder()
        # get Attachment folder
        attachment_folder = None
        for f in root_folder.get_items():
            if 'Attachments' in f.name:
                attachment_folder = f
                break
        else:
            if not attachment_folder:
                attachment_folder = root_folder.create_child_folder('Attachments')
        
        for att in attachments:
            att_files.append(attachment_folder.upload_file(att))
            # att_urls.append(f.share_with_link(share_scope='organization').share_link)
            

        return att_files

    def send_test_mail(self,account):
        try:
            m = account.new_message()
            m.to.add('david.tsai@hp.com')
            m.subject = 'Testing!'
            m.body = "Send Mail success"
            
            m.send()
        except Exception as e:
            print(e)



    def send_mail(self,to,cc=None,subject='',body='',attachments:list=None):
        mail = self.get_365_account.new_message()
        mail.to.add(to)
        mail.body=body
        mail.subject = subject
        if cc:
            mail.cc.add(cc)
        if attachments:
            mail.attachments.add(attachments)
        return mail.send()


    def send_rent_borrowed_mail(self,to=None,borrow_records=None,return_records=None,cc=None,message:str='',attachments:list=None):
        from django.template.loader import get_template
        from django.template import Context

        template = get_template('admin/mail_template.html')

        if return_records:
            return_member =  Member.objects.filter(id__in=return_records.values_list('member'))
            if to:
                to |= return_member
            else:
                to = return_member
        att_files = [ (file.name,file.share_with_link(share_scope='organization').share_link) for file in self.save_attachments_to_cloud(attachments)] if attachments else None
        attachments = None

        context = {
                    'receiver':'  '.join([t.usernameincompany for t in to]),
                    'message':message,
                    'borrow_records':borrow_records,
                    'return_records':return_records,
                    'sender':self.get_365_account.get_current_user().full_name,
                    'att_files':att_files
                }
        
        body = template.render(context)
        

        subject = "IUR record update"
        if cc:
            cc = list(cc.values_list('user__email',flat=True))
        if to:
            to = list(to.values_list('user__email',flat=True))
        return self.send_mail(to,cc,subject,body)

    def send_machine_arrived_mail(self,uuts,to,message:str='',attachments:list=None):
        from django.template.loader import get_template
        from django.template import Context
        arrive_uuts = self.arrive_uuts_classify(uuts)
        platform_phase_subject = uuts.values('platform_phase__platform__codename','platform_phase__phase__phase_text').distinct()
        platform_phase_subject = ' '.join([f"【{i['platform_phase__platform__codename']} {i['platform_phase__phase__phase_text']}】" for i in platform_phase_subject])
        template = get_template('admin/mail_machine_arrive_template.html')
        config_urls = uuts.values('platform_phase__config__config_name','platform_phase__config__config_url').distinct()
        att_files = [ (file.name,file.share_with_link(share_scope='organization').share_link) for file in self.save_attachments_to_cloud(attachments)] if attachments else None
        attachments = None
        context = {
                    'arrive_uuts':arrive_uuts,
                    'message':message,
                    'sender':self.get_365_account.get_current_user().full_name,
                    'config_urls':config_urls,
                    'att_files':att_files
                }
        
        body = template.render(context)
        
        

        subject = f"Machines arrived {platform_phase_subject}"

        return self.send_mail(to,None,subject,body,attachments)
            
    # def auth_Office_step_one(self,request):

    #     # callback = 'http://127.0.0.1:8000/iur/uut/sign_in_/'




    #     # account = Account(credentials=self.credentials)
    #     # url,state = account.con.get_authorization_url(requested_scopes=self.scopes,redirect_uri=callback)
    #     # self.saved_state = state
    #     # print(state)

    #     # print(url)
    #     return redirect('http://127.0.0.1:8000/iur/uut/')



    # def auth_Office_step_two(self):
    #     account = Account(credentials=self.credentials)
    #     callback = 'http://127.0.0.1:8000/iur/uut/sign_in_/'
    #     state = self.saved_state
    #     result = account.con.request_token(None,state,callback)
    #     print(result)
    #     if result:
    #         redirect( 'http://127.0.0.1:8000/iur/uut/')
    

    def arrive_uuts_classify(self,uuts):

        types = list(uuts.values_list('platform_phase__platform__group','platform_phase__platform__target').distinct())
        arrived_uuts=list()
        for group,target in types:
            t = group+' '+target
            selected_uuts = uuts.filter(Q(platform_phase__platform__group=group)&Q(platform_phase__platform__target=target))
            selected_uuts = selected_uuts.values_list('platform_phase__platform','platform_phase__phase','sku').order_by('platform_phase__platform','platform_phase__phase','sku').annotate(sku_cnt=Count('sku'))
            selected_uuts = [{'platform':Platform.objects.get(pk=uut[0]),'phase':UutPhase.objects.get(pk=uut[1]),'sku':uut[2],'qty':uut[3]} for uut in selected_uuts]
            
            arrived_uuts.append({
                'name':t,
                'uuts':selected_uuts
            })
        return arrived_uuts

    def machineArrive(self,request):
        if request.user.is_superuser:
            uuts = request.GET.getlist('id',None)

            if uuts:
                uuts = Uut.objects.filter(id__in = uuts)
                arrive_uuts = self.arrive_uuts_classify(uuts)
                context = {
                    'arrive_uuts':arrive_uuts,
                }

                if request.method =='POST':
                    mail_message = request.POST.get('mail_message','')
                    attachments = []
                    if request.FILES:
                        upload_file = request.FILES['attachment']
                        fs = FileSystemStorage()
                        saved_name = fs.save(upload_file.name,upload_file)
                        import os
                        attachments = [os.path.join(fs.location,saved_name)]
                    # to = ['cmitcommsw@hp.com','stevencommshwall@hp.com','commspms@hp.com']
                    to=['david.tsai@hp.com']
                    self.send_machine_arrived_mail(uuts,to,mail_message,attachments)

                return TemplateResponse(request,'admin/machine_arrive_template.html',context)


    class borrow_transfer_form(forms.ModelForm):
        class Meta:
            model = UutBorrowHistory
            fields=['member','purpose']
            widgets={
                'attachment':forms.FileInput(attrs={'class':'custom-file-input'})
            }

    def borrow_uuts(self,request):
        if request.user.is_superuser:
            uuts = request.GET.getlist('id')
            form = self.borrow_transfer_form()
            cc = self.Dropdown('CC',Member.objects.all().values_list('id','usernameincompany'))
            if uuts:
                uuts = Uut.objects.filter(id__in = uuts)

            if request.method=='POST':
                borrowRentRadios = request.POST.get('borrowRentRadios')
                
                if borrowRentRadios == 'back':
                    r_records = self.rent_back_uuts(uuts)
                    self.send_rent_borrowed_mail(return_records=r_records)
                elif borrowRentRadios == 'borrow':
                    attachments = []
                    if request.FILES:
                        upload_file = request.FILES['attachment']
                        fs = FileSystemStorage()
                        saved_name = fs.save(upload_file.name,upload_file)
                        import os
                        attachments = [os.path.join(fs.location,saved_name)]
                        print(attachments)
                    member = Member.objects.filter(id = request.POST.get('member',None))
                    purpose = request.POST.get('purpose','')
                    mail_cc = request.POST.getlist('selectCC',None)
                    if mail_cc:
                        mail_cc = Member.objects.filter(id__in=mail_cc)
                    mail_message = request.POST.get('mail_message','')
                    b_records,r_records = self.borrow_or_transfer(member[0],uuts,purpose)
                    self.send_rent_borrowed_mail(member,b_records,r_records,mail_cc,mail_message,attachments)

                    ## ajax
                    # if self.send_borrowed_mail(member,mail_cc,mail_message):
                    # ajax.back(result)
                
            context = {
                'form':form,
                'uuts':uuts,
                'cc':cc
            }
            return TemplateResponse(request,'admin/borrow_uut_template.html',context=context)
    
    def borrow_or_transfer(self,member,uuts,purpose):
        borrow_records=UutBorrowHistory.objects.none()
        return_records=UutBorrowHistory.objects.none()
        for uut in uuts:
            last_record = uut.uutborrowhistory_set.filter(back_time__isnull=True).first()
            if last_record and last_record.member != member:
                last_record = self.rent_back_uut(uut,last_record)
                return_records |= UutBorrowHistory.objects.filter(pk = last_record.id)
            if not last_record or last_record.back_time:
                new_record = uut.uutborrowhistory_set.create(
                    member = member,
                    purpose = purpose
                )   
                borrow_records |= UutBorrowHistory.objects.filter(pk=new_record.id)
                new_record.save()
                uut.status = UutStatus.objects.get(status_text__icontains='rent')
                uut.save()
        return borrow_records,return_records

    def rent_back_uuts(self,uuts):
        records = UutBorrowHistory.objects.none()
        filter_not_borrowed = uuts.filter(uutborrowhistory__isnull=False).filter(uutborrowhistory__back_time__isnull=True).distinct()
        for uut in filter_not_borrowed:
            record = self.rent_back_uut(uut)
            if record:
                records |= UutBorrowHistory.objects.filter(pk=record.id)
        return records

    def rent_back_uut(self,uut,record = None):
        last_record = uut.uutborrowhistory_set.filter(back_time__isnull=True).first()
        if record :
            last_record = record
        if not last_record.back_time:
            from datetime import datetime
            last_record.back_time = datetime.now()
            uut.status = UutStatus.KEEPON()
            uut.save()
            last_record.save()
            return last_record
    

    class edit_uut_form(forms.ModelForm):
        # borrower = forms.ModelChoiceField(queryset=Member.objects.all().order_by('usernameincompany'),required=False)
        status = forms.ModelChoiceField(queryset=UutStatus.objects.all().order_by('status_text'),required=False)
        platform = forms.ModelChoiceField(queryset=Platform.objects.all().order_by('codename'),required=False)
        phase = forms.ModelChoiceField(queryset=UutPhase.objects.all().order_by('phase_text'),required=False)
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
                
                for uut in uuts:
                    
                    if platform:
                        p = Platform.objects.get(id=platform)
                        pp,ppCreated = PlatformPhase.objects.get_or_create(platform = p,phase = uut.platform_phase.phase)
                        uut.platform_phase = pp
                    if phase: 
                        p = UutPhase.objects.get(id=phase)
                        pp,ppCreated = PlatformPhase.objects.get_or_create(platform = uut.platform_phase.platform,phase = p)
                        uut.platform_phase = pp
                    uut.scrap = True if scrap else uut.scrap
                    uut.sku = sku if sku else uut.sku
                    uut.status = UutStatus.objects.get(pk=status) if status else uut.status
                    uut.position = position if position else uut.position
                    uut.cpu = cpu if cpu else uut.cpu
                    uut.remark = remark if remark else uut.remark
                    uut.save()

            return TemplateResponse(request,'admin/edit_uut_template.html',context={'uuts':uuts,'form':form})

    
