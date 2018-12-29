# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.
models_list = [CustomersType , ServicesType, TimeSlot, CustomerDetails,Orders]

admin.site.register(models_list)
