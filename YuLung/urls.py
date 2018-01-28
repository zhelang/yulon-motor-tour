"""YuLung URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url , include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index , name='index' ),
    url(r'^reservation/' , include('reservation.urls')),
    url(r'^comments/$' , views.Comments.as_view(), name='comments'),
    url(r'^my_reservation/$' , views.MyReservation.as_view(), name='my_reservation'),
    url(r'^signin/$', views.SignIn.as_view(), name='sign-in'),
    url(r'^signup/$', views.SignUp.as_view(), name='sign-up'),
    url(r'^#_=_login/success/$', views.loginSuccess, name='login-success'),
    url(r'^login/success/$' , views.loginSuccessRedirect, name='login-success-redirect'),
    url(r'^faq/$' , views.FAQpage.as_view() , name='faq'),
    url(r'^privacy/$' , views.privacy , name='privacy'),
    url(r'^tos/$' , views.tos , name='tos'),

    
    url(r'^site_admin/$' , views.AdminIndex.as_view() , name='admin-index'),
    url(r'^site_admin/login/$' , views.AdminSignIn.as_view() , name='admin-login'),
    url(r'^site_admin/info/banner/$' , views.AdminBanner.as_view() , name='admin-banner'),
    url(r'^site_admin/info/faq/$' , views.AdminFAQ.as_view() , name='admin-faq'),
    url(r'^site_admin/info/faq/new/$' , views.AdminFAQCreate.as_view() , name='admin-faq-create'),
    url(r'^site_admin/info/faq/(?P<pk>[0-9]+)/$' , views.AdminFAQEdit.as_view(), name = 'admin-faq-edit'),
    url(r'^site_admin/info/faq/(?P<pk>[0-9]+)/delete/$' , views.adminFAQDelete, name = 'admin-faq-delete'),
    url(r'^site_admin/info/settings/$', views.AdminSiteInfo.as_view() , name='admin-siteinfo'),
    url(r'^site_admin/info/seo/$' , views.AdminSEO.as_view() , name='admin-seo'),
    url(r'^site_admin/service/course/$', views.AdminService.as_view(), name='admin-service'),
    url(r'^site_admin/service/course/new/$', views.AdminServiceCreate.as_view(), name='admin-service-create'),
    url(r'^site_admin/service/course/(?P<pk>[0-9]+)/$' , views.AdminServiceEdit.as_view() , name='admin-service-edit'),
    url(r'^site_admin/service/course/(?P<pk>[0-9]+)/delete/$' , views.adminServiceDelete, name='admin-service-delete'),
    url(r'^site_admin/service/customer/$' , views.AdminCustomer.as_view(), name='admin-customer'),
    url(r'^site_admin/service/customer/new/$' , views.AdminCustomerCreate.as_view(), name='admin-customer-create'),
    url(r'^site_admin/service/customer/(?P<pk>[0-9]+)/$' , views.AdminCustomerEdit.as_view() , name='admin-customer-edit'),
    url(r'^site_admin/service/customer/(?P<pk>[0-9]+)/delete/$' , views.adminCustomerDelete, name='admin-customer-delete'),
    url(r'^site_admin/calendar/$' , views.AdminCalendar.as_view(), name='admin-calendar'),
    
    url(r'^site_admin/calendar/time_slot/$' , views.AdminTimeSlot.as_view(), name='admin-timeslot'),
    url(r'^site_admin/calendar/time_slot/(?P<date>[0-9]{4}-?[0-9]{2}-?[0-9]{2})/$' , views.AdminTimeSlot.as_view(), name='admin-timeslot-date'),
    url(r'^site_admin/calendar/time_slot/(?P<date>[0-9]{4}-?[0-9]{2}-?[0-9]{2})/edit/(?P<pk>[0-9]+)/$' , views.AdminTimeSlotEdit.as_view(), name='admin-timeslot-date-edit'),
    url(r'^site_admin/calendar/time_slot/(?P<date>[0-9]{4}-?[0-9]{2}-?[0-9]{2})/delete/(?P<pk>[0-9]+)/$' , views.adminTimeSlotDelete, name='admin-timeslot-date-delete'),
    
    url(r'^site_admin/order/$' , views.AdminOrder.as_view(), name='admin-order'),
    
    url(r'^site_admin/ticket/$', views.AdminTicket.as_view(), name='admin-ticket'),
    
    
    
    
    url(r'^site_admin/comment/$' , views.AdminComment.as_view(), name='admin-comment'),
    url(r'^site_admin/comment/(?P<pk>[0-9]+)/approve/$' , views.adminCommentApprove, name='admin-comment-approve'),
    url(r'^site_admin/comment/(?P<pk>[0-9]+)/disapprove/$' , views.adminCommentDisapprove, name='admin-comment-disapprove'),
    url(r'^site_admin/comment/(?P<pk>[0-9]+)/delete/$' , views.adminCommentDelete, name='admin-comment-delete'),

    url(r'^site_admin/statistic/$' , views.AdminStatistic.as_view() , name='admin-statistic'),


    url(r'ajax/order/$' , views.getOrderDetails, name='ajax-get-order'),
    url(r'ajax/ticket/$' , views.getTicketDetails, name='ajax-get-ticket'),
    url(r'ajax/check_dayrender' , views.check_adminDayRender, name='ajax-admin-dayrender'),
    url(r'ajax/get_user_ticket', views.adminGetUserTicket, name='ajax-admin-get-ticket'),
    url(r'ajax/search_ticket/$' , views.adminSearchTicket, name='ajax-admin-search-ticket'),

    url(r'ajax/get_barchart/$' , views.adminGetBarChart, name='ajax-admin-get-barchart'),
    url(r'ajax/get_piechart/$' , views.adminGetPieChart, name='ajax-admin-get-piechart'),


    url(r'^oauth/', include('social_django.urls', namespace='social')),
    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


