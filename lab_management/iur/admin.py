from django.contrib import admin,messages
from django.utils.translation import ngettext
from .models import Uut,Platform
# Register your models here.

class PlatformInline(admin.TabularInline):
    model = Platform
    extra = 3

@admin.register(Uut)
class UutAdmin(admin.ModelAdmin):

    # settings
    using = 'labpostgres' 

    list_display = ('id','platform_id','sn','sku','cpu','phase','status','scrap','scrap_reason','remark','position','keyin_time')
    date_hierarchy ='keyin_time'
    # list_display_links = ('cpu','position')
    search_fields = ('id','sn','sku','cpu','phase','status','scrap','scrap_reason','remark','position','keyin_time',)
    readonly_fields = ('sn',)
    fieldsets = (
        ('UUT info', {
            "fields": (
                'sn','sku','cpu','phase',
            ),
        }),
        ('STORAGE info', {
            "fields": (
                'status','position',
            ),
            # "classes":('wide','extrapretty'),
            "classes":('collapse',),
            "description":'<code> UUT storage information </code>',
        }),
    )
    
    # fields = (('sn','sku','cpu','phase'),'status','scrap',('keyin_time'))
    # list_editable = ('scrap_reason','remark','scrap','position')
    list_filter = ('phase','scrap','position',)

    # fields = [field.name for field in Uut._meta.get_fields()]
    # list_display = [field.name for field in Uut._meta.get_fields()]
    actions = ['mark_scrap','mark_unscrap']
    
    def colored_phase(self,obj):
        from django.utils.html import format_html
        return format_html(f'<span style="color: blue">{obj.phase}</span>')
    colored_phase.short_description = 'PHASE'
    colored_phase.admin_order_field = 'phase'

    #override
    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using).select_related('platform').order_by('-keyin_time')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

    # actions
    def mark_scrap(self,request,queryset):
        be_updated = queryset.update(scrap = True)
        self.message_user(request,ngettext(f'{be_updated} item was mark scrap',f'{be_updated} items were mark scrap',be_updated),messages.SUCCESS)
    mark_scrap.short_description = 'Scrap'

    def mark_unscrap(self,request,queryset):
        be_updated = queryset.update(scrap = False)
        self.message_user(request,ngettext(f'{be_updated} item was mark unscrap',f'{be_updated} items were mark unscrap',be_updated),messages.SUCCESS)
    mark_unscrap.short_description = 'UnScrap'


    
