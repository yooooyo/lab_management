# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.conf import settings
import uuid
from django.contrib.auth.models import Group,User

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    usernameincompany = models.CharField(max_length=100)

    def __str__(self):
        return self.usernameincompany

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
    ssid_2_4 = models.CharField(db_column='ssid_2d4', max_length=50)  # Field renamed to remove unsuitable characters.
    ssid_2_4_password = models.CharField(db_column='ssid_2d4_password', max_length=50)  # Field renamed to remove unsuitable characters.
    ssid_2_4_bssid = models.CharField(db_column='ssid_2d4_bssid', max_length=50, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    ssid_2_4_band = models.CharField(db_column='ssid_2d4_band', max_length=50, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    ssid_5 = models.CharField(max_length=50, blank=True, null=True)
    ssid_5_password = models.CharField(max_length=50, blank=True, null=True)
    ssid_5_bssid = models.CharField(max_length=50, blank=True, null=True)
    ssid_5_band = models.CharField(max_length=50, blank=True, null=True)
    fw = models.CharField(max_length=100, blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'ap'


class ApBorrowHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    borrower = models.ForeignKey(Member,on_delete=models.CASCADE,)
    ap = models.ForeignKey(Ap, models.DO_NOTHING)
    rent_time = models.DateTimeField()
    back_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ap_borrow_history'


class Dashboard(models.Model):
    id = models.BigAutoField(primary_key=True)
    uut = models.ForeignKey('Uut', models.DO_NOTHING, blank=True, null=True)
    task = models.ForeignKey('Task', models.DO_NOTHING, blank=True, null=True)
    bios = models.CharField(max_length=50, blank=True, null=True)
    wwan = models.ForeignKey('Module', models.DO_NOTHING, db_column='wwan', blank=True, null=True,related_name='wwan')
    wwan_driver = models.ForeignKey('Driver', models.DO_NOTHING, db_column='wwan_driver', blank=True, null=True,related_name='wwan_driver')
    wlan = models.ForeignKey('Module', models.DO_NOTHING, db_column='wlan', blank=True, null=True,related_name='wlan')
    wlan_driver = models.ForeignKey('Driver', models.DO_NOTHING, db_column='wlan_driver', blank=True, null=True,related_name='wlan_driver')
    bt = models.ForeignKey('Module', models.DO_NOTHING, db_column='bt', blank=True, null=True,related_name='bt')
    bt_driver = models.ForeignKey('Driver', models.DO_NOTHING, db_column='bt_driver', blank=True, null=True,related_name='bt_driver')
    lan = models.ForeignKey('Module', models.DO_NOTHING, db_column='lan', blank=True, null=True,related_name='lan')
    lan_driver = models.ForeignKey('Driver', models.DO_NOTHING, db_column='lan_driver', blank=True, null=True,related_name='lan_driver')
    nfc = models.ForeignKey('Module', models.DO_NOTHING, db_column='nfc', blank=True, null=True,related_name='nfc')
    nfc_driver = models.ForeignKey('Driver', models.DO_NOTHING, db_column='nfc_driver', blank=True, null=True,related_name='nfc_driver')
    rfid = models.ForeignKey('Module', models.DO_NOTHING, db_column='rfid', blank=True, null=True,related_name='rfid')
    rfid_driver = models.ForeignKey('Driver', models.DO_NOTHING, db_column='rfid_driver', blank=True, null=True,related_name='rfid_driver')
    ap = models.ForeignKey(Ap, models.DO_NOTHING, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    join_tiom = models.DateTimeField()
    alive_time = models.DurationField(blank=True, null=True)
    dashboard_uuid = models.UUIDField(default=uuid.uuid4())
    group_name = models.CharField(max_length=50, blank=True, null=True)
    unit_manager = models.ForeignKey( Member,on_delete=models.CASCADE,)

    class Meta:
        managed = True
        db_table = 'dashboard'


class Driver(models.Model):
    id = models.BigAutoField(primary_key=True)
    owner = models.ForeignKey( Member,on_delete=models.CASCADE,)
    name = models.TextField()
    version = models.CharField(max_length=50)
    release_time = models.TimeField()
    path = models.FileField(null=True)  # This field type is a guess.
    category = models.CharField(max_length=50, blank=True, null=True)
    package_name = models.TextField(unique=True, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'driver'


class Module(models.Model):
    id = models.BigAutoField(primary_key=True)
    deliverable_name = models.TextField()
    short_name = models.CharField(max_length=50)
    vender_id = models.CharField(max_length=50, blank=True, null=True)
    device_id = models.CharField(max_length=50, blank=True, null=True)
    subsys_device_id = models.CharField(max_length=50, blank=True, null=True)
    subsys_vender_id = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    owner = models.ForeignKey( Member,on_delete=models.CASCADE,)
    support_driver = models.ForeignKey(Driver, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'module'


class Platform(models.Model):
    id = models.BigAutoField(primary_key=True)
    update_time = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=100, blank=True, null=True)
    behavior = models.CharField(max_length=100, blank=True, null=True,help_text = 'ex: NPI/OOC/SOFTPAQ')
    codename = models.CharField(max_length=200, blank=True, null=True,help_text='ex: Zigzag')
    GROUP_CHOICE = [
        ('COMMERICAL','Commerical'),
        ('CONSUMER','Consumer'),
    ]
    group = models.CharField(max_length=50, blank=True, null=True,choices = GROUP_CHOICE,)
    TARGET_CHOICE = [
        ('NB','Notebook'),
        ('DT','Desktop'),
        ('AIO','ALL in one'),
    ]
    target = models.CharField(max_length=50, blank=True, null=True,choices = TARGET_CHOICE)
    development_center = models.CharField(max_length=200, blank=True, null=True,help_text='ex: chongqing')
    cycle = models.CharField(max_length=50, blank=True, null=True,help_text='ex: 2020/20H1')
    forecast_cycle = models.CharField(max_length=50, blank=True, null=True)
    series = models.CharField(max_length=200, blank=True, null=True,help_text='ex: 300/400/500/600')
    forecast_series = models.CharField(max_length=200, blank=True, null=True)
    chipset = models.CharField(max_length=200, blank=True, null=True,help_text='ex: Tiger Lake/Coffee Lake')
    marketing_name = models.CharField(max_length=200, blank=True, null=True,help_text='ex: HP Elitebook 830 G5')
    odm = models.CharField(db_column='odm', max_length=50, blank=True, null=True,help_text = 'ex: IEC/QUANTA')  
    sepm = models.CharField(db_column='sepm', max_length=50, blank=True, null=True)  
    pdm = models.CharField(db_column='pdm', max_length=50, blank=True, null=True)  
    config = models.URLField(null=True,help_text = 'Platform configs file')
    class Meta:
        managed = True
        db_table = 'platform'

    def __str__(self):
        return self.codename


class Script(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    tool = models.ForeignKey('Tool', models.DO_NOTHING, blank=True, null=True)
    wwan = models.BooleanField() 
    wlan = models.BooleanField()  
    bt = models.BooleanField()  
    lan = models.BooleanField()  
    rfid = models.BooleanField()  
    nfc = models.BooleanField()  
    path = models.FileField(null=True)  
    create_time = models.DateTimeField()
    version = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'script'

    def __str__(self):
        return self.name


class Task(models.Model):
    id = models.BigAutoField(primary_key=True)
    uut = models.ForeignKey('Uut', models.DO_NOTHING)
    script = models.ForeignKey(Script, models.DO_NOTHING)
    tool = models.ForeignKey('Tool', models.DO_NOTHING, blank=True, null=True)
    status = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    finish_time = models.TimeField(blank=True, null=True)
    period = models.DurationField(blank=True, null=True)
    ap = models.ForeignKey(Ap, models.DO_NOTHING, blank=True, null=True)
    summary = models.TextField()
    task_uuid = models.UUIDField(default=uuid.uuid4)
    assigner = models.ForeignKey( Member,on_delete=models.CASCADE,)

    class Meta:
        managed = True
        db_table = 'task'


class Tool(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    version = models.CharField(max_length=50, blank=True, null=True)
    path = models.FileField(null=True)  # This field type is a guess.

    class Meta:
        managed = True
        db_table = 'tool'

    def __str__(self):
        return self.name

class UutPhase(models.Model):
    id = models.BigAutoField(primary_key=True)
    phase_text = models.CharField(max_length=30,null=True,unique=True)

    class Meta:
        managed = True
        db_table = 'uut_phase'
        ordering = ['-phase_text',]

    def __str__(self):
        return self.phase_text

class UutStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    status_text = models.CharField(max_length=30,null=True,unique=True)

    class Meta:
        managed = True
        db_table='uut_status'

    def __str__(self):
        return self.status_text

    

class Uut(models.Model):
    id = models.BigAutoField(primary_key=True)
    platform = models.ForeignKey('Platform', models.DO_NOTHING, blank=True, null=True, )
    sn = models.CharField(unique=True, max_length=50, null=False, blank=False)
    sku = models.CharField(max_length=50, blank=True, null=True,)
    cpu = models.CharField(max_length=50, blank=True, null=True)
    # STATUS_CHOICE = [   
    #     ('KEEP ON','Keep On'),
    #     ('RENT','Rent'),
    #     ('RETURN 8F','Return 8F'),
    # ]
    # status = models.ForeignKey(max_length=50,choices = STATUS_CHOICE,default=STATUS_CHOICE[0][1])
    status_default = UutStatus.objects.filter(status_text='Keep On')
    if status_default.count() == 0:
        status_default = UutStatus.objects.create(status_text='Keep On')
        status_default.save()
    else:
        status_default = status_default.first()
    status = models.ForeignKey(UutStatus, models.DO_NOTHING, db_column='status',blank=True, null=True,default = status_default.id )

    scrap_reason = models.TextField(blank=True, null=True,)
    remark = models.TextField(blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    scrap = models.BooleanField(default=False,)
    # keyin_time = models.DateTimeField(blank=True, null=True,auto_now_add=True)
    keyin_time = models.DateTimeField(blank=True, null=True)
    phase = models.ForeignKey(UutPhase, models.DO_NOTHING, db_column='phase', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'uut'

    def __str__(self):
        return self.sn

    @property
    def borrower(self):
        borrower = self.uutborrowhistory_set.filter(back_time__isnull=True).last()
        if borrower:
            return borrower.member.usernameincompany
        else:
            return None

class UutBorrowHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    member = models.ForeignKey(Member,on_delete=models.CASCADE,)
    # rent_time = models.DateTimeField(auto_now=True)
    rent_time = models.DateTimeField(blank=True, null=True)
    back_time = models.DateTimeField(blank=True, null=True)
    uut = models.ForeignKey(Uut, models.DO_NOTHING)
    purpose = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'uut_borrow_history'
        ordering=['rent_time',]

    def __str__(self):
        return f"{self.id} {self.uut} {self.member} '{self.rent_time}' '{self.back_time}''"
    






    

