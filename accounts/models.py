from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, UserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager

import qrcode
from io import BytesIO
from django.core.files import File
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        extra_fields.setdefault('is_active', True)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields['role'] = CustomUser.ADMIN  # Set the role to "admin"
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    ADMIN = 'admin'
    REGISTRATION_OFFICER = 'registration_officer'
    CLIENT = 'client'
    

    ROLE_CHOICES = [
        (ADMIN, _('Admin')),
        (REGISTRATION_OFFICER, _('registration_officer')),
        (CLIENT, _('client')),
    ]

    GENDER_CHOICE = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Non-binary', 'Non-binary'),
        ('Prefer not to say', 'Prefer not to say'),
    )

    REGION_CHOICES = (
        ('Muslim', 'Muslim'),
        ('Christian', 'Christian'),
        ('Prefer not to say', 'Prefer not to say'),
    )

    DISTRICT_CHOICE = (
        ('Kailauhun','Kailahun'),
        ('Kenema','Kenema'),
        ('Kono','Kono'),
        ('Bombali','Bombali'),
        ('Falaba','Falaba'),
        ('koinadugu','Koinadugu'),
        ('Tonkolili','Tokolili'),
        ('Kambia','Kambia'),
        ('Karene','Karene'),
        ('PortLoko','PortLoko'),
        ('Bo','Bo'),
        ('Bonth','Bonth'),
        ('Moyamba','Moyamba'),
        ('Pujehun','Pujehun'),
        ('Western Rural','Western Rural'),
        ('Western Urban','Wester Urban'),
    )

    REGION_CHOICES = (
        ('Eastern','Eastern'),
        ('Northern','Northern'),
        ('North East','North East'),
        ('Southern','Southern'),
        ('Western','Western')
    )

    TOWN_CHOICES = (
        ('Kailauhun','Kailahun'),
        ('Kenema','Kenema'),
        ('Freetown','Freetown'),
        ('Koidu_Town','Koidu_Town'),
        ('WaterLoo','WaterLoo'),
        ('Makeni','Makeni'),
        ('Magburaka','Magburaka'),
        ('Kambia','Kambia'),
        ('Kabala','Kabala'),
        ('Kamakwie','Kamakwie'),
        ('Bo','Bo'),
        ('Bonth','Bonth'),
        ('Moyamba','Moyamba'),
        ('Pujehun','Pujehun'),
        ('Bendugu','Bendugu'),
        ('PortLoko','PortLoko') 
    )


    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=CLIENT)
    nin = models.CharField(unique=True)
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(choices=GENDER_CHOICE, default='Male')
    religion = models.CharField(max_length=20, choices=REGION_CHOICES, default='Eastern')
    Telephone = models.CharField(max_length= 20, blank=True, null=True)
    address = models.CharField()
    photo = models.ImageField()
    district = models.CharField(choices=DISTRICT_CHOICE, default='Kono')
    region = models.CharField(max_length=20, choices=REGION_CHOICES, default='Eastern')
    city = models.CharField(max_length=50, choices=TOWN_CHOICES, default='Bo')
    occupation = models.CharField(max_length=50, blank=True, null=True)
    mother_name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=50)

    is_staff = models.BooleanField(default=False)  # Admin users are staff


    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    @property
    def is_client(self):
        return self.role == self.CLIENT
    
    @property
    def is_admin(self):
        return self.role == self.ADMIN
    
    @property
    def is_registration_officer(self):
        return self.role == self.REGISTRATION_OFFICER

    def save(self, *args, **kwargs):
        if self.is_admin:
            self.is_staff = True
        super().save(*args, **kwargs)



    def generate_qr_code(self):
        qr = self.generate_

