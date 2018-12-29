from django.urls import re_path
from . import views

app_name = 'reservation'

urlpatterns = [
    re_path(r'^$' ,views.Reservation.as_view() , name='reservation-index'),
    re_path(r'^(?P<customer_pk>[0-9]+)/service/$' , views.Service.as_view() , name='reservation-service'),
    re_path(r'^(?P<customer_pk>[0-9]+)/(?P<service_pk>[0-9]+)/date/$' , views.Date.as_view() , name='reservation-date'),
    re_path(r'^(?P<customer_pk>[0-9]+)/(?P<service_pk>[0-9]+)/(?P<timeslot_pk>[0-9]+)/info/$' , views.Info.as_view() , name='reservation-info'),
    re_path(r'^(?P<order_pk>[0-9]+)/confirm/$' , views.Confirm.as_view() , name='reservation-confirm'),
    re_path(r'^(?P<order_pk>[0-9]+)/details/$' , views.Confirm.as_view() , name='reservattion-order-details'),
    re_path(r'^service/(?P<service_pk>[0-9]+)/detail/$' , views.ServiceDetail.as_view() , name='service-detail'),
    re_path(r'^cancelreservation/(?P<order_pk>[0-9]+)/$' , views.cancel_reservation , name='reservation-cancel'),
    re_path(r'^site_admin/order/cancelreservation/(?P<order_pk>[0-9]+)/$' , views.admin_cancel_reservation , name='admin-reservation-cancel'),
    re_path(r'^site_admin/order/ticket/cancelreservation/(?P<ticket_pk>[0-9]+)/$' , views.admin_cancel_ticket_reservation , name='admin-ticket-reservation-cancel'),
    re_path(r'^sendvalidation_email/(?P<order_pk>[0-9]+)/$', views.send_validation_email, name='reservation-send-email'),
    re_path(r'^sendvalidation_sms/(?P<order_pk>[0-9]+)/$' , views.send_validation_sms, name="reservation-send-sms"),
    re_path(r'^sendvalidation_success/$' , views.send_validation_success , name='reservation-send-success'),
    re_path(r'^confirm_reservation/(?P<validation_key>[\w]+)/$' , views.confirm_reservation, name='reservation-confirm-reservation'),
    re_path(r'^ajax/dayrender/' , views.get_dayrender , name='ajax-dayrender'),
    re_path(r'^ajax/dayclick/' , views.get_dayclick, name='ajax-dayclick'),
    re_path(r'^ajax/setinputperson/$' , views.set_inputperson, name='ajax-inputperson'),
    re_path(r'^gen_ics/(?P<order_pk>[0-9]+)/$' , views.GenICS(), name='reservation-genics'),
    re_path(r'^gen_google/(?P<order_pk>[0-9]+)/$' , views.genGoogle , name='reservation-gengoogle')
    
]
