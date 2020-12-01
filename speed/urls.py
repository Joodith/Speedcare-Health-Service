from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.contrib.auth.views import auth_logout
from speed import views
app_name="speed"
urlpatterns=[
    url(r'^doctor_register/(?P<username>[-\w]+)/$',views.doctor_register,name="doc_reg"),
    #url(r'login/$', auth_views.LoginView.as_view(), name="login"),
    url(r'^',views.Google.as_view(),name="doc_user_login"),
    #url(r'^doctor_login/$',views.doctor_user_login,name="doc_user_login"),
    #url(r'^patient_register/$',views.patient_register,name="pat_reg"),
    #url(r'^patient_login/$',views.patient_user_login,name="pat_user_login"),
    #url(r'^verify/$', views.PhoneVerificationView, name="phone_verification_url"),
    #url(r'^logout/$',auth_logout,name="logout"),
    url(r'^home/$', views.DoctorHomeView.as_view(), name="doctor_home"),
    #url(r'^doctor_list/$',views.DoctorListView.as_view(),name="list_doctor"),
    url(r'^doctor_home/(?P<username>[-\w]+)/$',views.ListDoctor.as_view(),name="list_home"),
    #url(r'^doctor_detail/(?P<username>[-\w]+)/(?P<pk>\d+)/$',views.DoctorDetailView.as_view(),name="detail_doctor"),
    #url(r'^virtual_meet/(?P<username>[-\w]+)/(?P<pk>\d+)/$',views.DoctorDetailView2.as_view(),name="virtual_meet"),
    #url(r'^fix_meet/(?P<pk>\d+)/$',views.Meet,name="meet_fix"),
    #url(r'^show/$',views.sample.as_view(),name="app_show"),
    #url(r'^show_same/$',views.another.as_view(),name="show_detail"),
    url(r'^confirm/$',views.ConfirmView.as_view(),name="confirm"),
    #url(r'^clinic_search/$',views.ClinicSearch,name="search"),
    url(r'^$',views.ClinicListView.as_view(),name="list_clinic"),
    #url(r'^clinic_detail/(?P<slug>[-\w]+)/$',views.ClinicDetailView.as_view(),name="detail_clinic"),
    #url(r'^patient_home/$', views.PatientHomeView.as_view(), name="patient_home"),

    #url(r'^patient_list/(?P<username>[-\w]+)/$',views.PatientListView.as_view(),name="list_patient"),
    #url(r'^patient_detail/(?P<username>[-\w]+)/(?P<pk>\d+)/$',views.PatientDetailView.as_view(),name="detail_patient"),
    #url(r'^by/(?P<username>[-\w]+)/$',views.UserAppointments.as_view(),name="for_patient"),
    #url(r'^detail_app/(?P<username>[-\w]+)/$',views.AppointmentDetail.as_view(),name="detail_app"),
    #url(r'^cancel_patient/(?P<username>[-\w]+)/(?P<pk>\d+)/$',views.CancelAppointment.as_view(),name="cancel_pat"),
    #url(r'^delete_patient/(?P<username>[-\w]+)/(?P<pk>\d+)/$', views.DeleteAppointmentPatient.as_view(), name="delete_pat"),
    #url(r'^delete_patient_doctor/(?P<username>[-\w]+)/(?P<pk>\d+)/$', views.DeleteAppointmentDoctor.as_view(), name="delete_pat_doc"),


]