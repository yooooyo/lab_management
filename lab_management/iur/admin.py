from django.contrib import admin,messages
from django.utils.translation import ngettext
from .models import Uut,Platform,UutBorrowHistory,UutPhase
from django.db import models as djmodels
# Register your models here.

@admin.register(UutPhase)
class UutPhaseAdmin(admin.ModelAdmin):
    pass

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    search_fields = ('codename',)
    list_filter = ('codename',)
    list_display = ('series','group','marketing_name','codename')

    # fieldsets = (
    #     ('Solid info', {
    #         "fields": (
    #             'codename','sku','phase','platform',
    #         ),
    #     }),
    #     ('Plan info', {
    #         "fields": (
    #             'status','position',
    #         ),
    #         # "classes":('wide','extrapretty'),
    #         # "classes":('collapse',),
    #         # "description":'<code> UUT storage information </code>',
    #     }),
    # )

@admin.register(UutBorrowHistory)
class UutBorrowHistoryAdmin(admin.ModelAdmin):

    pass

@admin.register(Uut)
class UutAdmin(admin.ModelAdmin):

    #### settings
    using = 'labpostgres' 

    ###  settings list objects
    # list_max_show_all = 50
    list_per_page = 200
    list_display = ('id','platform','phase','sku','sn','borrower_display','status','scrap','scrap_reason','position','cpu','remark','keyin_time')
    list_editable = ('position','cpu','remark')
    list_filter = ('phase','scrap','position')
    date_hierarchy ='keyin_time'
    list_display_links = ('sn',)
    search_fields = ('id','sn','sku','cpu','status','scrap_reason','remark','position','platform__codename','uutborrowhistory__member__name')
    show_full_result_count = True


    ###  setting change list
    # raw_id_fields = ('platform',)
    list_select_related =  ('platform',)
    autocomplete_fields = ['platform',]
    # readonly_fields = ('sn',)
    fieldsets = (
        ('UUT info', {
            "fields": (
                'sn','sku','phase','platform',
            ),
        }),
        ('STORAGE info', {
            "fields": (
                'status','position',
            ),
            # "classes":('wide','extrapretty'),
            # "classes":('collapse',),
            # "description":'<code> UUT storage information </code>',
        }),
    )
    
    actions = ['mark_scrap','mark_unscrap']
    
    def colored_phase(self,obj):
        from django.utils.html import format_html
        return format_html(f'<span style="color: blue">{obj.phase}</span>')
    colored_phase.short_description = 'PHASE'
    colored_phase.admin_order_field = 'phase'

    def borrower_display(self,obj):
        borrower = obj.uutborrowhistory_set.last()
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
    def mark_scrap(self,request,queryset):
        be_updated = queryset.update(scrap = True)
        self.message_user(request,ngettext(f'{be_updated} item was mark scrap',f'{be_updated} items were mark scrap',be_updated),messages.SUCCESS)
    mark_scrap.short_description = 'Scrap'

    def mark_unscrap(self,request,queryset):
        be_updated = queryset.update(scrap = False)
        self.message_user(request,ngettext(f'{be_updated} item was mark unscrap',f'{be_updated} items were mark unscrap',be_updated),messages.SUCCESS)
    mark_unscrap.short_description = 'UnScrap'

    


    
