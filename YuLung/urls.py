"""YuLung URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  re_path(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  re_path(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  re_path(r'^blog/', include('blog.urls'))
"""
from django.http import HttpResponse
from django.urls import include, re_path
from django.contrib import admin
from django.contrib.auth import logout
from django.contrib.auth.views import (
    LoginView, LogoutView,
    PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView,
)
from django.contrib.sitemaps.views import sitemap
from YuLung.sitemaps import StaticSitemap
from reservation.sitemaps import ServiceSitemap
from django.conf import settings
from django.conf.urls.static import static
from . import views

sitemaps = {
    'static': StaticSitemap,
    'service': ServiceSitemap
}

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^$', views.index , name='index' ),
    re_path(r'^reservation/' , include('reservation.urls')),
    re_path(r'^comments/$' , views.Comments.as_view(), name='comments'),
    re_path(r'^my_reservation/$' , views.MyReservation.as_view(), name='my_reservation'),
    re_path(r'^signin/$', views.SignIn.as_view(), name='sign-in'),
    re_path(r'^signup/$', views.SignUp.as_view(), name='sign-up'),
    re_path(r'^#_=_login/success/$', views.loginSuccess, name='login-success'),
    re_path(r'^login/success/$' , views.loginSuccessRedirect, name='login-success-redirect'),
    re_path(r'^faq/$' , views.FAQpage.as_view() , name='faq'),
    re_path(r'^privacy/$' , views.privacy , name='privacy'),
    re_path(r'^tos/$' , views.tos , name='tos'),
    re_path(r'^my/$' , views.MyPage.as_view() , name='my'),
    
    re_path(r'^user/personalinfo/$' , views.UserInfo.as_view(), name='user-profile'),
    
    re_path(r'^password/reset/$',views.PasswordReset.as_view(), name='front_password_reset'),
    re_path(r'^password_reset/done/$', PasswordResetDoneView.as_view(template_name='password_reset_done.html') ,name='front_password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.PasswordResetConfirm.as_view(), name='front_password_reset_confirm'),
    re_path(r'^reset/done/$', PasswordResetCompleteView.as_view(template_name='password_set_complete.html') , name='front_password_reset_complete'),
    re_path(r'^logou/$', logout, name='logout'),
    
    re_path(r'^site_admin/$' , views.AdminIndex.as_view() , name='admin-index'),
    re_path(r'^site_admin/login/$' , views.AdminSignIn.as_view() , name='admin-login'),
    re_path(r'^site_admin/logout/$', views.adminLogout, name='admin-logout'),
    re_path(r'^site_admin/info/banner/$' , views.AdminBanner.as_view() , name='admin-banner'),
    
    re_path(r'^site_admin/password/reset/$',views.AdminPasswordReset.as_view(), name='password_reset'),
    re_path(r'^site_admin/password_reset/done/$', PasswordResetDoneView.as_view(template_name='admin_site/password_reset_done.html') ,name='password_reset_done'),
    re_path(r'^site_admin/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.AdminPasswordResetConfirm.as_view(), name='password_reset_confirm'),
    re_path(r'^site_admin/reset/done/$', PasswordResetCompleteView.as_view(template_name='admin_site/password_set_complete.html') , name='password_reset_complete'),
    
    
    re_path(r'^site_admin/info/faq/$' , views.AdminFAQ.as_view() , name='admin-faq'),
    re_path(r'^site_admin/info/faq/new/$' , views.AdminFAQCreate.as_view() , name='admin-faq-create'),
    re_path(r'^site_admin/info/faq/(?P<pk>[0-9]+)/$' , views.AdminFAQEdit.as_view(), name = 'admin-faq-edit'),
    re_path(r'^site_admin/info/faq/(?P<pk>[0-9]+)/delete/$' , views.adminFAQDelete, name = 'admin-faq-delete'),
    re_path(r'^site_admin/info/settings/$', views.AdminSiteInfo.as_view() , name='admin-siteinfo'),
    re_path(r'^site_admin/info/seo/$' , views.AdminSEO.as_view() , name='admin-seo'),
    re_path(r'^site_admin/info/email', views.AdminEmailTemplate.as_view(), name='admin-email'),
    re_path(r'^site_admin/service/course/$', views.AdminService.as_view(), name='admin-service'),
    re_path(r'^site_admin/service/course/new/$', views.AdminServiceCreate.as_view(), name='admin-service-create'),
    re_path(r'^site_admin/service/course/(?P<pk>[0-9]+)/$' , views.AdminServiceEdit.as_view() , name='admin-service-edit'),
    re_path(r'^site_admin/service/course/(?P<pk>[0-9]+)/delete/$' , views.adminServiceDelete, name='admin-service-delete'),
    re_path(r'^site_admin/service/customer/$' , views.AdminCustomer.as_view(), name='admin-customer'),
    re_path(r'^site_admin/service/customer/new/$' , views.AdminCustomerCreate.as_view(), name='admin-customer-create'),
    re_path(r'^site_admin/service/customer/(?P<pk>[0-9]+)/$' , views.AdminCustomerEdit.as_view() , name='admin-customer-edit'),
    re_path(r'^site_admin/service/customer/(?P<pk>[0-9]+)/delete/$' , views.adminCustomerDelete, name='admin-customer-delete'),
    re_path(r'^site_admin/calendar/$' , views.AdminCalendar.as_view(), name='admin-calendar'),    
    re_path(r'^site_admin/calendar/time_slot/$' , views.AdminTimeSlot.as_view(), name='admin-timeslot'),
    re_path(r'^site_admin/calendar/time_slot/(?P<date>[0-9]{4}-?[0-9]{2}-?[0-9]{2})/$' , views.AdminTimeSlot.as_view(), name='admin-timeslot-date'),
    re_path(r'^site_admin/calendar/time_slot/(?P<date>[0-9]{4}-?[0-9]{2}-?[0-9]{2})/edit/(?P<pk>[0-9]+)/$' , views.AdminTimeSlotEdit.as_view(), name='admin-timeslot-date-edit'),
    re_path(r'^site_admin/calendar/time_slot/(?P<date>[0-9]{4}-?[0-9]{2}-?[0-9]{2})/delete/(?P<pk>[0-9]+)/$' , views.adminTimeSlotDelete, name='admin-timeslot-date-delete'),
    re_path(r'^site_admin/order/$' , views.AdminOrder.as_view(), name='admin-order'),
    re_path(r'^site_admin/ticket/$', views.AdminTicket.as_view(), name='admin-ticket'),
    re_path(r'^site_admin/comment/$' , views.AdminComment.as_view(), name='admin-comment'),
    re_path(r'^site_admin/comment/(?P<pk>[0-9]+)/approve/$' , views.adminCommentApprove, name='admin-comment-approve'),
    re_path(r'^site_admin/comment/(?P<pk>[0-9]+)/disapprove/$' , views.adminCommentDisapprove, name='admin-comment-disapprove'),
    re_path(r'^site_admin/comment/(?P<pk>[0-9]+)/delete/$' , views.adminCommentDelete, name='admin-comment-delete'),
    re_path(r'^site_admin/statistic/$' , views.AdminStatistic.as_view() , name='admin-statistic'),
    re_path(r'^site_admin/data_export/$', views.AdminDataExport.as_view(), name='admin-data'),
    re_path(r'^site_admin/user_account/$' , views.AdminUserAccount.as_view(), name='admin-user-account'),
    re_path(r'^site_admin/user_profile/$', views.AdmonUserProfile.as_view(), name='admin-user-profile'),
    re_path(r'^site_admin/user_permission/$', views.AdminUserPermission.as_view(), name='admin-user-permission'),

    re_path(r'ajax/order/$' , views.getOrderDetails, name='ajax-get-order'),
    re_path(r'ajax/ticket/$' , views.getTicketDetails, name='ajax-get-ticket'),
    re_path(r'ajax/check_dayrender' , views.check_adminDayRender, name='ajax-admin-dayrender'),
    re_path(r'ajax/get_user_ticket', views.adminGetUserTicket, name='ajax-admin-get-ticket'),
    re_path(r'ajax/search_ticket/$' , views.adminSearchTicket, name='ajax-admin-search-ticket'),
    re_path(r'ajax/get_barchart/$' , views.adminGetBarChart, name='ajax-admin-get-barchart'),
    re_path(r'ajax/get_piechart/$' , views.adminGetPieChart, name='ajax-admin-get-piechart'),
    re_path(r'ajax/get_service_lines/$' , views.adminGetLineChartService, name='ajax-admin-get-service-lines'),
    re_path(r'ajax/get_custerm_lines/$' , views.adminGetLineChartCustomer, name='ajax-admin-get-customer-lines'),
    re_path(r'ajax/get_income_lines/$', views.adminGetLineChartIncome, name='ajax-admin-get-income-lines'),
    re_path(r'ajax/get_user/$' , views.adminGetUserAccount, name='ajax-admin-get-user-account'),
    re_path(r'ajax/edit_user/$' , views.adminUserAccountEdit, name='ajax-admin-user-account-edit'),
    re_path(r'ajax/del_user/$' , views.adminUserAccountDelete, name='ajax-admin-user-account-del'),
    re_path(r'ajax/update_faq_order/$', views.adminUpdateFAQOrder, name='ajax-admin-update-faq-order'),
    re_path(r'ajax/get_record_count/$', views.adminGetRecordCount, name='ajax-admin-get-record-count'),
    re_path(r'^oauth/', include('social_django.urls', namespace='social')),

    re_path(r'^sitemap\.xml$',sitemap, {'sitemaps':sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    re_path(r'^googlee431d29ab682695b\.html$', lambda r: HttpResponse("google-site-verification: googlee431d29ab682695b.html", content_type="text/plain")),
    re_path(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: ", content_type="text/plain")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
