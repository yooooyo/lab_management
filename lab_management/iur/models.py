# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models

class Member(models.Model):
    usernameincompany = models.CharField(max_length=100)
    user = models.OneToOneField(User, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'member'

    def __str__(self) -> str:
        return self.usernameincompany

    def email(self):
        return self.user.email

class UutStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    status_text = models.CharField(unique=True, max_length=30, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'uut_status'

    def __str__(self) -> str:
        return self.status_text

    @classmethod
    def KEEPON(self):
        obj,created = self.objects.get_or_create(status_text='Keep On')
        return obj
    
    @classmethod
    def RENT(self):
        obj,created = self.objects.get_or_create(status_text='Rent')
        return obj

    @classmethod
    def Return8F(self):
        obj,created = self.objects.get_or_create(status_text='Return 8F')
        return obj

class Ap(models.Model):
    id = models.BigAutoField(primary_key=True)
    no = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    vender = models.CharField(max_length=50, blank=True, null=True)
    adapter = models.CharField(max_length=50)
    storage = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    cycle = models.CharField(max_length=50, blank=True, null=True)
    cpu = models.CharField(max_length=50, blank=True, null=True)
    chip1 = models.CharField(max_length=100, blank=True, null=True)
    chip1_protocols = models.CharField(max_length=50, blank=True, null=True)
    chip2 = models.CharField(max_length=100, blank=True, null=True)
    chip2_protocols = models.CharField(max_length=50, blank=True, null=True)
    network_technology_standard = models.CharField(max_length=50, blank=True, null=True)
    admin_id = models.CharField(max_length=50, blank=True, null=True)
    admin_pw = models.CharField(max_length=50, blank=True, null=True)
    ssid_2d4 = models.CharField(max_length=50)
    ssid_2d4_password = models.CharField(max_length=50)
    ssid_2d4_bssid = models.CharField(max_length=50, blank=True, null=True)
    ssid_2d4_band = models.CharField(max_length=50, blank=True, null=True)
    ssid_5 = models.CharField(max_length=50, blank=True, null=True)
    ssid_5_password = models.CharField(max_length=50, blank=True, null=True)
    ssid_5_bssid = models.CharField(max_length=50, blank=True, null=True)
    ssid_5_band = models.CharField(max_length=50, blank=True, null=True)
    fw = models.CharField(max_length=100, blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_scrap = models.BooleanField(default=False)
    class Meta:
        managed = False
        db_table = 'ap'


class ApBorrowHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    ap = models.ForeignKey(Ap, models.DO_NOTHING)
    borrower = models.ForeignKey(Member, models.DO_NOTHING)
    rent_time = models.DateTimeField()
    back_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ap_borrow_history'


# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=150)

#     class Meta:
#         managed = False
#         db_table = 'auth_group'


# class AuthGroupPermissions(models.Model):
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#     permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_group_permissions'
#         unique_together = (('group', 'permission'),)


# class AuthPermission(models.Model):
#     name = models.CharField(max_length=255)
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
#     codename = models.CharField(max_length=100)

#     class Meta:
#         managed = False
#         db_table = 'auth_permission'
#         unique_together = (('content_type', 'codename'),)


# class AuthUser(models.Model):
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.BooleanField(default=False)
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         managed = False
#         db_table = 'auth_user'


# class AuthUserGroups(models.Model):
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_user_groups'
#         unique_together = (('user', 'group'),)


# class AuthUserUserPermissions(models.Model):
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_user_user_permissions'
#         unique_together = (('user', 'permission'),)




# class DjangoAdminLog(models.Model):
#     action_time = models.DateTimeField()
#     object_id = models.TextField(blank=True, null=True)
#     object_repr = models.CharField(max_length=200)
#     action_flag = models.SmallIntegerField()
#     change_message = models.TextField()
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'django_admin_log'


# class DjangoContentType(models.Model):
#     app_label = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)

#     class Meta:
#         managed = False
#         db_table = 'django_content_type'
#         unique_together = (('app_label', 'model'),)


# class DjangoMigrations(models.Model):
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'django_migrations'


# class DjangoSession(models.Model):
#     session_key = models.CharField(primary_key=True, max_length=40)
#     session_data = models.TextField()
#     expire_date = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'django_session'


class Driver(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50,blank=True,null=True)
    package_name = models.TextField(unique=True, blank=True, null=True)
    version = models.CharField(max_length=50)
    release_time = models.TimeField()
    category = models.CharField(max_length=50, blank=True, null=True)
    path = models.FileField(upload_to='uploads/driver/',null=True,blank=True)
    owner = models.ForeignKey(Member, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'driver'


class Module(models.Model):
    id = models.BigAutoField(primary_key=True)
    deliverable_name = models.TextField(blank=True,null=True)
    short_name = models.CharField(max_length=50)
    vender_id = models.CharField(max_length=50, blank=True, null=True)
    device_id = models.CharField(max_length=50, blank=True, null=True)
    subsys_device_id = models.CharField(max_length=50, blank=True, null=True)
    subsys_vender_id = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    owner = models.ForeignKey(Member, models.DO_NOTHING)
    support_driver = ArrayField(base_field=models.BigIntegerField(),null=True)

    class Meta:
        managed = True
        db_table = 'module'
    



class Platform(models.Model):
    GROUP_CHOICE = [
        ('COMMERICAL','Commerical'),
        ('CONSUMER','Consumer'),
    ]
    TARGET_CHOICE = [
        ('NB','Notebook'),
        ('DT','Desktop'),
        ('AIO','ALL in one'),
    ]
    id = models.BigAutoField(primary_key=True)
    update_time = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=100, blank=True, null=True)
    behavior = models.CharField(max_length=100, blank=True, null=True)
    codename = models.CharField(max_length=200, blank=True, null=True)
    group = models.CharField(max_length=50, blank=True, null=True,choices=GROUP_CHOICE)
    target = models.CharField(max_length=50, blank=True, null=True,choices=TARGET_CHOICE)
    development_center = models.CharField(max_length=200, blank=True, null=True)
    cycle = models.CharField(max_length=50, blank=True, null=True)
    forecast_cycle = models.CharField(max_length=50, blank=True, null=True)
    series = models.CharField(max_length=200, blank=True, null=True)
    forecast_series = models.CharField(max_length=200, blank=True, null=True)
    chipset = models.CharField(max_length=200, blank=True, null=True)
    marketing_name = models.CharField(max_length=200, blank=True, null=True)
    odm = models.CharField(max_length=50, blank=True, null=True)
    sepm = models.CharField(max_length=50, blank=True, null=True)
    pdm = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'platform'

    def __str__(self) -> str:
        return self.codename


class PlatformConfig(models.Model):
    id = models.BigAutoField(primary_key=True)
    config_name = models.CharField(max_length=50)
    config_url = models.URLField(max_length=200)

    class Meta:
        managed = True
        db_table = 'platform_config'

    def __str__(self) -> str:
        return self.config_name

class UutPhase(models.Model):
    id = models.BigAutoField(primary_key=True)
    phase_text = models.CharField(unique=True, max_length=30, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'uut_phase'

    def __str__(self) -> str:
        return self.phase_text

class PlatformPhase(models.Model):
    phase = models.ForeignKey(UutPhase, models.DO_NOTHING)
    platform = models.ForeignKey(Platform, models.DO_NOTHING)
    config = models.ForeignKey(PlatformConfig, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'platform_phase'
        unique_together = (('platform', 'phase'),)
        ordering = ['platform__codename']


    def __str__(self) -> str:
        return f'{self.platform.codename} - {self.phase.phase_text}'

    

class Tool(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    version = models.CharField(max_length=50, blank=True, null=True)
    path = models.FileField(upload_to='uploads/tool/',null=True,blank=True)

    class Meta:
        managed = True
        db_table = 'tool'


class Script(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField(unique=True)
    wwan = models.BooleanField(default=False)
    wlan = models.BooleanField(default=False)
    bt = models.BooleanField(default=False)
    lan = models.BooleanField(default=False)
    rfid = models.BooleanField(default=False)
    nfc = models.BooleanField(default=False)
    path = models.FileField(upload_to='uploads/scripts/',null=True,blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    version = models.CharField(max_length=50, blank=True, null=True)
    tool = models.ForeignKey(Tool, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'script'




class Uut(models.Model):
    id = models.BigAutoField(primary_key=True)
    sn = models.CharField(unique=True, max_length=50)
    sku = models.CharField(max_length=50, blank=True, null=True)
    cpu = models.CharField(max_length=50, blank=True, null=True)
    status = models.ForeignKey(UutStatus, models.DO_NOTHING, blank=True, null=True,default=UutStatus.KEEPON())
    scrap_reason = models.TextField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    scrap = models.BooleanField(default=False)
    keyin_time = models.DateTimeField(blank=True, null=True)
    platform_phase = models.ForeignKey(PlatformPhase, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'uut'

    def __str__(self) -> str:
        return self.sn

    @property
    def platform(self):
        return self.platform_phase.platform.codename

    @property
    def borrower(self):
        unreturn_history = self.uutborrowhistory_set.filter(back_time__isnull=True)
        return '-' if not unreturn_history.count() else unreturn_history.order_by('-rent_time').first().member.usernameincompany
    

    def platform_name(self):
        return self.platform_phase.platform.codename
    platform_name.short_description = 'platform'
    platform_name.admin_order_field = 'platform__codename'

    def platform_group(self):
        return self.platform_phase.platform.group
    platform_group.short_description = 'group'

    def platform_target(self):
        return self.platform_phase.platform.target
    platform_target.short_description = 'target'

    def platform_cycle(self):
        return self.platform_phase.platform.cycle
    platform_cycle.short_description = 'cycle'
    platform_cycle.admin_order_field = 'platform__cycle'

    def uut_phase(self):
        return self.platform_phase.phase.phase_text
    uut_phase.short_description = 'phase'


class UutBorrowHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    rent_time = models.DateTimeField(auto_now_add=True)
    back_time = models.DateTimeField(blank=True, null=True)
    purpose = models.TextField(blank=True, null=True)
    member = models.ForeignKey(Member, models.DO_NOTHING, blank=True, null=True)
    uut = models.ForeignKey(Uut, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'uut_borrow_history'


    def uut_phase(self):
        return self.platform_phase.phase.phase_text
    uut_phase.short_description = 'phase'