# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import (
    CustomerDetails,
    CustomersType,
    Orders,
    ServicesType,
    TimeSlot
)

# Register your models here.
admin.site.register(CustomerDetails)
admin.site.register(CustomersType)
admin.site.register(Orders)
admin.site.register(ServicesType)
admin.site.register(TimeSlot)
