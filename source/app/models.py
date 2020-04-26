from django.db import models
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.utils import timezone

class UserManager(BaseUserManager):
    '''
    User Custom Manager
    '''
    def create_user(self, email=None, password=None):
        '''
        Create User
        '''
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email))
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        '''
        Create Superuser
        '''
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# Create your models here.
class Manager(AbstractBaseUser, PermissionsMixin):
    '''
    Model class for Manager 
    '''
    email = models.EmailField('Email Address', unique=True)
    firstname = models.CharField('Firstname', max_length=50)
    lastname = models.CharField('Lastname', max_length=50)
    address = models.CharField('address', max_length=200, null=True, blank=True)
    company = models.CharField('Company', max_length=75)
    is_staff = models.BooleanField('Staff member', default=False)
    is_active = models.BooleanField('Active', default=False)
    is_superuser = models.BooleanField('Is a Super user', default=False)
    create_date = models.DateTimeField('Joined Time', auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    is_app_user = models.BooleanField('App User', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.firstname

    class Meta:
        ''' User Class Meta '''
        verbose_name = 'Manager'
        verbose_name_plural = 'Managers'
        app_label = 'app'
        ordering = ['firstname']

class Employee(models.Model):
    '''
    Model class for Employee
    '''
    firstname = models.CharField('Firstname', max_length=50)
    lastname = models.CharField('Lastname', max_length=50)
    address = models.CharField('address', max_length=200)
    city = models.CharField('address', max_length=75)
    mobile_number = models.CharField('Mobile Number', max_length=20, null=True, blank=True)
    is_active = models.BooleanField('Active', default=False)
    create_date = models.DateTimeField('Joined Time', auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    