from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.db.models import Q 
import uuid
import datetime

from django.db.models.fields import BigIntegerField, TextField, URLField

# Create your models here.
class Ap(models.Model):
    id = models.BigAutoField(primary_key=True)
    no = models.CharField(max_length=100,blank=True,null=True)
    name = models.CharField(max_length=50,blank=True,default='Unknown')
    vender = models.CharField(max_length=50, blank=True, null=True)
    adapter = models.CharField(max_length=50, blank=True, null=True)
    storage = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    cycle = models.CharField(max_length=50, blank=True, null=True)
    cpu = models.CharField(max_length=50, blank=True, null=True)
    chip1 = models.CharField(max_length=100, blank=True, null=True)
    chip1_protocols = models.CharField(max_length=50, blank=True, null=True)
    chip2 = models.CharField(max_length=100, blank=True, null=True)
    chip2_protocols = models.CharField(max_length=50, blank=True, null=True)
    network_technology_standard = models.CharField(max_length=50, blank=True, null=True)
    admin_id = models.CharField(max_length=50, blank=True, null=True)
    admin_pw = models.CharField(max_length=50, blank=True, null=True)
    ssid_2d4 = models.CharField(max_length=50, blank=True, null=True)
    ssid_2d4_password = models.CharField(max_length=50, blank=True, null=True)
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
    is_default = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'ap'

    def __str__(self) -> str:
        return self.ssid_2d4 or self.ssid_5 
    
    @classmethod
    def find_by_ssid(self,ssid):
        if ssid:
            return self.objects.filter(Q(ssid_2d4__iexact=ssid)|Q(ssid_5__iexact=ssid))
        return None

    @classmethod
    def find_or_create_by_ssid(self,ssid):
        return self.objects.get_or_create(ssid_2d4=ssid)

    @classmethod
    def get_default_ap(self):
        return self.objects.get(is_default=True)


class ApBorrowHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    ap = models.ForeignKey(Ap, models.DO_NOTHING)
    borrower = models.ForeignKey('iur.Member', models.DO_NOTHING)
    rent_time = models.DateTimeField()
    back_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ap_borrow_history'

class DriverCategory(models.Model):
    name = models.CharField(max_length=50,unique=True)

    class Meta:
        managed = True
        db_table='driver_category'

class Driver(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50,blank=True,null=True)
    owner = models.ForeignKey('iur.Member', models.CASCADE,null=True,blank=True)
    package_name = models.TextField(unique=True, blank=True, null=True)
    version = models.CharField(max_length=50)
    release_time = models.TimeField(null=True,blank=True)
    category = models.ForeignKey(DriverCategory, blank=True, null=True,on_delete=models.DO_NOTHING)
    path = models.FileField(upload_to='uploads/driver/',null=True,blank=True)
    driver_url = models.URLField(null=True,blank=True,db_column='url')
    description=models.TextField(null=True,blank=True)
    support_module = ArrayField(base_field=models.BigIntegerField(),null=True,blank=True)

    class Meta:
        managed = True
        db_table = 'driver'
    def __str__(self) -> str:
        return self.name

class Module(models.Model):
    id = models.BigAutoField(primary_key=True)
    deliverable_name = models.TextField(blank=True,null=True)
    short_name = models.CharField(max_length=50,blank=True,null=True)
    vender_id = models.CharField(max_length=50, blank=True, null=True)
    device_id = models.CharField(max_length=50, blank=True, null=True)
    subsys_device_id = models.CharField(max_length=50, blank=True, null=True)
    subsys_vender_id = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    owner = models.ForeignKey('iur.Member', models.DO_NOTHING,blank=True,null=True)

    class Meta:
        managed = True
        db_table = 'module'

    def __str__(self) -> str:
        return self.short_name

class Tool(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    version = models.CharField(max_length=50, blank=True, null=True)
    tool_url = URLField(null=True,blank=True,db_column='url')

    class Meta:
        managed = True
        db_table = 'tool'

    def __str__(self):
       return self.name +':'+ self.version
        

class Script(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField(unique=True)
    version = models.CharField(max_length=50, blank=True, null=True)
    tool = models.ManyToManyField(Tool)
    functions=ArrayField(base_field=models.BigIntegerField(),null=True,blank=True)
    wwan = models.BooleanField(default=False)
    wlan = models.BooleanField(default=False)
    bt = models.BooleanField(default=False)
    lan = models.BooleanField(default=False)
    rfid = models.BooleanField(default=False)
    nfc = models.BooleanField(default=False)
    path = models.FileField(upload_to='uploads/scripts/',null=True,blank=True)
    script_url  = URLField(null=True,blank=True,db_column='url')
    add_time = models.DateTimeField(default=datetime.datetime.now())

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

# class TaskManager(models.Manager):

#     def create(self,script_name,status='wait',assigner = None,task_group=None,power_cycle_info=None,ap=None):
#         pass

class Task(models.Model):
    id = models.BigAutoField(primary_key=True)
    uut = models.ForeignKey('iur.Uut',on_delete=models.CASCADE,null=True,blank=True)
    uut_uuid = models.UUIDField(null=True,blank=True)
    group_uuid = models.UUIDField()
    group_series = models.BigIntegerField(null=False,blank=False)
    group_name = models.CharField(max_length=50,blank=True,null=True)
    group_task_series = models.BigIntegerField(blank=True,null=True)
    script = models.ForeignKey(Script,on_delete=models.CASCADE,null=False)
    status = models.ForeignKey(TaskStatus,on_delete=models.CASCADE,null=False)
    ap = models.ForeignKey(Ap,on_delete=models.CASCADE,blank = True,null=True)
    assigner = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    uut_info = JSONField(blank=True,null=True)
    power_cycle_info = JSONField(blank=True,null=True)
    start_time = models.DateTimeField(blank=True,null=True)
    finish_time = models.DateTimeField(blank = True,null=True)
    add_time=models.DateTimeField(auto_now_add=True)
    tool = models.ForeignKey(Tool,on_delete=models.CASCADE,null=True,blank=True)
    # ssid = models.TextField(blank=True,null=True)
    log = URLField(blank=True,null=True)

    class Meta:
        managed = True
        db_table='uut_task'# This is an auto-generated Django model module.
        unique_together=['group_task_series','group_uuid']
     
    def __str__(self) -> str:
        return f'{self.id} - {self.uut} - {self.group_name} - {self.script} {self.status}'

    # objects = TaskManager()


class PowerState(models.Model):
    name = models.CharField(max_length=50,unique=True)
    description = models.TextField(null=True,blank=True)

    class Meta:
        managed=True
        db_table = 'power_state'
    
    def __str__(self) -> str:
        return self.name

class TaskFunction(models.Model):
    name = models.CharField(max_length=50,unique=True)
    description = models.TextField(null=True,blank=True)

    class Meta:
        managed = True
        db_table='task_function'

class TaskIssue(models.Model):
    title = models.CharField(max_length=200,null=True,blank=True)
    level = models.CharField(max_length=50,null=True,blank=True)
    task=models.ForeignKey(Task,on_delete=models.CASCADE)
    power_state = models.ForeignKey(PowerState,null=True,blank=True,on_delete=models.CASCADE)
    device_driver = JSONField(null=True,blank=True)
    function = JSONField(null=True,blank=True)
    description = TextField(null=True,blank=True)
    add_time=models.DateTimeField(blank=True,null=True,default=datetime.datetime.now())
    
    class Meta:
        managed = True
        db_table='task_issue'

class GeneralQueryString(models.Model):
    name=models.CharField(max_length=200)
    query = models.TextField()
    description = models.TextField(null=True,blank=True)

    class Meta:
        db_table='generalquerystring'
    

