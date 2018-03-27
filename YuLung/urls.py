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
from django.http import HttpResponse
from django.conf.urls import url , include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.sitemaps.views import sitemap
from YuLung.sitemaps import StaticSitemap
#from reservation.sitemaps import ReservationSitemap
from django.conf import settings
from django.conf.urls.static import static
import views

sitemaps = {
    'static': StaticSitemap,
#    'reservation': ReservationSitemap,
#    'dynamic': DynamicSitemap
}

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
    url(r'^my/$' , views.MyPage.as_view() , name='my'),
    
    url(r'^user/personalinfo/$' , views.UserInfo.as_view(), name='user-profile'),
    
    url(r'^password/reset/$',views.PasswordReset.as_view(), name='front_password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, {'template_name':'password_reset_done.html'} ,name='front_password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.PasswordResetConfirm.as_view(), name='front_password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, {'template_name':'password_set_complete.html'} , name='front_password_reset_complete'),
    
    
    url(r'^site_admin/$' , views.AdminIndex.as_view() , name='admin-index'),
    url(r'^site_admin/login/$' , views.AdminSignIn.as_view() , name='admin-login'),
    url(r'^site_admin/logout/$', views.adminLogout, name='admin-logout'),
    url(r'^site_admin/info/banner/$' , views.AdminBanner.as_view() , name='admin-banner'),
    
    url(r'^site_admin/password/reset/$',views.AdminPasswordReset.as_view(), name='password_reset'),
    url(r'^site_admin/password_reset/done/$', auth_views.password_reset_done, {'template_name':'admin_site/password_reset_done.html'} ,name='password_reset_done'),
    url(r'^site_admin/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.AdminPasswordResetConfirm.as_view(), name='password_reset_confirm'),
    url(r'^site_admin/reset/done/$', auth_views.password_reset_complete, {'template_name':'admin_site/password_set_complete.html'} , name='password_reset_complete'),
    
    
    url(r'^site_admin/info/faq/$' , views.AdminFAQ.as_view() , name='admin-faq'),
    url(r'^site_admin/info/faq/new/$' , views.AdminFAQCreate.as_view() , name='admin-faq-create'),
    url(r'^site_admin/info/faq/(?P<pk>[0-9]+)/$' , views.AdminFAQEdit.as_view(), name = 'admin-faq-edit'),
    url(r'^site_admin/info/faq/(?P<pk>[0-9]+)/delete/$' , views.adminFAQDelete, name = 'admin-faq-delete'),
    url(r'^site_admin/info/settings/$', views.AdminSiteInfo.as_view() , name='admin-siteinfo'),
    url(r'^site_admin/info/seo/$' , views.AdminSEO.as_view() , name='admin-seo'),
    url(r'^site_admin/info/email', views.AdminEmailTemplate.as_view(), name='admin-email'),
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
    url(r'^site_admin/data_export/$', views.AdminDataExport.as_view(), name='admin-data'),
    url(r'^site_admin/user_account/$' , views.AdminUserAccount.as_view(), name='admin-user-account'),
    url(r'^site_admin/user_profile/$', views.AdmonUserProfile.as_view(), name='admin-user-profile'),
    url(r'^site_admin/user_permission/$', views.AdminUserPermission.as_view(), name='admin-user-permission'),

    url(r'ajax/order/$' , views.getOrderDetails, name='ajax-get-order'),
    url(r'ajax/ticket/$' , views.getTicketDetails, name='ajax-get-ticket'),
    url(r'ajax/check_dayrender' , views.check_adminDayRender, name='ajax-admin-dayrender'),
    url(r'ajax/get_user_ticket', views.adminGetUserTicket, name='ajax-admin-get-ticket'),
    url(r'ajax/search_ticket/$' , views.adminSearchTicket, name='ajax-admin-search-ticket'),
    url(r'ajax/get_barchart/$' , views.adminGetBarChart, name='ajax-admin-get-barchart'),
    url(r'ajax/get_piechart/$' , views.adminGetPieChart, name='ajax-admin-get-piechart'),
    url(r'ajax/get_service_lines/$' , views.adminGetLineChartService, name='ajax-admin-get-service-lines'),
    url(r'ajax/get_custerm_lines/$' , views.adminGetLineChartCustomer, name='ajax-admin-get-customer-lines'),
    url(r'ajax/get_income_lines/$', views.adminGetLineChartIncome, name='ajax-admin-get-income-lines'),
    url(r'ajax/get_user/$' , views.adminGetUserAccount, name='ajax-admin-get-user-account'),
    url(r'ajax/edit_user/$' , views.adminUserAccountEdit, name='ajax-admin-user-account-edit'),
    url(r'ajax/del_user/$' , views.adminUserAccountDelete, name='ajax-admin-user-account-del'),
    url(r'ajax/update_faq_order/$', views.adminUpdateFAQOrder, name='ajax-admin-update-faq-order'),
    url(r'ajax/get_record_count/$', views.adminGetRecordCount, name='ajax-admin-get-record-count'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),

    #url(r'^sitemap\.xml$', django.contrib.sitemaps.views.sitemap, {'sitemaps': SITEMAPS, 'template_name': 'sitemap.xml'}, name='django.contrib.sitemaps.views.sitemap')
    url(r'^sitemap\.xml$',sitemap, {'sitemaps':sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^googlee431d29ab682695b\.html$', lambda r: HttpResponse("google-site-verification: googlee431d29ab682695b.html", content_type="text/plain")),
    url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: ", content_type="text/plain")),
    url(r'^djga/', include('google_analytics.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
