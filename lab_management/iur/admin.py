from django.contrib import admin,messages
from django.utils.translation import ngettext
from .models import Uut,Platform,UutBorrowHistory,UutPhase

from django.contrib.auth.models import Group,User
# Register your models here.

admin.site.site_header = 'Lab Admin'
admin.site.site_title  = 'Lab_Admin'
admin.site.enable_nav_sidebar = True

# admin.site.unregister(User)
# admin.site.unregister(Group)

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

    inlines = [
        UutInline,
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
    list_display = ('uut','member','rent_time')
    
    search_fields=('member__name','uut__sn',)

    pass

@admin.register(Uut)
class UutAdmin(admin.ModelAdmin):

    #### settings
    using = 'labpostgres' 

    ###  settings list objects
    # list_max_show_all = 50
    list_per_page = 20
    list_display = ('id','platform','phase','sku','sn','borrower_display','status','scrap','scrap_reason','position','cpu','remark','keyin_time')
    # list_editable = ('position','cpu','remark')
    # list_editable = ('cpu',)
    list_filter = ('phase','scrap','position','status')
    date_hierarchy ='keyin_time'
    list_display_links = ('sn',)
    search_fields = ('sn','platform__codename',)
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
                'phase','platform',
            )
        }),
    )
    


    def colored_phase(self,obj):
        from django.utils.html import format_html
        return format_html(f'<span style="color: blue">{obj.phase}</span>')
    colored_phase.short_description = 'PHASE'
    colored_phase.admin_order_field = 'phase'

    def borrower_display(self,obj):
        borrower = obj.uutborrowhistory_set.filter(back_time__isnull=True)
        if borrower: return borrower.member.name
        return '-'
    borrower_display.short_description = 'Borrower'
    # borrower_display.admin_order_field = 'uutborrowhistory__member__name'

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
    actions = ['mark_scrap','mark_unscrap','make_edit']

    def mark_scrap(self,request,queryset):
        be_updated = queryset.update(scrap = True)
        self.message_user(request,ngettext(f'{be_updated} item was mark scrap',f'{be_updated} items were mark scrap',be_updated),messages.SUCCESS)
    mark_scrap.short_description = 'Scrap'

    def mark_unscrap(self,request,queryset):
        be_updated = queryset.update(scrap = False)
        self.message_user(request,ngettext(f'{be_updated} item was mark unscrap',f'{be_updated} items were mark unscrap',be_updated),messages.SUCCESS)
    mark_unscrap.short_description = 'UnScrap'

    # def make_edit(self,request,queryset,**kwargs):
    #     self.list_editable = ('position','cpu','remark','scrap','status','sku','phase','platform')
    #     self.lookup_allowed()
    # make_edit.short_description = 'Edit UUTs' 


    # custom view

    add_form_template = 'admin/add_uut_template.html'
    def add_view(self, request, form_url='', extra_context=None):
        form = self.get_form(request,obj = None,change=False)
        return super().add_view(request, form_url=form_url, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        if request.method == 'POST' and 'uut-save' in request.POST:
            sn_list = request.POST.getlist('sn')
            sku_list = request.POST.getlist('sku')
            position_list = request.POST.getlist('position')
            for sn,sku,position in zip(sn_list,sku_list,position_list):
                Uut.objects.create(sn = sn,sku=sku,position=position,phase = obj.phase,platform=obj.platform)
            self.message_user(request,f'{len(sn_list)} uut be added.',messages.SUCCESS)
            return
        return super().save_model(request, obj, form, change)
    change_list_template = 'admin/uut_changelist_template.html'

    def get_search_results(self,request,queryset,term):
        qs ,use_distinct = super().get_search_results(request,queryset,term)
        qs |= qs.uutborrowhistory_set.filter(member__name=term).filter(back_time__isnull=True)
        return qs,use_distinct
        




    
