# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from .twilio import *
import uuid
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

from geoposition.fields import GeopositionField


class MyUserManager(BaseUserManager):
    ''' Inherits BaseUserManager class'''

    def create_superuser(self, email, password):
        '''Creates and saves a superuser with the given email and password.'''
        user = self.model(email=email)
        user.set_password(password)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None):
        """
        Create user with given email and password.
        :param email:
        :param password:
        :return:
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email))
        # set_password is used set password in encrypted form.
        # user.set_password(blank=True)
        user.is_active = True
        user.save(using=self._db)
        return user


# # --------------Model for website User--------------------

class MyUser(AbstractBaseUser, PermissionsMixin):
    '''Base User Table used same for Authentication Purpose	'''
    
    '''Docstring for MyUser'''
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True
    )
    email = models.EmailField(
        "Email", unique=True,max_length=100
        )
    full_name = models.CharField(
        "Full Name", max_length=40
    )
    mobile = models.CharField(
        "Mobile", max_length=15, unique=True
    )
    
    is_block = models.BooleanField(
        default=False
    )
    otp = models.CharField(
        'OTP', max_length=4, blank=True, null=True
    )
    is_otp_verified = models.BooleanField(
        'OTP Verified ', default=False
    )

    is_active = models.BooleanField(
        'Active', default=True)
    is_staff = models.BooleanField('Staff', default=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    is_superuser = models.BooleanField(
        default=False
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    objects = MyUserManager()
    USERNAME_FIELD = 'email' 

    def __str__(self):
        """:return: the email"""
        return self.full_name

class PointOfInterest(models.Model):
    email = models.CharField(max_length=100)
    position = GeopositionField()

    def __str__(self):
    	return self.email
    
class Products(models.Model):
	CHOICE=[
    ('Chocolate', 'Chocolate'),
    ('Biscuit', 'Biscuit'),
    ('Fruits', 'Fruits'),
    ('Vegetables', 'Vegetables'),
    ('Flower', 'Flower'),  
    ('Mobile','Mobile') ,
    ]

	name=models.CharField(max_length=100)
	price=models.FloatField()
	offer_price=models.FloatField()

	product_id=models.IntegerField(unique=True)
	discription=models.CharField(max_length=200)
	choice = models.CharField(('choice'), max_length=20, choices=CHOICE)
	img=models.ImageField(upload_to='proimg')
	def __str__(self):
		return self.name

class ProductChoice(models.Model):
	name=models.CharField(max_length=100)
	
	def __str__(self):
		return self.name
class Cart(models.Model):
	id=models.AutoField(primary_key=True)
	email=models.CharField(max_length=80)
	book_id=models.CharField(max_length=80)
	book_name=models.CharField(max_length=80)
	index=models. BooleanField(default=True)
	price=models.FloatField()
	deleverd=models.BooleanField(default=True)
	img=models.CharField(max_length=100)
	prd_name=models.CharField(max_length=100)
	total=models.FloatField()
	quantity=models.IntegerField(default=1)
	order_id=models.CharField(max_length=100)
	def __str__(self):
		return self.book_name

class Orders(models.Model):
	id=models.AutoField(primary_key=True)
	email=models.CharField(max_length=80)
	book_id=models.CharField(max_length=80,unique=True)
	price=models.FloatField()
	address=models.CharField(max_length=80)
	name=models.CharField(max_length=80)
	pin=models.CharField(max_length=10)

	def __str__(self):
		return self.email