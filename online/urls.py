"""online URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url,include
from allauth.account.views import LogoutView,LoginView
from . import views
import speed

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.HomePage.as_view(),name="home"),
    url(r'^speed/',include("speed.urls",namespace="speed")),
    url(r'^accounts/',include("allauth.urls")),
    #url(r'login/$',LoginView.as_view(), name="login"),
    #url(r'^accounts/logout/',LogoutView.as_view(),name="account_logout"),
    url(r'^test/',views.TestPage.as_view(),name="test"),
    url(r'^thanks/',views.ThanksPage,name="thanks"),
    #url(r'^signup/$',speed.views.doctor_signup,name="signup"),
    #url(r'^doctor_login/$',speed.views.doctor_user_login, name="doc_user_login"),
    url(r'^clinic_search/$', speed.views.ClinicSearch, name="search"),
    url(r'^clinic_detail/(?P<slug>[-\w]+)/$',speed.views.ClinicDetailView.as_view(),name="detail_clinic"),
    url(r'^virtual_meet/(?P<username>[-\w]+)/(?P<pk>\d+)/$',speed.views.DoctorDetailView2.as_view(),name="virtual_meet"),
    url(r'^fix_meet/(?P<pk>\d+)/$',speed.views.Meet,name="meet_fix"),
    url(r'^patient_register/$',speed.views.patient_register,name="pat_reg"),
    url(r'^patient_login/$',speed.views.patient_user_login,name="pat_user_login"),
    url(r'^verify/$', speed.views.PhoneVerificationView, name="phone_verification_url"),
    url(r'^by/(?P<username>[-\w]+)/$',speed.views.UserAppointments.as_view(),name="for_patient"),
    url(r'^patient_home/$', speed.views.PatientHomeView.as_view(), name="patient_home"),
    url(r'^patient_list/(?P<username>[-\w]+)/$',speed.views.PatientListView.as_view(),name="list_patient"),
    url(r'^patient_detail/(?P<username>[-\w]+)/(?P<pk>\d+)/$',speed.views.PatientDetailView.as_view(),name="detail_patient"),
    url(r'^detail_app/(?P<username>[-\w]+)/$',speed.views.AppointmentDetail.as_view(),name="detail_app"),
    url(r'^show/$',speed.views.sample.as_view(),name="app_show"),
    url(r'^show_same/$',speed.views.another.as_view(),name="show_detail"),
    url(r'^doctor_list/$',speed.views.DoctorListView.as_view(),name="list_doctor"),
    url(r'^doctor_detail/(?P<username>[-\w]+)/(?P<pk>\d+)/$',speed.views.DoctorDetailView.as_view(),name="detail_doctor"),
    url(r'^cancel_patient/(?P<username>[-\w]+)/(?P<pk>\d+)/$',speed.views.CancelAppointment.as_view(), name="cancel_pat"),
    url(r'^delete_patient/(?P<username>[-\w]+)/(?P<pk>\d+)/$',speed.views.DeleteAppointmentPatient.as_view(),
        name="delete_pat"),
    url(r'^delete_patient_doctor/(?P<username>[-\w]+)/(?P<pk>\d+)/$',speed.views.DeleteAppointmentDoctor.as_view(),
        name="delete_pat_doc"),
    url(r'map/$',speed.views.searchmap,name="map_search"),
    url(r'time/$',speed.views.TimeView,name="fix_time"),
    url(r'calender/$',speed.views.EventFeed,name="feed"),
    url(r'^process_pay/(?P<pk>\d+)/$',speed.views.process_payment,name="process"),
    url(r'^paypal_use/',include('paypal.standard.ipn.urls')),
    url(r'^payment_done/(?P<pk>\d+)/$',speed.views.ret_view,name="done"),
    url(r'^payment_cancel/(?P<pk>\d+)/$',speed.views.cancel_view,name="cancel"),
    url(r'^settings_time/create_slot/$', speed.views.CreateSlot.as_view(), name="slot_create"),
    url(r'^settings_time/(?P<username>[-\w]+)/$',speed.views.Doctor_slot.as_view(),name="slot_time"),

]
