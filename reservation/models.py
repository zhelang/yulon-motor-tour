# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator , validate_email, RegexValidator
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField

# Create your models here.

class ServicesType(models.Model):
    #service_type_image = models.ImageField(upload_to='services_type_image')
    service_type_image = ImageField(upload_to='services_type_image')
    service_title = models.CharField(max_length=255)
    service_description = models.CharField(max_length=1024)
    session_time_length = models.DecimalField(max_digits=4 , decimal_places=2 , validators=[MinValueValidator(0.0) , MaxValueValidator(9.0)])
    service_code = models.CharField(max_length=5)
    service_note = models.CharField(max_length=1024,null=True)
    service_fee = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    for_family = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.service_code + '-' + self.service_title


class CustomersType(models.Model):
    #customers_type_image = models.ImageField(upload_to='customers_type_image')
    customers_type_image = ImageField(upload_to='customers_type_image')
    customer_title = models.CharField(max_length=255)
    customer_description = models.CharField(max_length=1024)
    #session_time_lenth = models.DecimalField(max_digits=4 , decimal_places=2, validators=[MinValueValidator(0.0) , MaxValueValidator(9.0)])
    customer_code = models.CharField(max_length=5)
    available_service = models.ManyToManyField(ServicesType)
    active = models.BooleanField(default=True)
    
    def __unicode__(self):
        #s = u''.join( (self.customer_code + '-' + self.customer_title.encode('ascii',errors='replace')))
    #return s.encode('utf-8').strip()
       return self.customer_code + '-' + self.customer_title


class TimeSlot(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)
    available_manpower = models.IntegerField(validators=[MinValueValidator(0)])
    remain_mainpower = models.IntegerField(validators=[MinValueValidator(0)])    
    capacity = models.IntegerField(validators=[MinValueValidator(0)] ,default=0)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return str(self.date) + ' | ' + str( self.start_time)



class CustomerDetails(models.Model):
    
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=u'行動電話號碼格式必須是「0910123456」或「+886910123456」，請再次確認電話號碼。')
    
    name = models.CharField(max_length=255)
    email = models.EmailField(validators=[validate_email])
    phone = models.CharField(max_length=16, validators=[phone_regex])
    phone2 = models.CharField(max_length=16, blank=True)
    address = models.CharField(max_length=255,blank=True)

    def __unicode__(self):
        return self.name + ' - ' + self.email + ' - ' + self.phone


class Orders(models.Model):
    customer_type = models.ForeignKey(CustomersType, on_delete=models.CASCADE, null=True)
    service_type = models.ForeignKey(ServicesType, on_delete=models.CASCADE, null=True)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, null=True)
    customer_details = models.ForeignKey(CustomerDetails, on_delete=models.CASCADE, null=True)
    number_of_customer = models.IntegerField(null=True , validators=[MinValueValidator(0)])
    code = models.CharField(max_length=15,null=True , unique=True)
    status = models.CharField(max_length=25, default="unconfirmed")
    user = models.ForeignKey(User , on_delete=models.CASCADE, null=True)
    validation_key = models.CharField(max_length=30, null=True)

    def __unicode__(self):
        return str(self.code) + ' || '# + self.time_slot.__unicode__()

