# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views.generic import View
from django.views.generic.edit import CreateView , UpdateView , DeleteView
from django.views.generic.list import ListView
from django.views.decorators.cache import never_cache
from django.http import HttpResponse , HttpResponseNotFound , JsonResponse
import json
from django.core import serializers
from django.core.mail import send_mail
from django.db.models import Q
from rolepermissions.decorators import has_permission_decorator
from forms import *
from models import *
from YuLung.models import Ticket
import random , string
import datetime, pytz
from every8dsms import *
from django_cal.views import Events
import dateutil.rrule as rrule
from YuLung.settings import ALLOWED_HOSTS
from YuLung.models import EmailTemplate
import re

class Reservation(ListView):
    template_name = 'order/reservation.html'

    @never_cache
    def get(self, request):
        object_list = CustomersType.objects.filter(active=True)
        return render(request , self.template_name, context={'object_list':object_list})


class Service(View):
    template_name = 'order/service.html'

    @never_cache
    def get(self, request, customer_pk):
        selected_customer = get_object_or_404(CustomersType , pk=customer_pk)
        #object_list = ServicesType.objects.filter(active=True)
        object_list = selected_customer.available_service.filter(active=True)
        return render(request , self.template_name, context={'object_list':object_list,
                                                             'customer_pk':customer_pk,
                                                             'selected_customer_title':selected_customer.customer_title
                                                             })

class ServiceDetail(View):
    template_name = 'order/service_detail.html'

    def get(self, request, service_pk):
        service_id = get_object_or_404(ServicesType, pk=service_pk)
        return render(request , self.template_name, context={'service':service_id})
    
class Date(View):
    template_name = 'order/date.html'
    
    @never_cache
    def get(self, request, customer_pk , service_pk):
        selected_customer = get_object_or_404(CustomersType , pk=customer_pk)
        selected_service = get_object_or_404(ServicesType, pk=service_pk)
        option = range(1, 15)
        return render(request , self.template_name , context={'selected_service':selected_service,
                                                              'customer_pk':customer_pk,
                                                              'service_pk':service_pk,
                                                              'selected_customer_title':selected_customer.customer_title,
                                                              'option':option
                                                              })
        
    
def get_dayrender(request):
    date = Q(date=request.GET['date'])
    active = Q(active=True)
    time_slot_list = TimeSlot.objects.filter(date , active).order_by('start_time')
    
    today = datetime.datetime.now(pytz.timezone('Asia/Taipei')).strftime('%Y-%m-%d')
    
    #print today
    
    if request.GET['date'] < today:
        for ts in time_slot_list:
            ts.active = False
            ts.save()
        return HttpResponse("OUTDATED")
    else:
        if len(time_slot_list) == 0:
            return HttpResponse("NO TIME SLOT")
        else:
            data = {}
            data['event'] = []
            for ts in time_slot_list:
                event = dict()
                event['date'] = str(ts.date)
                event['time'] = str(ts.start_time.isoformat())
                event['capacity'] = ts.capacity
                orders_list = Orders.objects.filter(time_slot=ts)
                if len(orders_list) > 0:
                    for order in orders_list:
                        event['title'] = order.service_type.service_title
                        event['id'] = order.service_type.id
                        event['cid'] = order.customer_type.id
                data['event'].append(event)
            return HttpResponse(json.dumps(data), content_type='application/json')
            #remain_manpower = 0
            #for ts in time_slot_list:
            #    remain_manpower += ts.remain_mainpower
            #if remain_manpower == 0:
            #    return HttpResponse("FULL")
            #else:
            #    return HttpResponse("OK")
            
    #print "get time slot ", request.GET['date']
    
    
    
def get_dayclick(request):
    date = Q(date=request.GET['date'])
    active = Q(active=True)
    time_slot_list = TimeSlot.objects.filter(date , active)
    if len(time_slot_list) == 0:
        return HttpResponse("NO TIME SLOT")
    else:
        return HttpResponse(serializers.serialize('json',time_slot_list))
    
def set_inputperson(request):
    if (request.GET['person_number'] != None):
        request.session['person_number'] = request.GET['person_number']
        return HttpResponse('OK')
    else:
        return HttpResponse('Error:person number cannot be null!' , status=401)
    
    
class Info(View):
    template_name = 'order/info.html'
    form_class = CustomerDetailsForm
    
    @never_cache
    def get(self, request, customer_pk, service_pk, timeslot_pk):

        form=self.form_class(None)

        selected_customer = get_object_or_404(CustomersType , pk=customer_pk)
        selected_service = get_object_or_404(ServicesType, pk=service_pk)
        selected_timeslot = get_object_or_404(TimeSlot, pk=timeslot_pk)
        
        if (request.user.is_authenticated()):
            user_name = request.user.username
            form=self.form_class(initial={'email':request.user.email})
        else:
            user_name = None      
        
        
        if request.session.get('person_number') != None:
            return render(request , self.template_name , context={'selected_service_title':selected_service.service_title,
                                                                  'selected_service_note':selected_service.service_note,
                                                                  'selected_service_obj':selected_service,
                                                                  'customer_pk':customer_pk,
                                                                  'service_pk':service_pk,
                                                                  'timeslot_pk':timeslot_pk,
                                                                  'selected_customer_title':selected_customer.customer_title,
                                                                  'selected_timeslot':selected_timeslot,
                                                                  'form':form,
                                                                  'user_name':user_name
                                                                  })
        else:
            return render(request , self.template_name , context={'selected_service_title':selected_service.service_title,
                                                                  'selected_service_note':selected_service.service_note,
                                                                  'selected_service_obj':selected_service,
                                                                  'customer_pk':customer_pk,
                                                                  'service_pk':service_pk,
                                                                  'timeslot_pk':timeslot_pk,
                                                                  'selected_customer_title':selected_customer.customer_title,
                                                                  'selected_timeslot':selected_timeslot,
                                                                  'form':form,
                                                                  'user_name':user_name,
                                                                  'error_msg':"NULL PERSON NUMBER"
                                                                  })
        

    def post(self, request, customer_pk, service_pk, timeslot_pk):
        form=self.form_class(request.POST)
        error_msg = []
        
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            phone2 = form.cleaned_data['phone2']
            address = form.cleaned_data['address']

            customer_details = CustomerDetails.objects.create(name=name, email=email, phone=phone, phone2=phone2, address=address)
            customer_details.save()

            order = Orders(customer_type=CustomersType.objects.get(pk=customer_pk),
                                          service_type=ServicesType.objects.get(pk=service_pk),
                                          time_slot=TimeSlot.objects.get(pk=timeslot_pk),
                                          customer_details=customer_details
                                          )
            flag_ErrPersonNume = False
            if order.time_slot.capacity - int(request.session['person_number']) >= 0:
                order.time_slot.capacity = order.time_slot.capacity - int(request.session['person_number'])
                order.number_of_customer = int(request.session['person_number'])
                order.time_slot.save()
                request.session['person_number'] = None
            else:
                error_msg.append("Incorrect Person Number")
                flag_ErrPersonNume = True

            if request.user.is_authenticated():
                order.user = request.user

            date_str = datetime.datetime.now().strftime('%Y%m%d')
            
            # TODO check b4 save
            
            if flag_ErrPersonNume != True:
                try:
                    last_order_num = Orders.objects.last().code[-7:]
                    code = date_str + str(int(last_order_num) + 1).zfill(7)
                    #order.code = ''.join(random.choice(string.ascii_uppercase + string.digits) for k in range(7))
                    order.code = code
                    order.validation_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for k in range(30))
                    order.save()
                except:
                    #order.code = ''.join(random.choice(string.ascii_uppercase + string.digits) for k in range(7))
                    order.code = date_str + "0000000"
                    order.validation_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for k in range(30))
                    order.save()
                
            
                
            if error_msg == []:
                
                return redirect('reservation:reservation-confirm', order_pk=order.pk)

        selected_customer = get_object_or_404(CustomersType , pk=customer_pk)
        selected_service = get_object_or_404(ServicesType, pk=service_pk)
        selected_timeslot = get_object_or_404(TimeSlot, pk=timeslot_pk)
        #selected_service = ServicesType.objects.get(pk=request.session['selected_service_id'])
        return render(request , self.template_name , context={'selected_service_title':selected_service.service_title,
                                                              'selected_service_note':selected_service.service_note,
                                                              'selected_service_obj':selected_service,
                                                              'customer_pk':customer_pk,
                                                              'service_pk':service_pk,
                                                              'timeslot_pk':timeslot_pk,
                                                              'selected_customer_title':selected_customer.customer_title,
                                                              'selected_timeslot':selected_timeslot,
                                                              'form':form,
                                                              'error_msg':error_msg
                                                              })


class Confirm(View):
    
    template_name = 'order/confirm.html'
    
    @never_cache
    def get(self, request, order_pk):
        order = get_object_or_404(Orders, pk=order_pk)
        return render(request , self.template_name, context={'order':order})

class OrderDetails(View):

    template_name = 'order/details.html'

    @never_cache
    def get(self, request, order_pk):
        order = get_object_or_404(Orders, pk=order_pk)
        return render(request , self.template_name, context={'order':order})

@has_permission_decorator('view_site_admin')
def admin_cancel_reservation(request, order_pk):
    order = get_object_or_404(Orders, pk=order_pk)
    order.time_slot.capacity = order.time_slot.capacity + order.number_of_customer
    order.time_slot.save()
    order.status = "cancelled"
    order.save()
    return redirect('admin-order')

@has_permission_decorator('view_site_admin')
def admin_cancel_ticket_reservation(request, ticket_pk):
    ticket = get_object_or_404(Ticket, pk=ticket_pk)
    ticket.order.time_slot.capacity = ticket.order.time_slot.capacity + ticket.order.number_of_customer
    ticket.order.time_slot.save()
    ticket.order.status = "cancelled"
    ticket.order.save()
    ticket.delete()
    return redirect('admin-order')

def cancel_reservation(request, order_pk):
    if (request.user.is_authenticated()):
        user = User.objects.get(username = request.user.username)
        order = get_object_or_404(Orders, pk=order_pk)
        if (order.user == user):
            order.time_slot.capacity = order.time_slot.capacity + order.number_of_customer 
            order.time_slot.save()
            order.status = "cancelled"
            order.save()
            
            return render(request, 'order/cancel_success.html')
    return HttpResponseNotFound("Page Not Found")
        
def send_validation_email(request , order_pk):
    order = Orders.objects.get(pk=order_pk)
    validation_key = order.validation_key
    to_email = order.customer_details.email
    email_template = EmailTemplate.objects.last()
    email_template.email_content.format(ALLOWED_HOSTS[0],validation_key).encode('utf-8').decode('string_escape')
   
    send_mail(
        unicode(email_template.subject.format(order.code)).encode('utf-8'),
        #unicode(email_template.email_content.format(ALLOWED_HOSTS[0],validation_key).decode('string_escape')).encode('utf-8'),
        email_template.email_content.format(ALLOWED_HOSTS[0],validation_key).encode('utf-8').decode('string_escape').decode('utf-8'),
        email_template.from_email,
        [to_email],
        fail_silently=False,
    )
 
    return redirect('reservation:reservation-send-success')
    
def send_validation_sms(reuqest, order_pk):
    order = Orders.objects.get(pk=order_pk)
    validation_key = order.validation_key
    to_phone = order.customer_details.phone
    to_phone2 = order.customer_details.phone2
    email_template = EmailTemplate.objects.last()
    msg = email_template.email_content.format(ALLOWED_HOSTS[0],validation_key).encode('utf-8').decode('string_escape').decode('utf-8')

    sms = every8dsms()
    sms.login('didier', '03489200')
    sms.send_message('', msg, to_phone, '', '')

    if (to_phone2 != None):
        #to_phone2 = re.findall(r'^\+?1?\d{9,15}$', phone2)
        sms2 = every8dsms()
        sms2.login('didier', '03489200')
        sms2.send_message('', msg, to_phone2, '', '')

    return redirect('reservation:reservation-send-success')
    
def send_validation_success(request):
    return render(request, 'order/validation_letter_sent.html',context={})
    
def confirm_reservation(request, validation_key):
    
    # "unconfirmed" , "confirmed" , "occupy"

    print "validation_key =" , validation_key    
    order = get_object_or_404(Orders , validation_key=validation_key)
    if order.status == 'unconfirmed':
        order.status = "confirmed"
    order.save()
    
    #return redirect('reservation:reservation-confirm', order_pk=order.pk)
    return render(request, 'order/email_confirm.html' , context={'order':order})
    
class GenICS(Events):

    def get_object(self, request, order_pk):
        return Orders.objects.get(pk=order_pk)
    
    def items(self , obj):
        return [obj]
    
    def item_summary(self, item):
        return item.service_type.service_title

    
    def item_start(self, item):
        return datetime.datetime.combine(item.time_slot.date , item.time_slot.start_time)
    
    def item_end(self, item):
        if item.time_slot.end_time == None:
            duration = item.service_type.session_time_length
            end_time = self.item_start(item) + datetime.timedelta(hours=int(duration),
                                                                      minutes= int(duration - int(duration)) * 60 )
            
            return end_time
        else:
            return datetime.datetime.combine(item.time_slot.date , item.time_slot.end_time)
        
    def item_description(self, item):
        return item.service_type.service_description
    
    def item_location(self,item):
        return u'367 苗栗縣三義鄉尖豐公路39-1號'
    
    
def genGoogle(request, order_pk):
    
    order = get_object_or_404(Orders, pk=order_pk)
    
    local = pytz.timezone('Asia/Taipei')
    
    start_time = datetime.datetime.combine(order.time_slot.date , order.time_slot.start_time)
    duration = order.service_type.session_time_length
    end_time = start_time + datetime.timedelta(hours=int(duration),minutes= int(duration - int(duration)) * 60 )
    
    start_time = (local.localize(start_time, is_dst=None)).astimezone(pytz.utc)
    end_time = (local.localize(end_time, is_dst=None)).astimezone(pytz.utc)
    
    outJSON = {'summary':order.service_type.service_title,
               'location':u'367 苗栗縣三義鄉尖豐公路39-1號',
               'description':order.service_type.service_description,
               'start':{'dateTime':start_time.strftime('%Y%m%dT%H%M%SZ'),'timeZone':'Asia/Taipei'},
               'end':{'dateTime':end_time.strftime('%Y%m%dT%H%M%SZ'), 'timeZone':'Asia/Taipei'}
               }

    return JsonResponse(outJSON)
    
    
