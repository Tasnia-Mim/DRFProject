import uuid

from django.db import models
from django.conf import settings

from phonenumber_field.modelfields import PhoneNumberField

from autoslug import AutoSlugField
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from .manager import CustomUserManager       

class User(AbstractBaseUser, PermissionsMixin):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)      
    name = models.CharField(max_length=255)         
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    is_organization_user = models.BooleanField(default=False)   
    slug = AutoSlugField(populate_from= 'name', unique = True)

    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return f"UID: {self.uid}, Name: {self.name}" 




class OrganizationUser(models.Model): 
    GENDER_CHOICE =(
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    )       
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='organization_user', null='True', blank='True')    
    role = models.CharField(max_length=100, null='True', blank='True')    
    gender = models.CharField(max_length=20, choices=GENDER_CHOICE , null='True', blank='True')
    personal_phone = PhoneNumberField(blank=True)
    personal_address = models.TextField(null='True', blank='True') 
    

    def __str__(self):
        return f'{self.user}'
       


class Doctor(models.Model):
    GENDER_CHOICE =(
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    )      
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor', null='True', blank='True')    
    speciality = models.CharField(max_length=100, null='True', blank='True')
    chamber_email = models.CharField(max_length=100, null='True', blank='True')
    chamber_phone = models.CharField(max_length=100, null='True', blank='True')   
    personal_phone =PhoneNumberField(blank=True)
    personal_address = models.TextField(null='True', blank='True') 
    about = models.TextField(null='True', blank='True')
    gender = models.CharField(max_length=20, choices=GENDER_CHOICE , null='True', blank='True')

    def __str__(self):
        return f'{self.user}'

   

class Patient(models.Model):
    GENDER_CHOICE =(
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient', null='True', blank='True')
    blood_group = models.CharField(max_length=50, null='True', blank='True')
    weight = models.TextField(null='True', blank='True')
    height = models.TextField(null='True', blank='True')
    gender = models.CharField(max_length=20, choices=GENDER_CHOICE , null='True', blank='True')
    phone =PhoneNumberField(blank=True)
    address = models.TextField(null='True', blank='True')    

    def __str__(self):
        return f'{self.user}'

    
    
class Appointment(models.Model):
    STATUS_CHOICE = (
        ('approved','approved'),
        ('canceled','canceled'),
        ('pending','pending'),
    )
    uid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointment', null='True', blank='True')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_appointment', null='True', blank='True')
    request_time = models.DateTimeField(auto_now_add = True)
    problem = models.TextField(null='True', blank='True')
    appointment_time = models.DateTimeField(max_length=100, null='True', blank='True')
    fee = models.TextField(null='True', blank='True')
    appointment_status = models.CharField(max_length=20, choices=STATUS_CHOICE, null='True', blank='True')

  

class Medicine(models.Model):
    uid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length=255)     

    def __str__(self):
        return f"UID: {self.uid}, Name: {self.name}"    

    

class Prescription(models.Model):
    uid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_prescription', null='True', blank='True')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_prescription', null='True', blank='True')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='prescription', null='True', blank='True')                
    generated_at =  models.DateTimeField(auto_now_add = True)
    treatment = models.TextField(null='True', blank='True')



class DoctorFollow(models.Model):
    FOLLOW_STATUS_CHOICE = (
        ('approved','approved'),
        ('canceled','canceled'),
        ('pending','pending'),
    )
    uid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow_sender', null='True', blank='True')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow_receiver', null='True', blank='True')
    follow_status = models.CharField(max_length=20, choices=FOLLOW_STATUS_CHOICE, null='True', blank='True')



class PatientFollow(models.Model):    
    uid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow_sender_patient', null='True', blank='True')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow_receiver_doctor', null='True', blank='True')
    

class Blog(models.Model): 
    uid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    blogger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs', null='True', blank='True')
    tittle = models.CharField(max_length=200, null='True', blank='True')
    blog = models.TextField(null='True', blank='True')

    def __str__(self):
        return f"UID: {self.uid}, Tittle: {self.tittle}"    


    



    






