from django.conf.urls import url
import views

app_name = 'reservation'

urlpatterns = [
    url(r'^$' ,views.Reservation.as_view() , name='reservation-index'),
    url(r'^(?P<customer_pk>[0-9]+)/service/$' , views.Service.as_view() , name='reservation-service'),
    url(r'^(?P<customer_pk>[0-9]+)/(?P<service_pk>[0-9]+)/date/$' , views.Date.as_view() , name='reservation-date'),
    url(r'^(?P<customer_pk>[0-9]+)/(?P<service_pk>[0-9]+)/(?P<timeslot_pk>[0-9]+)/info/$' , views.Info.as_view() , name='reservation-info'),
    url(r'^(?P<order_pk>[0-9]+)/confirm/$' , views.Confirm.as_view() , name='reservation-confirm'),
    url(r'^(?P<order_pk>[0-9]+)/details/$' , views.Confirm.as_view() , name='reservattion-order-details'),
    url(r'^service/(?P<service_pk>[0-9]+)/detail/$' , views.ServiceDetail.as_view() , name='service-detail'),
    url(r'^cancelreservation/(?P<order_pk>[0-9]+)/$' , views.cancel_reservation , name='reservation-cancel'),
    url(r'^site_admin/order/cancelreservation/(?P<order_pk>[0-9]+)/$' , views.admin_cancel_reservation , name='admin-reservation-cancel'),
    url(r'^site_admin/order/ticket/cancelreservation/(?P<ticket_pk>[0-9]+)/$' , views.admin_cancel_ticket_reservation , name='admin-ticket-reservation-cancel'),
    url(r'^sendvalidation_email/(?P<order_pk>[0-9]+)/$', views.send_validation_email, name='reservation-send-email'),
    url(r'^sendvalidation_sms/(?P<order_pk>[0-9]+)/$' , views.send_validation_sms, name="reservation-send-sms"),
    url(r'^sendvalidation_success/$' , views.send_validation_success , name='reservation-send-success'),
    url(r'^confirm_reservation/(?P<validation_key>[\w]+)/$' , views.confirm_reservation, name='reservation-confirm-reservation'),
    url(r'^ajax/dayrender/' , views.get_dayrender , name='ajax-dayrender'),
    url(r'^ajax/dayclick/' , views.get_dayclick, name='ajax-dayclick'),
    url(r'^ajax/setinputperson/$' , views.set_inputperson, name='ajax-inputperson'),
    url(r'^gen_ics/(?P<order_pk>[0-9]+)/$' , views.GenICS(), name='reservation-genics'),
    url(r'^gen_google/(?P<order_pk>[0-9]+)/$' , views.genGoogle , name='reservation-gengoogle')
    
]
