# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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
    ssid_2_4 = models.CharField(db_column='ssid_2.4', max_length=50)  # Field renamed to remove unsuitable characters.
    ssid_2_4_password = models.CharField(db_column='ssid_2.4_password', max_length=50)  # Field renamed to remove unsuitable characters.
    ssid_2_4_bssid = models.CharField(db_column='ssid_2.4_bssid', max_length=50, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    ssid_2_4_band = models.CharField(db_column='ssid_2.4_band', max_length=50, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    ssid_5 = models.CharField(max_length=50, blank=True, null=True)
    ssid_5_password = models.CharField(max_length=50, blank=True, null=True)
    ssid_5_bssid = models.CharField(max_length=50, blank=True, null=True)
    ssid_5_band = models.CharField(max_length=50, blank=True, null=True)
    fw = models.CharField(max_length=100, blank=True, null=True)
    remark = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ap'


class ApBorrowHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    borrower = models.ForeignKey('Member', models.DO_NOTHING)
    ap = models.ForeignKey(Ap, models.DO_NOTHING)
    rent_time = models.DateTimeField()
    back_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
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
    dashboard_uuid = models.UUIDField()
    group_name = models.CharField(max_length=50, blank=True, null=True)
    unit_manager = models.ForeignKey('Member', models.DO_NOTHING, db_column='unit_manager')

    class Meta:
        managed = False
        db_table = 'dashboard'


class Driver(models.Model):
    id = models.BigAutoField(primary_key=True)
    owner = models.ForeignKey('Member', models.DO_NOTHING, db_column='owner')
    name = models.TextField()
    version = models.CharField(max_length=50)
    release_time = models.TimeField()
    path = models.TextField(blank=True, null=True)  # This field type is a guess.
    category = models.CharField(max_length=50, blank=True, null=True)
    package_name = models.TextField(unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'driver'


class Member(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=50, blank=True, null=True)
    birth = models.DateField(blank=True, null=True)
    mail = models.CharField(unique=True, max_length=50)
    enabled = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'member'


class Module(models.Model):
    id = models.BigAutoField(primary_key=True)
    deliverable_name = models.TextField()
    short_name = models.CharField(max_length=50)
    vender_id = models.CharField(max_length=50, blank=True, null=True)
    device_id = models.CharField(max_length=50, blank=True, null=True)
    subsys_device_id = models.CharField(max_length=50, blank=True, null=True)
    subsys_vender_id = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    owner = models.ForeignKey(Member, models.DO_NOTHING)
    support_driver = models.ForeignKey(Driver, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'module'


class Platform(models.Model):
    id = models.BigAutoField(primary_key=True)
    update_time = models.DateTimeField()
    content = models.CharField(max_length=100, blank=True, null=True)
    behavior = models.CharField(max_length=100, blank=True, null=True)
    codename = models.CharField(max_length=200, blank=True, null=True)
    group = models.CharField(max_length=50, blank=True, null=True)
    target = models.CharField(max_length=50, blank=True, null=True)
    development_center = models.CharField(max_length=200, blank=True, null=True)
    cycle = models.CharField(max_length=50, blank=True, null=True)
    forecast_cycle = models.CharField(max_length=50, blank=True, null=True)
    series = models.CharField(max_length=200, blank=True, null=True)
    forecast_series = models.CharField(max_length=200, blank=True, null=True)
    chipset = models.CharField(max_length=200, blank=True, null=True)
    marketing_name = models.CharField(max_length=200, blank=True, null=True)
    odm = models.CharField(db_column='ODM', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sepm = models.CharField(db_column='SEPM', max_length=50, blank=True, null=True)  # Field name made lowercase.
    pdm = models.CharField(db_column='PDM', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'platform'


class Script(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    tool = models.ForeignKey('Tool', models.DO_NOTHING, blank=True, null=True)
    wwan = models.TextField()  # This field type is a guess.
    wlan = models.TextField()  # This field type is a guess.
    bt = models.TextField()  # This field type is a guess.
    lan = models.TextField()  # This field type is a guess.
    rfid = models.TextField()  # This field type is a guess.
    nfc = models.TextField()  # This field type is a guess.
    path = models.TextField(blank=True, null=True)  # This field type is a guess.
    create_time = models.DateTimeField()
    version = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'script'


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
    task_uuid = models.UUIDField()
    assigner = models.ForeignKey(Member, models.DO_NOTHING, db_column='assigner')

    class Meta:
        managed = False
        db_table = 'task'


class Tool(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    version = models.CharField(max_length=50, blank=True, null=True)
    path = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tool'


class Uut(models.Model):
    id = models.BigAutoField(primary_key=True)
    platform = models.ForeignKey(Platform, models.DO_NOTHING, blank=True, null=True)
    sn = models.CharField(max_length=50)
    sku = models.CharField(max_length=50, blank=True, null=True)
    cpu = models.CharField(max_length=50, blank=True, null=True)
    phase = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50)
    scrap_reason = models.TextField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    scrap = models.BooleanField()
    keyin_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uut'



class UutBorrowHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    member = models.ForeignKey(Member, models.DO_NOTHING)
    rent_time = models.DateTimeField()
    back_time = models.TimeField(blank=True, null=True)
    uut = models.ForeignKey(Uut, models.DO_NOTHING)
    purpose = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uut_borrow_history'
