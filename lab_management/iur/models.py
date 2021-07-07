# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.contrib.auth.models import User

from django.db import models

class Member(models.Model):
    usernameincompany = models.CharField(max_length=100)
    user = models.OneToOneField(User, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'member'
        ordering=['usernameincompany']

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
    def RETURN8F(self):
        obj,created = self.objects.get_or_create(status_text='Return 8F')
        return obj

    @classmethod
    def SCRAP(self):
        obj,created = self.objects.get_or_create(status_text='Scrap')
        return obj

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
        return f'{self.codename} - {self.cycle}' 


class PlatformConfig(models.Model):
    id = models.BigAutoField(primary_key=True)
    config_name = models.CharField(max_length=50,null=True,blank=True)
    config_url = models.URLField(max_length=200,null=True,blank=True)

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
        ordering = ['phase_text']

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
        return f'{self.platform.codename} - {self.platform.cycle} - {self.phase.phase_text}'

    def config_name(self):
        return self.config.config_name

    def config_url(self):
        return self.config.config_url


class Uut(models.Model):
    id = models.BigAutoField(primary_key=True)
    sn = models.CharField(unique=True, max_length=50)
    sku = models.CharField(max_length=50, blank=True, null=True)
    cpu = models.CharField(max_length=50, blank=True, null=True)
    status = models.ForeignKey(UutStatus, models.DO_NOTHING, blank=True, null=True,default=UutStatus.KEEPON())
    # try:
        # status = models.ForeignKey(UutStatus, models.DO_NOTHING, blank=True, null=True,default=UutStatus.KEEPON())
    # except:
    #     status = models.ForeignKey("UutStatus", models.DO_NOTHING, blank=True, null=True)
    # status = models.ForeignKey("UutStatus", models.DO_NOTHING, blank=True, null=True)
    scrap_reason = models.TextField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    scrap = models.BooleanField(default=False)
    # keyin_time = models.DateTimeField(auto_now_add=True)
    keyin_time = models.DateTimeField(blank=True, null=True,auto_now_add=True)
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
    def last_borrowed(self):
         return self.uutborrowhistory_set.filter(back_time__isnull=True).first() 

    @property
    def borrower(self):
        history = self.last_borrowed
        return '-' if not history else history.member.usernameincompany

    def borrow_purpose(self):
        history = self.last_borrowed
        return '-' if not history else history.purpose
    

    def platform_name(self):
        try:
            return self.platform_phase.platform.codename
        except:
            return '-'
    platform_name.short_description = 'platform'
    platform_name.admin_order_field = 'platform__codename'

    def platform_group(self):
        try:
            return self.platform_phase.platform.group
        except:
            return '-'
    platform_group.short_description = 'group'

    def platform_target(self):
        try:
            return self.platform_phase.platform.target
        except:
            return '-'
    platform_target.short_description = 'target'

    def platform_cycle(self):
        try:
            return self.platform_phase.platform.cycle
        except:
            return '-'
    platform_cycle.short_description = 'cycle'
    platform_cycle.admin_order_field = 'platform__cycle'

    def uut_phase(self):
        try:
            return self.platform_phase.phase.phase_text
        except:
            return '-'
    uut_phase.short_description = 'phase'


class UutBorrowHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    # rent_time = models.DateTimeField(auto_now_add=True)
    rent_time = models.DateTimeField(null=True)
    back_time = models.DateTimeField(blank=True, null=True)
    purpose = models.TextField(blank=True, null=True)
    member = models.ForeignKey(Member, models.CASCADE, blank=True, null=True)
    uut = models.ForeignKey(Uut, models.CASCADE)

    class Meta:
        managed = True
        db_table = 'uut_borrow_history'
        


    def uut_phase(self):
        return self.platform_phase.phase.phase_text
    uut_phase.short_description = 'phase'