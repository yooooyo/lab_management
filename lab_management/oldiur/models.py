# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Commercial2018(models.Model):
    platformname = models.CharField(db_column='PlatformName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    phase = models.CharField(db_column='Phase', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sku = models.FloatField(db_column='SKU', blank=True, null=True)  # Field name made lowercase.
    sn = models.CharField(db_column='SN', max_length=255, blank=True, null=True)  # Field name made lowercase.
    borrower = models.CharField(db_column='Borrower', max_length=255, blank=True, null=True)  # Field name made lowercase.
    unitstatus = models.CharField(db_column='unitStatus', max_length=255, blank=True, null=True)  # Field name made lowercase.
    yearcycle = models.CharField(db_column='YearCycle', max_length=255, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=255, blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=255, blank=True, null=True)  # Field name made lowercase.
    borrowingdate1 = models.DateTimeField(db_column='borrowingDate1', blank=True, null=True)  # Field name made lowercase.
    position = models.CharField(max_length=255, blank=True, null=True)
    cat = models.CharField(db_column='CAT', max_length=255, blank=True, null=True)  # Field name made lowercase.
    borrowingdate2 = models.CharField(db_column='borrowingDate2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    borrowingdate3 = models.CharField(db_column='borrowingDate3', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mailone = models.CharField(db_column='mailOne', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mailtwo = models.CharField(db_column='mailTwo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mailthree = models.CharField(db_column='mailThree', max_length=255, blank=True, null=True)  # Field name made lowercase.
    keyintime = models.CharField(db_column='keyInTime', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cpu = models.CharField(db_column='CPU', max_length=255, blank=True, null=True)  # Field name made lowercase.
    wlan = models.CharField(db_column='WLAN', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "'Commercial 2018$'"


class CatInfo(models.Model):
    platform = models.CharField(db_column='Platform', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sn = models.CharField(db_column='SN', primary_key=True, max_length=11)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=20, blank=True, null=True)  # Field name made lowercase.
    currenttask = models.TextField(db_column='CurrentTask', blank=True, null=True)  # Field name made lowercase.
    os = models.CharField(db_column='OS', max_length=30, blank=True, null=True)  # Field name made lowercase.
    image = models.CharField(db_column='Image', max_length=30, blank=True, null=True)  # Field name made lowercase.
    bios = models.CharField(db_column='BIOS', max_length=30, blank=True, null=True)  # Field name made lowercase.
    wlan_module = models.TextField(db_column='WLAN Module', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    wlan_driver = models.TextField(db_column='WLAN Driver', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    bt_module = models.TextField(db_column='BT Module', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    bt_driver = models.TextField(db_column='BT Driver', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    wwan_module = models.TextField(db_column='WWAN Module', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    wwan_driver = models.TextField(db_column='WWAN Driver', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gnss_module = models.TextField(db_column='GNSS Module', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gnss_driver = models.TextField(db_column='GNSS Driver', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    nic_module = models.TextField(db_column='NIC Module', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    nic_driver = models.TextField(db_column='NIC Driver', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    nfc_module = models.TextField(db_column='NFC Module', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    nfc_driver = models.TextField(db_column='NFC Driver', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rfid_module = models.TextField(db_column='RFID Module', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rfid_driver = models.TextField(db_column='RFID Driver', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    lastusedtime = models.DateTimeField(db_column='LastUsedTime', blank=True, null=True)  # Field name made lowercase.
    tag = models.CharField(db_column='Tag', max_length=50, blank=True, null=True)  # Field name made lowercase.
    wwan_firmware = models.TextField(db_column='WWAN Firmware', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    wwan_modem = models.TextField(db_column='WWAN Modem', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'CAT_info'


class Drivertable(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    prouct = models.CharField(db_column='Prouct', max_length=100, blank=True, null=True)  # Field name made lowercase.
    sw_manager = models.CharField(db_column='SW Manager', max_length=100, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    modules = models.TextField(db_column='Modules', blank=True, null=True)  # Field name made lowercase.
    device = models.CharField(db_column='Device', max_length=100, blank=True, null=True)  # Field name made lowercase.
    os = models.CharField(db_column='OS', max_length=100, blank=True, null=True)  # Field name made lowercase.
    deliverables = models.TextField(db_column='Deliverables', blank=True, null=True)  # Field name made lowercase.
    version = models.CharField(db_column='Version', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DriverTable'


class Erdtable(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    deliverables_name = models.CharField(db_column='Deliverables_Name', max_length=150, blank=True, null=True)  # Field name made lowercase.
    short_name = models.CharField(db_column='Short_Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    owner = models.CharField(db_column='Owner', max_length=50, blank=True, null=True)  # Field name made lowercase.
    vender_id = models.CharField(db_column='Vender_ID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    device_id = models.CharField(db_column='Device_ID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    subsys_vender_id = models.CharField(db_column='Subsys_Vender_ID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    subsys_device_id = models.CharField(db_column='Subsys_Device_ID', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ERDTable'


class IurBorrowRecord(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sn = models.CharField(db_column='SN', max_length=100, blank=True, null=True)  # Field name made lowercase.
    platformname = models.CharField(db_column='platformName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    phase = models.CharField(max_length=100, blank=True, null=True)
    sku = models.CharField(db_column='SKU', max_length=100, blank=True, null=True)  # Field name made lowercase.
    borrower = models.CharField(max_length=100, blank=True, null=True)
    unitstatus = models.CharField(db_column='unitStatus', max_length=100, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(max_length=100, blank=True, null=True)
    borrowingdate = models.DateTimeField(db_column='borrowingDate', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'IUR_borrow_record'


class IurMailList(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(unique=True, max_length=500, blank=True, null=True)
    mail = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'IUR_mail_list'


class OdmFunctionalTest(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    platform = models.CharField(max_length=200, blank=True, null=True)
    os = models.CharField(db_column='OS', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bios = models.CharField(db_column='BIOS', max_length=200, blank=True, null=True)  # Field name made lowercase.
    module = models.CharField(max_length=200, blank=True, null=True)
    driver_version = models.CharField(max_length=200, blank=True, null=True)
    firmware_version = models.CharField(max_length=200, blank=True, null=True)
    installer_release_day = models.DateTimeField(blank=True, null=True)
    target_get_result_day = models.DateTimeField(blank=True, null=True)
    note = models.CharField(max_length=200, blank=True, null=True)
    start_day = models.DateTimeField(blank=True, null=True)
    end_day = models.DateTimeField(blank=True, null=True)
    image_version = models.CharField(max_length=200, blank=True, null=True)
    ftp = models.CharField(max_length=400, blank=True, null=True)
    odm = models.CharField(db_column='ODM', max_length=200, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(max_length=200, blank=True, null=True)
    category = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ODM_functional_test'


class OdmStressTest(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    platform = models.CharField(max_length=200, blank=True, null=True)
    os = models.CharField(db_column='OS', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bios = models.CharField(db_column='BIOS', max_length=200, blank=True, null=True)  # Field name made lowercase.
    module = models.CharField(max_length=200, blank=True, null=True)
    driver_version = models.CharField(max_length=200, blank=True, null=True)
    firmware_version = models.CharField(max_length=200, blank=True, null=True)
    test_script = models.CharField(max_length=200, blank=True, null=True)
    note = models.CharField(max_length=200, blank=True, null=True)
    start_day = models.DateTimeField(blank=True, null=True)
    end_day = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ODM_stress_test'


class Taskitem(models.Model):
    taskitem = models.TextField(db_column='TaskItem', blank=True, null=True)  # Field name made lowercase.
    taskindex = models.BigIntegerField(db_column='TaskIndex', blank=True, null=True)  # Field name made lowercase.
    tasktype = models.CharField(db_column='TaskType', max_length=10, blank=True, null=True)  # Field name made lowercase.
    id = models.BigIntegerField(db_column='ID',  null=False,primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TaskItem'


class Testtable(models.Model):
    personid = models.IntegerField(db_column='personID', primary_key=True)  # Field name made lowercase.
    personname = models.CharField(db_column='personName', max_length=25)  # Field name made lowercase.
    personmoney = models.DecimalField(db_column='personMoney', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    persondescription = models.TextField(db_column='personDescription', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'TestTable'


class Unittable(models.Model):
    sn = models.CharField(db_column='SN', unique=True, max_length=100, blank=True, null=True)  # Field name made lowercase.
    platformname = models.CharField(db_column='platformName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    phase = models.CharField(max_length=100, blank=True, null=True)
    sku = models.CharField(db_column='SKU', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cat = models.CharField(db_column='CAT', max_length=100, blank=True, null=True)  # Field name made lowercase.
    borrower = models.CharField(max_length=100, blank=True, null=True)
    unitstatus = models.CharField(db_column='unitStatus', max_length=100, blank=True, null=True)  # Field name made lowercase.
    yearcycle = models.CharField(db_column='yearCycle', max_length=100, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(max_length=100, blank=True, null=True)
    note = models.CharField(max_length=100, blank=True, null=True)
    borrowingdate1 = models.DateTimeField(db_column='borrowingDate1', blank=True, null=True)  # Field name made lowercase.
    position = models.CharField(max_length=100, blank=True, null=True)
    keyintime = models.DateTimeField(db_column='keyInTime')  # Field name made lowercase.
    mailone = models.CharField(db_column='mailOne', max_length=100, blank=True, null=True)  # Field name made lowercase.
    mailtwo = models.CharField(db_column='mailTwo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    mailthree = models.CharField(db_column='mailThree', max_length=100, blank=True, null=True)  # Field name made lowercase.
    borrowingdate2 = models.DateTimeField(db_column='borrowingDate2', blank=True, null=True)  # Field name made lowercase.
    borrowingdate3 = models.DateTimeField(db_column='borrowingDate3', blank=True, null=True)  # Field name made lowercase.
    cpu = models.CharField(db_column='CPU', max_length=100, blank=True, null=True)  # Field name made lowercase.
    wlan = models.CharField(db_column='WLAN', max_length=100, blank=True, null=True)  # Field name made lowercase.
    noteone = models.CharField(db_column='noteOne', max_length=100, blank=True, null=True)  # Field name made lowercase.
    notetwo = models.CharField(db_column='noteTwo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    notethree = models.CharField(db_column='noteThree', max_length=100, blank=True, null=True)  # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UnitTable'

    def __str__(self):
        return f"{self.id} {self.sn} {self.platformname} {self.borrower}"
    


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Sysdiagrams(models.Model):
    name = models.CharField(max_length=128)
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    definition = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sysdiagrams'
        unique_together = (('principal_id', 'name'),)


class Tasktable(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sn = models.CharField(db_column='SN', max_length=11)  # Field name made lowercase.
    task = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=10, blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    starttime = models.DateTimeField(db_column='startTime', blank=True, null=True)  # Field name made lowercase.
    finishtime = models.DateTimeField(db_column='finishTime', blank=True, null=True)  # Field name made lowercase.
    series = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'taskTable'


class TaskResultAnalysis(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    task_id = models.IntegerField(db_column='task_ID')  # Field name made lowercase.
    type = models.CharField(max_length=500, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    device = models.CharField(max_length=500, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'task_result_analysis'
