from rest_framework import serializers as rest_serializers
from django.contrib.auth.models import User
from reservation.models import *
from models import *

class UserSerializer(rest_serializers.ModelSerializer):
        
    class Meta:
        model = User
        fields = ['username']
        
        
class TimeSlotSerializer(rest_serializers.ModelSerializer):
        
    date = rest_serializers.DateField(format="%Y-%m-%d")
    
    class Meta:
        model = TimeSlot
        fields = ['date']
        
        
class CustomerTypeSerializer(rest_serializers.ModelSerializer):
    
    class Meta:
        model = CustomersType
        fields = ['customer_title']
        
        
class CustomerDetailsSerializer(rest_serializers.ModelSerializer):

    class Meta:
        model = CustomerDetails
        fields = ['name' , 'email' , 'phone']


class ServiceTypeSerializer(rest_serializers.ModelSerializer):

    class Meta:
        model = ServicesType
        fields = ['service_title']


class OrderSerializer(rest_serializers.ModelSerializer):

    time_slot = TimeSlotSerializer(read_only=True)
    customer_details = CustomerDetailsSerializer(read_only=True)
    customer_type = CustomerTypeSerializer(read_only=True)
    service_type = ServiceTypeSerializer(read_only=True)

    class Meta:
        model = Orders
        fields = ['code' , 'customer_details' , 'customer_type' , 'time_slot', 'service_type']

        
class TicketSerializer(rest_serializers.ModelSerializer):
    
    assigned_to = UserSerializer(read_only=True)
    assigned_by = UserSerializer(read_only=True)
    order = OrderSerializer(read_only=True)
    create_at = rest_serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    last_modified = rest_serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    
    
    class Meta:
        model = Ticket
        fields = '__all__'
        depth = 2