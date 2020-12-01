from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse,reverse_lazy
from django.utils.text import slugify
from speed.manager import UserManager
from django.core.exceptions import ValidationError

# Create your models here.
class Clinic(models.Model):
    name=models.CharField(max_length=100,primary_key=True)
    address=models.TextField(max_length=200)
    city=models.CharField(max_length=100)
    slug = models.SlugField(allow_unicode=True, default="slug", unique=True)
    def __str__(self):
        return self.name
    def save(self,*args,**kwargs):
        self.slug=slugify(self.name)
        super().save(*args,**kwargs)
    def get_absolute_url(self):
        return reverse('detail_clinic',kwargs={'slug':self.slug})

class Doctor(models.Model):
    user = models.OneToOneField(User,null=True,blank=True,on_delete=models.SET_NULL,related_name="doctors")
    name=models.CharField(max_length=100)
    clinic=models.ForeignKey("Clinic",null=True,blank=True,on_delete=models.SET_NULL,related_name="doctors")
    qualf=models.TextField(max_length=100,blank=False)
    special=models.TextField(max_length=100,blank=False)
    contact_no=models.CharField(max_length=10)
    members = models.ManyToManyField("Patient", through="GroupMember")
    register=models.BooleanField(default=False)
    fees=models.PositiveSmallIntegerField(null=True,blank=True)

    def __str__(self):
        return self.user.username
    def get_absolute_url(self):
        return reverse('speed:detail_doctor',kwargs={'username':self.user.username,'pk':self.pk})
class GroupMember(models.Model):
    patient = models.ForeignKey("Patient",null=True,blank=True,on_delete=models.SET_NULL,related_name="user_group")
    doctor = models.ForeignKey("Doctor",null=True,blank=True,on_delete=models.SET_NULL, related_name="membership")
    def __str(self):
        return self.patient.name


class Appointment(models.Model):
    patient=models.ForeignKey("Patient",default="1",on_delete=models.CASCADE,related_name="appointments")
    contact_no=models.CharField(max_length=10,default="Enter number")
    doctor=models.ForeignKey("Doctor",default="2",on_delete=models.CASCADE,related_name="doc_appointments")
    created_at=models.DateTimeField(auto_now=True)
    subject=models.TextField(max_length=100)
    delt=models.BooleanField(default=True)
    deldoc=models.BooleanField(default=True)
    order_id = models.AutoField(primary_key=True, auto_created=True)
    pay_status = models.BooleanField(default=False)
    def get_id(self):
        return self.order_id

    def __str__(self):
        return self.patient.user.username
    def get_absolute_url(self):
        return reverse('speed:for_patient',kwargs={'username':self.patient.user.username})

class Patient(models.Model):
    user=models.OneToOneField(User,null=True,blank=True,on_delete=models.SET_NULL,related_name="patient_profile")
    name=models.CharField(max_length=100)
    age=models.PositiveSmallIntegerField()
    email = models.EmailField(blank=True)
    phone_number_verified = models.BooleanField(default=False)
    change_pw = models.BooleanField(default=True)
    phone_number = models.CharField(default=1, unique=True, max_length=10)
    country_code = models.IntegerField(default="+91", blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'phone_number', 'country_code']
    def __str__(self):
        return self.user.username
    def get_absolute_url(self):
        return reverse('speed:detail_patient',kwargs={'username':self.user.username,'pk':self.pk})


class TimeSlot(models.Model):
    doc=models.ManyToManyField('Doctor',related_name="slots")
    date=models.DateField()
    start_time=models.TimeField()
    duration=models.IntegerField()
    def __str__(self):
        return self.doc.user.username
    def get_absolute_url(self):
        return reverse('slot_time',kwargs={'username':self.slots.user.username})




class MapDetail(models.Model):
    clinic= models.OneToOneField(Clinic, null=True, blank=True, on_delete=models.SET_NULL, related_name="rel_clinic")
    latitude=models.DecimalField(decimal_places=10,max_digits=20)
    longitude=models.DecimalField(decimal_places=10,max_digits=20)
    near=models.BooleanField(default=False)
    def __str__(self):
        return self.clinic.name











