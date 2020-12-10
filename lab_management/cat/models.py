from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
import uuid

# Create your models here.
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
        managed = True
        db_table = 'ap'
    def __str__(self) -> str:
        return self.name


class ApBorrowHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    ap = models.ForeignKey(Ap, models.DO_NOTHING)
    borrower = models.ForeignKey('iur.Member', models.DO_NOTHING)
    rent_time = models.DateTimeField()
    back_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ap_borrow_history'

class Driver(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50,blank=True,null=True)
    package_name = models.TextField(unique=True, blank=True, null=True)
    version = models.CharField(max_length=50)
    release_time = models.TimeField()
    category = models.CharField(max_length=50, blank=True, null=True)
    path = models.FileField(upload_to='uploads/driver/',null=True,blank=True)
    owner = models.ForeignKey('iur.Member', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'driver'
    def __str__(self) -> str:
        return self.name

class Module(models.Model):
    id = models.BigAutoField(primary_key=True)
    deliverable_name = models.TextField(blank=True,null=True)
    short_name = models.CharField(max_length=50)
    vender_id = models.CharField(max_length=50, blank=True, null=True)
    device_id = models.CharField(max_length=50, blank=True, null=True)
    subsys_device_id = models.CharField(max_length=50, blank=True, null=True)
    subsys_vender_id = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    owner = models.ForeignKey('iur.Member', models.DO_NOTHING)
    support_driver = ArrayField(base_field=models.BigIntegerField(),null=True)

    class Meta:
        managed = True
        db_table = 'module'

    def __str__(self) -> str:
        return self.short_name

class Tool(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    version = models.CharField(max_length=50, blank=True, null=True)
    path = models.FileField(upload_to='uploads/tool/',null=True,blank=True)

    class Meta:
        managed = True
        db_table = 'tool'

    def __str__(self) -> str:
        return self.name

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

    def __str__(self) -> str:
        return self.name

class TaskStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    status_text = models.CharField(max_length=50,unique=True,null=False)
    
    class Meta:
        managed = True
        db_table='uut_task_status'

    def __str__(self) -> str:
        return self.status_text

class Task(models.Model):
    id = models.BigAutoField(primary_key=True)
    uut = models.ForeignKey('iur.Uut',on_delete=models.CASCADE,null=False)
    script = models.ForeignKey(Script,on_delete=models.CASCADE,null=False)
    tool = models.ForeignKey(Tool,on_delete=models.CASCADE)
    status = models.ForeignKey(TaskStatus,on_delete=models.CASCADE,null=False)
    ap = models.ForeignKey(Ap,on_delete=models.CASCADE,blank = True,null=True)
    assigner = models.ForeignKey('iur.Member',on_delete=models.CASCADE)
    task_group = models.UUIDField(default=uuid.uuid4())
    uut_info = JSONField(blank=True,null=True)
    start_time = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField(blank = True,null=True)
    
    class Meta:
        managed = True
        db_table='uut_task'# This is an auto-generated Django model module.
    

