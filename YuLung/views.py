# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect , reverse, get_object_or_404
from django.views.generic import View
from django.views.generic.edit import CreateView , UpdateView , DeleteView
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate , login 
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.safestring import mark_safe
from django.http import HttpResponse , JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from rolepermissions.mixins import HasPermissionsMixin
from rolepermissions.decorators import has_permission_decorator
from rolepermissions.roles import get_user_roles , assign_role , remove_role, clear_roles
from rolepermissions.checkers import has_role
from django.db.models import Q
from forms import *
from models import *
from serializers import *
from reservation.models import *
from reservation.forms import *
import datetime
import pytz
import json
import pandas as pd
import numpy as np

from YuLung.settings import ALLOWED_HOSTS

def index(request):
    last_banner = Banner.objects.all().last()
    site_info = SiteInfo.objects.last()
    seo = SEO.objects.last()
    site = ALLOWED_HOSTS[1]
    
    today = datetime.datetime.now()
    year = today.year
    month = today.month
    
    allTicket = Ticket.objects.filter(order__time_slot__date__year__icontains=year, order__time_slot__date__month__icontains=month)
        
    if allTicket.exists():
        data = []
        for ticket in allTicket:
            data.append({"date":datetime.datetime.combine(ticket.order.time_slot.date,ticket.order.time_slot.start_time),
                         "service_title":ticket.order.service_type.service_title,
                         "customer_count":ticket.order.number_of_customer
                         })
            
        df_ticket = pd.DataFrame(data)
    
    
        table = pd.pivot_table(df_ticket,values="customer_count", index=["date"],columns=["service_title"],aggfunc=sum)
        mask = np.where(~np.isnan(table))
        
        #print table
        #print mask
        
        ind = table.index.values.tolist()
        col = table.columns.values.tolist()
        
        eventData = []
        
        for i in range(len(mask[0])):
            
            if table.iloc[mask[0][i],mask[1][i]] >= 15:
                s = "Full"
            else:
                s = "Remaining " + str(table.iloc[mask[0][i],mask[1][i]])
            
            eventData.append({"start":ind[mask[0][i]],
                             "title":col[mask[1][i]]+s
                             })
    
    else:
        eventData = None
    
    
    return render(request , 'index/index.html', context={'banner_obj':last_banner,
                                                         'current_page':'index',
                                                         'site_info':site_info,
                                                         'seo' : seo,
                                                         'site':site,
                                                         'eventData':eventData
                                                         })

def loginSuccess(request):
    return render(request, 'signin_success.html' , context={})

def loginSuccessRedirect(request):
    return render(request, 'signin_success_redirect.html', context={})

class FAQpage(View):

    template_name = 'faq.html'
    
    def get(self, request):
        faq_list = FAQ.objects.filter(active=True).order_by('priority')
        return render(request, self.template_name , context={'faq_list':faq_list,'current_page':'faq'})


class Comments(View):
    
    template_name = 'comment/comment.html'
    
    def get(self , request):
        
        comment_list = Comment.objects.filter(active=True)
        current_time = datetime.datetime.now(pytz.utc)
        
        return render(request, self.template_name , context={'comment_list':comment_list,
                                                             'current_time':current_time,
                                                             'current_page':'comment'
                                                             })
    
    def post(self, request):
            
        comment_list = Comment.objects.filter(active=True)
        if request.user.is_authenticated():
            
            #user = User.objects.get()
            user = request.user
            comment = Comment.objects.create(title=request.POST.get('title'),
                                             content=request.POST.get('content'),
                                             star = request.POST.get('rating'),
                                             user = user
                                             )
            comment.save()
            current_time = datetime.datetime.now(pytz.utc)
            return render(request, self.template_name, context={'comment_list':comment_list,
                                                                'current_time':current_time,
                                                                'success':True,
                                                                'current_page':'comment'
                                                                })
        current_time = datetime.datetime.now(pytz.utc)
        return render(request, self.template_name, context={'comment_list':comment_list,
                                                            'current_time':current_time,
                                                            'error_msg':"Please Login",
                                                            'current_page':'comment'
                                                            })
    
class MyReservation(View):
    
    template_name = 'my_reservation.html'
    
    
    def get(self, request):
        
        if request.user.is_authenticated():
            
            user = User.objects.get(username=request.user.username)
            order_list = Orders.objects.filter(user=user)
            print order_list
            return render(request, self.template_name, context={'order_list':order_list,'current_page':'my_reservation'})
            
        return render(request , self.template_name , context={'error_msg':'Please Login 1st','current_page':'my_reservation'})
    
    
class SignIn(View):
    
    template_name = 'signin.html'
    form_class = LoginForm
    
    def get(self, request):
        
        form = self.form_class(None)
        return render(request, self.template_name , context={'form':form})
    
    def post(self, request):
        
        form = self.form_class(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
        
            user = authenticate(username=username, password=password)
            print "User = ", user
            if user != None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('login-success')
            return render(request, self.template_name , context={'error_msg':'Incorrect Password or Username', 'form':form})
        return render(request, self.template_name , context={'error_msg':'Invalid Form', 'form':form})


class SignUp(View):

    template_name = 'signup.html'
    form_class = RegisterForm

    def get(self, request):

        form = self.form_class(None)
        return render(request, self.template_name , context={'form':form})

    def post(self, request):

        form = self.form_class(request.POST)

        if form.is_valid():
            
            try:
                user = User.objects.get(username = form.cleaned_data['username'])
                return render(request, self.template_name , context={'error_msg':'Username has been taken', 'form':form}) 
                
            except ObjectDoesNotExist:
                if form.cleaned_data['password'] == form.cleaned_data['password_confirm']:
                    user = User.objects.create_user(username = form.cleaned_data['username'],
                                                    email=form.cleaned_data['username'],
                                                    password=form.cleaned_data['password'])
                    user.save()
                
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('login-success')
                    
                
                return render(request, self.template_name , context={'error_msg':'Unmatched Password', 'form':form})
                
        return render(request, self.template_name , context={'error_msg':'Invalid Form', 'form':form})


def privacy(request):
    return render(request, 'privacy.html' , context={})

def tos(request):
    return render(request, 'tos.html' , context={})


# ============================================================================================================================


class AdminIndex(HasPermissionsMixin, View):

    required_permission = 'view_site_admin'
    template_name = 'admin/index/index.html'

    def get(self, request):
        
        allTicket = Ticket.objects.filter(assigned_to=request.user)
        allOrder = []
        for ticket in allTicket:
            title = ticket.order.time_slot.start_time.strftime("%H:%M") +' '+ ticket.order.service_type.service_title 
            title2 = str(ticket.order.number_of_customer) + ' people'
            allOrder.append({'id':int(ticket.pk),
                             'title':title,
                             'title2':title2,
                             'start':ticket.order.time_slot.date,
                             #'allDay': True,
                             'desciption':ticket.order.__unicode__()
                             })
            
        today = datetime.datetime.now(pytz.timezone('Asia/Taipei'))
        
        weekTicket = Ticket.objects.filter(Q(order__time_slot__date__lte = today) & Q(order__time_slot__date__gte=today-datetime.timedelta(days=7)) & Q(assigned_to=request.user) )
        twoMonthTicket = Ticket.objects.filter(Q(order__time_slot__date__lte = today) & Q(order__time_slot__date__gte=today-datetime.timedelta(days=60)) & Q(assigned_to=request.user))
        finishedTicket = Ticket.objects.filter(Q(finished=True) & Q(assigned_to=request.user))
        
        
        return render(request, self.template_name , context={'allOrder':allOrder,
                                                             'weekTicket':weekTicket,
                                                             'twoMonthTicket':twoMonthTicket,
                                                             'finishedTicket':finishedTicket,
                                                             'allTicket':allTicket
                                                            })
        
class AdminSignIn(View):
    
    template_name = 'admin/login.html'
    form_class = AdminLoginForm
        
    def get(self, request):
        
        form = self.form_class(None)
        return render(request, self.template_name, context={'form':form})
        
    def post(self, request):
        
        form = self.form_class(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
        
            user = authenticate(request, username=username , password=password)
            if user !=None:
                login(request, user)
                return redirect('admin-index')
            
            print "User does not exist"
            
            return render(request, self.template_name, context={'error_msg':'User does not exist'})
        
        print "Invalid Form"
        return render(request, self.template_name , context={'error_msg':'Invalid Form'})
        
        
class AdminBanner( HasPermissionsMixin, View):
    
    required_permission = 'view_site_admin'
    template_name = 'admin/info/basic_banner.html'
    form_class = BannerCreateForm
    

    def get(self, request):

        last_banner = Banner.objects.all().last()
        form = self.form_class(None)
        return render(request, self.template_name, context={'banner':last_banner,
                                                            'form':form
                                                            })
    
    def post(self, request):
        
        form = self.form_class(request.POST , request.FILES)
        last_banner = Banner.objects.all().last()
        
        if form.is_valid():
            banner = Banner.objects.create(banner_image = form.cleaned_data.get('banner_image'),
                                           banner_description = form.cleaned_data.get('banner_description'),
                                           banner_url = form.cleaned_data.get('banner_url')
                                           )
            banner.save()
            
            return redirect('admin-banner')
        
        print 'Form not valid'
        return render(request, self.template_name, context={'banner':last_banner,
                                                            'form':form,
                                                            'error_msg':'Invalid Form'
                                                            })
        
    
class AdminFAQ(HasPermissionsMixin, View):
    
    required_permission = 'view_site_admin'
    template_name = 'admin/info/basic_faq.html'
    form_class = FAQAdminForm

    def get(self, request):
        
        faq_list = FAQ.objects.order_by('priority')    
        form = self.form_class(None)
        return render(request, self.template_name , context={'faq_list':faq_list,
                                                             'form':form
                                                             })


class AdminFAQCreate(HasPermissionsMixin, View):

    required_permission = 'view_site_admin'
    template_name = 'admin/info/faq_form.html'
    form_class = FAQAdminForm
    
    
    def get(self, request):
        
        faq_list = FAQ.objects.order_by('priority')    
        form = self.form_class(None)
        return render(request, self.template_name , context={'faq_list':faq_list,
                                                             'form':form
                                                             })
        
    
    def post(self, request):
        
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin-faq')
            
        faq_list = FAQ.objects.order_by('priority')
        return render(request , self.template_name, context={'faq_list':faq_list,
                                                             'form':form,
                                                             'error_msg':'Invalid Form'
                                                             })
    
    
class AdminFAQEdit(HasPermissionsMixin , UpdateView):
    
    required_permission = 'view_site_admin'
    template_name = 'admin/info/faq_form.html'
    form_class = FAQAdminForm
    model = FAQ
    
    
    def get_context_data(self, *args, **kwargs):
        context = super(AdminFAQEdit, self).get_context_data(*args, **kwargs)
        context['faq_list'] = faq_list = FAQ.objects.order_by('priority')
        context['edit'] = True
        return context

    def get_success_url(self):
        return reverse('admin-faq')
    

@has_permission_decorator('view_site_admin')    
def adminUpdateFAQOrder(request):

    faqOrder = request.GET.getlist('faqOrder[]')

    #print faqOrder

    if faqOrder != "" and faqOrder != None and faqOrder != []:
        
        for i in range(len(faqOrder)):
            faq = FAQ.objects.get(pk=faqOrder[i])
            faq.priority = i
            faq.save()
        
        return HttpResponse("success")
    
    return HttpResponse("fail")

    
@has_permission_decorator('view_site_admin')
def adminFAQDelete(request, pk):
    
    faq = get_object_or_404(FAQ , pk=pk)
    faq.delete()
    return redirect('admin-faq')
    
class AdminSiteInfo(HasPermissionsMixin, View):
    
    required_permission = 'view_site_admin'
    template_name = 'admin/info/basic_info.html'
    form_class = SiteInfoAdminForm
    instance = SiteInfo.objects.last()
    
    def get(self, request):
        
        last_site_info = SiteInfo.objects.last()
        form = self.form_class(instance=self.instance)
        return render(request, self.template_name, context={'form':form})
    
    def post(self, request):
        
        form = self.form_class(request.POST,instance=self.instance)
        if form.is_valid():
            form.save()
            return redirect('admin-siteinfo')
        return render(request, self.template_name, context={'form':form,
                                                            'error_msg':'Invalid Form'})
    
    
class AdminSEO(HasPermissionsMixin, UpdateView):
    
    model = SEO
    required_permission = 'view_site_admin'
    template_name = 'admin/info/basic_seo.html'
    form_class = SEOAdminForm

    
    def get_object(self, queryset=None):
        return SEO.objects.last()
    
    def get_success_url(self):
        return reverse('admin-seo')
        
class AdminService(HasPermissionsMixin, View):
    
    required_permission = 'view_site_admin'
    template_name = 'admin/service/basic_service.html'
    form_class = ServicesTypeCreateForm
    
    def get_success_url(self):
        return reverse('admin-service')
    
    def get(self, request):
        
        service_list = ServicesType.objects.all()
        form = self.form_class(None)
        return render(request, self.template_name, context={'service_list':service_list,
                                                            'form':form
                                                            })
class AdminServiceCreate(HasPermissionsMixin, CreateView):
    
    required_permission = 'view_site_admin'
    form_class = ServicesTypeCreateForm
    model = ServicesType
    template_name = 'admin/service/service_form.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(AdminServiceCreate, self).get_context_data(*args, **kwargs)
        context['service_list'] = ServicesType.objects.values('service_title').all()
        context['new'] = True
        return context        
        
    def get_success_url(self):
        return reverse('admin-service')
        
class AdminServiceEdit(HasPermissionsMixin, UpdateView):
    
    required_permission = 'view_site_admin'
    form_class = ServicesTypeCreateForm
    model = ServicesType
    template_name = 'admin/service/service_form.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(AdminServiceEdit, self).get_context_data(*args, **kwargs)
        context['service_list'] = ServicesType.objects.all()
        context['edit'] = True
        return context
    
    def get_success_url(self):
        return reverse('admin-service')
    
@has_permission_decorator('view_site_admin')
def adminServiceDelete(request, pk):
    
    service = get_object_or_404(ServicesType , pk=pk)
    service.delete()
    return redirect('admin-service')
    
class AdminCustomer(HasPermissionsMixin, View):
    
    required_permission = 'view_site_admin'
    template_name = 'admin/service/basic_customer.html'
    form_class = CustomersTypeForm


    def get(self, request):
        
        customer_list = CustomersType.objects.all()
        form = self.form_class(None)
        
        return render(request, self.template_name, context={'customer_list':customer_list,
                                                            'form':form
                                                            })
        
class AdminCustomerCreate(HasPermissionsMixin, CreateView):

    required_permission = 'view_site_admin'
    template_name = 'admin/service/customer_form.html'
    form_class = CustomersTypeForm
    model = CustomersType
    
    def get_context_data(self, *args, **kwargs):
        context = super(AdminCustomerCreate, self).get_context_data(*args, **kwargs)
        context['customer_list'] = CustomersType.objects.all()
        context['new'] = True
        return context
    
    def get_success_url(self):
        return reverse('admin-customer')
        
class AdminCustomerEdit(HasPermissionsMixin, UpdateView):
    
    required_permission = 'view_site_admin'
    form_class = CustomersTypeForm
    model = CustomersType
    template_name = 'admin/service/customer_form.html'
    
    
    def get_context_data(self, *args, **kwargs):
        context = super(AdminCustomerEdit, self).get_context_data(*args, **kwargs)
        context['customer_list'] = CustomersType.objects.all()
        context['edit'] = True
        return context
    
    def get_success_url(self):
        return reverse('admin-customer')

        
        
@has_permission_decorator('view_site_admin')
def adminCustomerDelete(request, pk):
    
    customer = get_object_or_404(CustomersType , pk=pk)
    customer.delete()
    return redirect('admin-customer')      

class AdminCalendar(HasPermissionsMixin, View):
    
    required_permission = 'view_site_admin'
    template_name = 'admin/calendar/basic_calendar.html'
    
    def get(self, request):
        return render(request, self.template_name, context={})
    
    def post(self, request):
        
        #print request.POST['allWorkingDay']
        #print request.POST['time_slot']
        
        allWoringDay = json.loads(request.POST['allWorkingDay'])
        #print allWoringDay
        
        
        for workingDay in allWoringDay:
            
            
            if TimeSlot.objects.filter(date=workingDay).exists():
                print 'skip'
                continue
            else:
                time_slot_array = json.loads( request.POST['time_slot'])
                for ts in time_slot_array:
                    start_time = ts.get('start_time').split(':')
                    start_time = datetime.time(int(start_time[0]) , int(start_time[1]))
                    #time_slot = TimeSlot.objects.create(date=workingDay , start_time=start_time)
                    time_slot = TimeSlot(date=workingDay,
                                         start_time=start_time,
                                         available_manpower=int(ts.get('available')),
                                         remain_mainpower=int(ts.get('available')),
                                         capacity=int(ts.get('capacity'))
                                         )
                    
                    time_slot.save()
        return HttpResponse('OK')
    
    
@has_permission_decorator('view_site_admin') 
def check_adminDayRender(request):
    
    #print 'checking date', request.GET['date']
    
    date = Q(date=request.GET['date'])
    active = Q(active=True)
    time_slot_list = TimeSlot.objects.filter(date , active)
    today = datetime.datetime.now(pytz.timezone('Asia/Taipei')).strftime('%Y-%m-%d')
    
    if request.GET['date'] < today:
        return HttpResponse('OUTDATED')
    else:
        if len(time_slot_list) > 0:
            return HttpResponse("HASTIMESLOT")
        else:
            return HttpResponse("NOTIMESLOT")
    
    return HttpResponse('ERROR')
    
    
class AdminTimeSlot(HasPermissionsMixin, View):
    
    required_permission = 'view_site_admin'
    template_class = 'admin/calendar/basic_time.html'
    form_class = TimeSlotAdminForm
    
    def get(self, request, date):
        timeslot_list = TimeSlot.objects.filter(date=date)
        form = self.form_class(None)
        return render(request, self.template_class , context={'timeslot_list':timeslot_list,
                                                              'form':form,
                                                              'date':date
                                                              })
    
    def post(self, request, date):
        
        form = self.form_class(request.POST)
        url_date = date
        if form.is_valid():
            
            date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            start_time = form.cleaned_data['start_time']
            available_manpower = form.cleaned_data['available_manpower']
            capacity = form.cleaned_data['capacity']
            active = form.cleaned_data['active']
                    
            time_slot = TimeSlot.objects.create(date=date,start_time=start_time,
                                                available_manpower=available_manpower,
                                                remain_mainpower=available_manpower,
                                                capacity=capacity,
                                                active=active
                                                )
            return redirect('admin-timeslot-date' , date=url_date)
                    
        timeslot_list = TimeSlot.objects.filter(date=date)
        return render(request, self.template_class , context={'timeslot_list':timeslot_list,
                                                              'form':form,
                                                              'date':date
                                                              })
            

    
    

class AdminTimeSlotEdit(HasPermissionsMixin, View):
    
    
    required_permission = 'view_site_admin'
    template_class = 'admin/calendar/basic_time.html'
    form_class = TimeSlotAdminForm
    
    def get(self, request, date, pk):
        
        timeslot_list = TimeSlot.objects.filter(date=date)
        ts = get_object_or_404(TimeSlot , pk=pk)
        form = self.form_class(instance=ts)
        return render(request, self.template_class , context={'timeslot_list':timeslot_list,
                                                              'form':form,
                                                              'date':date,
                                                              'edit':True,
                                                              'ts':ts
                                                              })
    
    def post(self, request, date, pk):
        
        ts = get_object_or_404(TimeSlot , pk=pk)
        form = self.form_class(request.POST, instance=ts)
        if form.is_valid():
            form.save()
            return redirect('admin-timeslot-date' , date=date)
    
        timeslot_list = TimeSlot.objects.filter(date=date)
        return render(request, self.template_class , context={'timeslot_list':timeslot_list,
                                                              'form':form,
                                                              'date':date,
                                                              'edit':True,
                                                              'error_msg':'Invalid Form'
                                                              })
    
@has_permission_decorator('view_site_admin')
def adminTimeSlotDelete(request, date, pk):
    
    ts = get_object_or_404(TimeSlot, pk=pk)
    ts.delete()
    return redirect('admin-timeslot-date' , date=date)
    
@has_permission_decorator('view_site_admin')
def getOrderDetails(request):
    
    order = Orders.objects.get(pk=request.GET['order_pk'])
    
    outJson = {'username':order.user.username,
               'service_title':order.service_type.service_title,
               'status':order.status,
               'name':order.customer_details.name,
               'phone':order.customer_details.phone,
               'email':order.customer_details.email,
               'address':order.customer_details.address
               }
    
    return JsonResponse(outJson)

@has_permission_decorator('view_site_admin')
def getTicketDetails(request):
    
    order = Ticket.objects.get(pk=request.GET['ticket_pk']).order
    
    outJson = {'username':order.user.username,
               'service_title':order.service_type.service_title,
               'status':order.status,
               'name':order.customer_details.name,
               'phone':order.customer_details.phone,
               'email':order.customer_details.email,
               'address':order.customer_details.address
               }
    
    return JsonResponse(outJson)
    
    
class AdminOrder(HasPermissionsMixin, View):
    
    required_permission = 'view_site_admin'
    template_class = 'admin/order/basic_order.html'
    
    def get(self, request):
        confirmed_orders = Orders.objects.filter(status='confirmed').order_by('time_slot__date')
        unfinished_ticket = Ticket.objects.filter(finished=False).order_by('create_at')
        all_user = User.objects.all()
        
        return render(request, self.template_class , context={'confirmed_orders':confirmed_orders,
                                                              'unfinished_ticket':unfinished_ticket,
                                                              'all_user':all_user
                                                              })
        
        
        
    def post(self, request):
        
        order_pk = request.POST.get('order_pk')
        ticket_pk = request.POST.get('ticket_pk')
        assign_to = request.POST.get('assign_to')
        
        #print 'Ticket_pk = ',ticket_pk
        #print 'Order_pk = ', order_pk
        
        if ticket_pk != None and ticket_pk != "":
            
            ticket = Ticket.objects.get(pk=ticket_pk)
            assign_to_user = User.objects.get(pk = assign_to)
            user = request.user
            
            ticket.assigned_by = user
            ticket.assigned_to = assign_to_user
            ticket.save()
            return redirect('admin-order')
        
        
        if order_pk != None and order_pk != "":    
        
            if assign_to != None:
                order = Orders.objects.get(pk=order_pk)
                assign_to_user = User.objects.get(pk = assign_to)
                user = request.user
            
                ticket = Ticket.objects.create(assigned_by=user, assigned_to=assign_to_user,order=order)
                ticket.save()
                order.status = 'completed'
                order.save()
                
                return redirect('admin-order')
        
        
        confirmed_orders = Orders.objects.filter(status='confirmed')
        unfinished_ticket = Ticket.objects.filter(finished=False)
        all_user = User.objects.all()
        
        return render(request, self.template_class, context={'confirmed_orders':confirmed_orders,
                                                              'unfinished_ticket':unfinished_ticket,
                                                              'all_user':all_user,
                                                              'error_msg':'Order/User Error'
                                                              })
        
        
        
class AdminTicket(HasPermissionsMixin, View):
    
    required_permission = 'view_site_admin'
    template_class = 'admin/order/basic_ticket.html'
        
        
    def get(self, request):
        
        allTicket = Ticket.objects.all().order_by('-order__time_slot__date')
        paginator = Paginator(allTicket, 20)
        page = request.GET.get('page')
        try:
            pageTicket = paginator.page(page)
        except PageNotAnInteger:
            pageTicket = paginator.page(1)
        except EmptyPage:
            pageTicket = paginator.page(paginator.num_pages)
        
        return render(request, self.template_class, context={'pageTicket':pageTicket})
        
        

        
@has_permission_decorator('view_site_admin') 
def adminSearchTicket(request):
    
    year = request.GET.get('year')
    month = request.GET.get('month')
    keywords = request.GET.get('keywords')
    
    #print 'Year = ', year
    #print 'Month =', month
    #print 'keywords', keywords
    
    if year=="" and month == "" and keywords == "":
        print "No input"
        return HttpResponse("NULL");
    
    ticketSet = None
    
    if ticketSet == None and year != '':
        ticketSet = Ticket.objects.filter(order__time_slot__date__year = int(year))
        
    
    if month != "" and ticketSet == None:
        ticketSet = Ticket.objects.filter(order__time_slot__date__month = int(month))
    
    elif month !="":
        ticketSet = ticketSet.filter(order__time_slot__date__month = int(month))
    
    
    if keywords != '':
        
        Qname = Q(order__customer_details__name__icontains=keywords)
        Qphone = Q(order__customer_details__phone__icontains=keywords)
        Qemail = Q(order__customer_details__email__icontains=keywords)
        Qcust = Q(order__customer_type__customer_title__icontains=keywords)
        Qser = Q(order__service_type__service_title__icontains=keywords)
        Qassignto = Q(assigned_to__username=keywords)
        Qassignby = Q(assigned_by__username=keywords)
        
        
        if ticketSet == None:
            ticketSet = Ticket.objects.filter(Qname | Qphone| Qemail | Qcust | Qser | Qassignto | Qassignby)
        else:
            ticketSet = ticketSet.filter(Qname | Qphone| Qemail | Qcust | Qser | Qassignto | Qassignby)
    
    #print ticketSet
    if not ticketSet.exists():
        return HttpResponse("NULL");
    else:
        #ticketSetJson = serializers.serialize('json', ticketSet)
        ticketSetSerializer = TicketSerializer(ticketSet, many=True)
        
        return JsonResponse(ticketSetSerializer.data, safe=False)
    
    
    
        
class AdminComment(HasPermissionsMixin, View):
    
    required_permission = 'view_site_admin'
    template_class = 'admin/comment/basic_comment.html'
    
    def get(self, request):
        
        new_comments = Comment.objects.filter(approve=False)
        published_comments = Comment.objects.filter(active=True)
        Q1 = Q(approve=True)
        Q2 = Q(active=False)
        unpublished_comments = Comment.objects.filter(Q1 & Q2)
        
        
        return render(request, self.template_class, context={'new_comments':new_comments,
                                                             'published_comments':published_comments,
                                                             'unpublished_comments':unpublished_comments
                                                             })
    
@has_permission_decorator('view_site_admin')
def adminCommentApprove(request, pk):
    
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve = True
    comment.active = True
    comment.save()
    return redirect('admin-comment')
    
@has_permission_decorator('view_site_admin')        
def adminCommentDisapprove(request, pk):
    
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve = True
    comment.save()
    return redirect('admin-comment')
        
@has_permission_decorator('view_site_admin')
def adminCommentDelete(request, pk):

    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('admin-comment')

        
class AdminStatistic(HasPermissionsMixin, View):
    
    required_permission = 'view_site_admin'
    template_name = 'admin/statistic/basic_statistic.html'
    
    def get(self, request):
        
        earliestYear = Ticket.objects.first().order.time_slot.date.year
        thisYear = datetime.datetime.now().year
        
        return render(request, self.template_name , context={"yearList":range(earliestYear, thisYear+1)})
        
        
        
def getBarPieDataFrame(year, month):
        
    ticketSet = Ticket.objects.filter(order__time_slot__date__year = int(year), order__time_slot__date__month = int(month))
    
    if ticketSet.exists():
        ticketData = []
        
        for t in ticketSet:
            ticketData.append({"service_title":t.order.service_type.service_title,
                               "customer_count":t.order.number_of_customer,
                               "service_fee":t.order.service_type.service_fee
                               })
        
        
        df_ticket = pd.DataFrame(ticketData)
        
        df_ticket = df_ticket.groupby('service_title').agg({'customer_count':sum, "service_fee":sum})
            
        return df_ticket
    else:
        return "NULL"    
    
        
@has_permission_decorator('view_site_admin')        
def adminGetBarChart(request):
    
    year = request.GET.get('year')
    month = request.GET.get('month')

    
    df_ticket = getBarPieDataFrame(year, month)
    
    if isinstance(df_ticket, str):
        return HttpResponse(df_ticket)
    else:
        
        df_ticket['income'] = df_ticket['service_fee'] * df_ticket['customer_count']
        
        outJson = {"labels":df_ticket.index.values.tolist(),
                   "data":df_ticket['customer_count'].values.tolist(),
                   "total_income":df_ticket['income'].sum(),
                   "total_customer":df_ticket['customer_count'].sum()
                   }
        
        return JsonResponse(outJson)
    
    
@has_permission_decorator('view_site_admin')              
def adminGetPieChart(request):
        
    year = request.GET.get('year')
    month = request.GEt.get('month')
        
    df_ticket = getBarPieDataFrame(year, month)
        
    outJson = {"labels":df_ticket.index.values.tolist(),
               "data":df_ticket['customer_count'].values.tolist()
               }
    
    return JsonResponse(outJson)


def getLineDataFrame(year):

    ticketSet = Ticket.objects.filter(order__time_slot__date__year = int(year))

    #print 'ticketSet' , ticketSet
    
    if ticketSet.exists():
        ticketData = []
        
        for t in ticketSet:
            #print 'Ticket pk = ' , t.order
            
            try:
            
                ticketData.append({ "month":t.order.time_slot.date.month,
                                    "service_title":t.order.service_type.service_title,
                                    "customer_count":t.order.number_of_customer,
                                    "customer_title":t.order.customer_type.customer_title
                                    })
        
            except AttributeError:
                continue
        
        df_ticket = pd.DataFrame(ticketData)
        
        return df_ticket
    else:
        return "NULL"


@has_permission_decorator('view_site_admin')
def adminGetLineChartService(request):

    year = request.GET.get('year')
    
    df_ticket = getLineDataFrame(year)
    allServiceTitle = []
    allService = ServicesType.objects.all()
    
    for s in allService:
        allServiceTitle.append(s.service_title)
    
    
    if isinstance(df_ticket, str):
        
        table = pd.DataFrame(0 , index=range(1,13) , columns=allServiceTitle)
        
    else:
    
        table = pd.pivot_table(df_ticket,values="customer_count", index=["month"],columns=["service_title"],aggfunc=sum)
        table = table.reindex(range(1,13))
        table = table.transpose()
        table = table.reindex(allServiceTitle)
        table = table.transpose()
        table = table.fillna(0)
    
    #print table
    
    col_data = []
    
    for column in table:
        col_data.append(table[column].values.tolist())
    
    
    outJson = {"labels":table.columns.values.tolist(),
                "x_labels":table.index.values.tolist(),
                "col_data":col_data,
                }
    
    return JsonResponse(outJson)


def adminGetLineChartCustomer(request):
    
    year = request.GET.get('year')
    
    df_ticket = getLineDataFrame(year)
    allCustomerTitle = []
    allCustomer = CustomersType.objects.all()

    for c in allCustomer:
        allCustomerTitle.append(c.customer_title)

    if isinstance(df_ticket, str):
        table = pd.DataFrame(0, index=range(1,13) , columns=allCustomerTitle)
    else:
        table = pd.pivot_table(df_ticket,values="customer_count", index=["month"],columns=["customer_title"],aggfunc=sum)
        table = table.reindex(range(1,13))
        table = table.transpose()
        table = table.reindex(allCustomerTitle)
        table = table.transpose()
        table = table.fillna(0)
        
    col_data = []
    
    for column in table:
        col_data.append(table[column].values.tolist())
    
    
    outJson = {"labels":table.columns.values.tolist(),
                "x_labels":table.index.values.tolist(),
                "col_data":col_data,
                }
    
    return JsonResponse(outJson)

        
@has_permission_decorator('view_site_admin')
def adminGetUserTicket(request):
        
    allTicket = Ticket.objects.filter(assigned_to=request.user)
    allOrder = []
    for ticket in allTicket:
        allOrder.append(ticket.order)
    
    allOrder = serializers.serialize('json', allOrder)
    print allOrder
    return JsonResponse(allOrder, safe=False)
        
        
class AdminDataExport(HasPermissionsMixin, View):
    
    required_permission = 'view_site_admin'
    template_name = 'admin/statistic/basic_download.html'
        
        
    def get(self, request):
        
        return render(request, self.template_name, context={})
        
        
class AdminUserAccount(HasPermissionsMixin, View):
        
    required_permission = 'view_site_admin'
    template_name = 'admin/user/basic_account.html'
    form_class = AdminUserCreateForm
        
    def get(self, request):
        
        allUser = User.objects.all()
        
        roleUser = []
        
        for user in allUser:
            if get_user_roles(user) != []:
                roleUser.append(user)
        
        form = self.form_class(None)
        
        return render(request, self.template_name, context={"roleUser":roleUser,'form':form})
        
        
        
    def post(self, request):
        
        #print "POST!!!"
        form = self.form_class(request.POST)
        
        allUser = User.objects.all()
        roleUser = []
            
        for user in allUser:
            if get_user_roles(user) != []:
                roleUser.append(user)
        
        
        
        if form.is_valid():            
            username = form.cleaned_data['username']
            
            try:
                user = User.objects.get(username=username)
                return render(request, self.template_name, context={"roleUser":roleUser,'form':form, 'error_msg':'Username has been taken'})
            except User.DoesNotExist:
                password = form.cleaned_data['password']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                
                user = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email)
                user.set_password(password)
                user.save()
                print request.POST.get('role')
                assign_role(user, request.POST.get('role'))
    
                return redirect('admin-user-account')



        return render(request, self.template_name, context={"roleUser":roleUser,'form':form, 'error_msg':'invalid form'})


@has_permission_decorator('view_site_admin')
def adminGetUserAccount(request):

    username = request.GET.get('username')
    user = User.objects.get(username=username)

    role = get_user_roles(user)
    if role == []:
        return HttpResponse("non-admin")

    outJson = {'first_name':user.first_name,
               'last_name':user.last_name,
               'email':user.email,
               'role':role[0].get_name()
               }
    
    return JsonResponse(outJson)

@csrf_protect
@has_permission_decorator('view_site_admin')
def adminUserAccountEdit(request):

    requestUser = User.objects.get(username=request.user.username)
    if has_role(requestUser, 'manager'):

        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        role = request.POST.get('role')
        
        user = User.objects.get(username=username)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        
        clear_roles(user)
        assign_role(user, role)
        
        return HttpResponse("success")
    else:
        return HttpResponse("no permission")

@csrf_protect
@has_permission_decorator('view_site_admin')
def adminUserAccountDelete(request):
    
    requestUser = User.objects.get(username=request.user.username)
    if has_role(requestUser, 'manager'):
        
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        user.delete()
        
        return HttpResponse("success")
    else:
        return HttpResponse("no permission")
    
    
class AdmonUserProfile(HasPermissionsMixin, View):
    
    required_permission = 'view_site_admin'
    template_name = 'admin/user/alter_personalinfo.html'
    
    def get(self, request):
        
        return render(request, self.template_name, context={})
        
        
    def post(self, request):
        
        user = User.objects.get(username=request.user.username)
        
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        
        if request.POST.get('password') != "":
            user.set_password(request.POST.get('password'))
        
        user.save()
    
        return redirect('admin-user-profile')
    
@has_permission_decorator('view_site_admin')
def adminGetRecordCount(request):
    
    yearFrom = request.GET.get('yearFrom')
    yearTo = request.GET.get('yearTo')
    monthFrom = request.GET.get('monthFrom')
    monthTo = request.GET.get('monthTo')
    
    if yearFrom != None and yearTo != None and monthFrom != None and monthTo !=None:
        fromDate = datetime.date(int(yearFrom), int(monthFrom), 1)
        toDate = datetime.date(int(yearTo) + (int(monthTo) == 12), (int(monthTo) + 1 if int(monthTo) < 12 else 1), 1) - datetime.timedelta(1)
    
        ticketSet = Ticket.objects.filter(order__time_slot__date__gte = fromDate, order__time_slot__date__lte = toDate)
    
        count = str(ticketSet.count())
        return HttpResponse(count)
    
    return HttpResponse("0")
    
    
    



