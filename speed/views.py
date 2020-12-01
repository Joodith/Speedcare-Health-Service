from django.shortcuts import render,get_object_or_404,redirect
from django.http import Http404
from django.views.generic import TemplateView,CreateView,DetailView,ListView,RedirectView,DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from django.contrib.auth import authenticate,login
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from speed.forms import DoctorProfileForm,PatientUserForm,PatientProfileForm,PhoneVerificationForm\
    ,CityForm,Virtual,Usercreateform,MapForm,SlotForm
from speed.models import Doctor,Clinic,Patient,Appointment,GroupMember,MapDetail,TimeSlot
from .authy_api import send_verfication_code, verify_sent_code
from .calender import main
import json
import datetime
import pickle
from django_ical.views import ICalFeed
from django.core.serializers import serialize
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
import requests


# Create your views here.
class Google(TemplateView):
    template_name ="registration/google_login.html"
def doctor_register(request,username):
    registered=False
    user=User.objects.get(username=username)
    if request.method=="POST":
        #user_form=DoctorUserForm(data=request.POST)
        reg_form=DoctorProfileForm(data=request.POST)
        if reg_form.is_valid():
            #user=user_form.save()
            #user.set_password(user.password)
            #user.save()
            reg=reg_form.save(commit=False)
            reg.user=user
            reg.save()
            registered=True
            return render(request,"doctor/doctor_detail.html",{'doctor':reg,'registered':registered})
        else:
            messages.error(request, 'Change the username!')
    else:
        #user_form=DoctorUserForm()
        reg_form=DoctorProfileForm()
    return render(request,"registration/doctor_registration.html",{'reg_form':reg_form,'registered':registered})
def doctor_signup(request):
    if request.method=="POST":
        user_form=Usercreateform(data=request.POST)
        user_form.save()
        return reverse("doc_user_login")
    else:
        user_form=Usercreateform()
        return render(request,"registration/google_login.html",{'user_form':user_form})



def doctor_user_login(request):
    if request.method=="POST":
        form = AuthenticationForm(request, request.POST)
        username=request.POST.get('username')
        password= request.POST.get('password')

        user=authenticate(username=username,password=password)

        if user:
            login(request,user)
            return HttpResponseRedirect(reverse('speed:list_home',kwargs={'username':username}))
        else:
            messages.error(request, 'Invalid username and password')
    else:
        form = AuthenticationForm(request)
    return render(request,"registration/doctor_login.html",{'form':form})

def patient_register(request):
    registered=False
    if request.method=="POST":
        base_form=PatientUserForm(data=request.POST)
        pat_form=PatientProfileForm(data=request.POST)
        if base_form.is_valid() and pat_form.is_valid():
            user = base_form.save()
            user.set_password(user.password)
            user.save()
            pat=pat_form.save(commit=False)
            pat.user=user
            pat.save()
            registered=True
            return HttpResponseRedirect(reverse('pat_user_login'))
        else:
            messages.error(request, '')

    else:
        base_form=PatientUserForm()
        pat_form=PatientProfileForm()
    return render(request,"registration/patient_registration.html",{'base_form':base_form,'pat_form':pat_form,'registered':registered})

def patient_user_login(request):

    if request.method=="POST":
        form=AuthenticationForm(request,request.POST)
        username = request.POST.get('username')
        if not User.objects.filter(username=username):
            messages.error(request, 'User with the mobile number does not exist!')
            return HttpResponseRedirect(reverse('pat_user_login'))
        user = User.objects.get(username=username)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        patient = Patient.objects.get(user__username=user.username)
        patient.phone_number = user.username
        user.backend = 'django.contrib.auth.backends.ModelBackend'

        # print(user.two_factor_auth)
        if user:
            """login(request,user)
            return render(request, "patient/show_detail.html", {'appointment': patient})"""

            try:
                response = send_verfication_code(patient)
                pass
            except Exception as e:
                messages.add_message(request, messages.ERROR,
                                     'verification code not sent. \n'
                                     'Please retry logging in.')
                return HttpResponseRedirect(reverse('pat_user_login'))
            data = json.loads(response.text)

            if data['success'] == False:
                messages.add_message(request, messages.ERROR,
                                     data['message'])
                return HttpResponseRedirect(reverse('pat_user_login'))

            if data['success'] == True:
                request.method = "GET"
                print(request.method)
                kwargs = {'patient': patient}
                return PhoneVerificationView(request, **kwargs)
            else:
                messages.add_message(request, messages.ERROR,
                                     data['message'])
                return HttpResponseRedirect(reverse('pat_user_login'))
        else:
            messages.error(request, 'User with the mobile number does not exist!')
            return HttpResponseRedirect(reverse('pat_user_login'))
    else:
        form = AuthenticationForm(request)
        return render(request, "registration/patient_login.html", {'form': form})

def PhoneVerificationView(request, **kwargs):
   template_name = 'registration/phone_confirm.html'

   if request.method == "POST":
       username = request.POST['username']
       user = User.objects.get(username=username)
       user.backend = 'django.contrib.auth.backends.ModelBackend'
       patient=Patient.objects.get(user__username=user.username)
       patient.phone_number=user.username
       patient.save()
       form = PhoneVerificationForm(request.POST)
       if form.is_valid():
           verification_code = request.POST['one_time_password']
           response = verify_sent_code(verification_code, patient)
           print(response.text)
           data = json.loads(response.text)

           if data['success'] == True:
               login(request, user)
               if patient.phone_number_verified is False:
                   patient.phone_number_verified = True
                   patient.save()
               return render(request,"patient/show_detail.html",{'appointment':patient})
           else:
               messages.add_message(request, messages.ERROR,
                               data['message'])
               return render(request, template_name, {'patient':patient})
       else:
           context = {
               'patient': patient,
               'form': form,
           }
           return render(request, template_name, context)

   elif request.method == "GET":
       patient = kwargs['patient']
       return render(request, template_name, {'patient': patient})

## DOCTOR VIEWS

class DoctorListView(ListView):
    context_object_name ="listdoc"
    model=Doctor
    template_name ="doctor/doctor_list.html"

class DoctorDetailView(DetailView):
    model=Doctor
    template_name="doctor/doctor_detail.html"
    def get_queryset(self):
        queryset=super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))

class DoctorDetailView2(DetailView):
    model=Doctor
    template_name="doctor/doctor_detail2.html"
    def get_queryset(self):
        queryset=super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))


def Meet(request,pk):
    if request.method=='POST':
        v_form=Virtual(request.POST)
        p_form=AuthenticationForm(request,request.POST)
        username = request.POST.get('username')
        if v_form.is_valid():
            subject=request.POST.get('subject')
            user=User.objects.get(username=username)
            user.backend ='django.contrib.auth.backends.ModelBackend'
            if user:
                p=User.objects.get(pk=user.pk)
                date=request.POST.get('day')
                time=request.POST.get('time')
                appointment_pat=v_form.save(commit=False)
                appointment_pat.patient=Patient.objects.get(user__id=p.id)
                appointment_pat.save()
                appointment_doc=v_form.save(commit=False)
                appointment_doc.doctor=Doctor.objects.get(pk=pk)
                appointment_doc.save()
                patient = Patient.objects.get(user__username=user.username)
                patient.phone_number = user.username
                patient.save()
                #print(appointment_doc.doctor.user.email)
                main(appointment_doc.doctor.user.email,date,time)
                """login(request,user)
                return render(request, "patient/show_detail.html", {'appointment': patient})"""
                try:
                    response = send_verfication_code(patient)
                    pass
                except Exception as e:
                    messages.add_message(request, messages.ERROR,
                                             'verification code not sent. \n'
                                             'Please retry logging in.')
                    return HttpResponseRedirect(reverse('pat_user_login'))
                data = json.loads(response.text)

                if data['success'] == False:
                    messages.add_message(request, messages.ERROR,
                                             data['message'])
                    return HttpResponseRedirect(reverse('pat_user_login'))

                if data['success'] == True:
                    request.method = "GET"
                    print(request.method)
                    kwargs = {'patient': patient}
                    return PhoneVerificationView(request, **kwargs)
                else:
                    messages.add_message(request, messages.ERROR,
                                             data['message'])
                    return HttpResponseRedirect(reverse('pat_user_login'))

    else:
        v_form=Virtual()
        p_form=AuthenticationForm(request)
    return render(request,"appointment/appointment_form.html",{'v_form':v_form,'p_form':p_form})
class sample(TemplateView):
    template_name ="patient/show_app.html"
class another(TemplateView):
    template_name ="patient/show_detail.html"

class ConfirmView(TemplateView):
    template_name="appointment/confirm_app.html"


class DoctorHomeView(TemplateView,RedirectView):
    template_name="doctor/doctor_base.html"
    def get_redirect_url(self, pk):
        doctor=Doctor.objects.get(pk=pk)
        username=doctor.user.username
        return reverse('speed:detail_doctor',args=(username,pk))
class ClinicListView(ListView):
    model=Clinic
    template_name="clinic/clinic_list.html"


def ClinicSearch(request):
    if request.method=="POST":
        form=CityForm(request.POST)
        context={}
        if form.is_valid():
            query=form.cleaned_data.get('city')
            res=Clinic.objects.filter(city__iexact=query)
            context.update({'res':res})
            return render(request,'clinic/clinic_list.html',context)
        else:
            return HttpResponse("Not valid")
    else:
        form=CityForm()
    return render(request,"clinic/clinic_search.html",{'form':form})

class ClinicDetailView(DetailView):
    model=Clinic
    template_name ="clinic/clinic_detail.html"

class ListDoctor(ListView):
    model=Doctor
    template_name="doctor/home_list.html"
    def get_queryset(self):
        self.people=Doctor.objects.get(user__username__iexact=self.kwargs.get('username'))
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['people']=self.people
        return context




class AppointmentList(ListView):
    model=Appointment
    template_name="appointment/appointment_list.html"
class UserAppointments(ListView):
    model=Appointment
    template_name="appointment/user_appointment_list.html"

    def get_queryset(self):
        try:
            self.appointment_user=Patient.objects.prefetch_related('appointments').get(user__username__iexact=self.kwargs.get('username'))
        except Patient.DoesNotExist:
            raise Http404
        else:
            return self.appointment_user.appointments.all()
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['appointment_user']=self.appointment_user
        return context
class AppointmentDetail(DetailView):
    model=Appointment
    def get_queryset(self):
        queryset=super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))
    template_name="appointment/appointment_detail.html"

class PatientHomeView(TemplateView):
    template_name ="patient/patient_base.html"

class PatientListView(ListView):
    model = Patient
    template_name = "patient/home_patient.html"

    def get_queryset(self):
        self.person= User.objects.prefetch_related('patient_profile').get(username__iexact=self.kwargs.get('username'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['person'] = self.person
        return context

class PatientDetailView(DetailView):
    model=Patient
    def get_queryset(self):
        queryset=super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))

    template_name = "patient/patient_detail.html"

class  CancelAppointment(DeleteView):
    model=Appointment
    def get_success_url(self):
        p=self.kwargs.get('username')
        return reverse_lazy('for_patient',kwargs={'username':p})
    def get_queryset(self):
       queryset=super().get_queryset()
       return queryset.filter(patient__user__username=self.kwargs.get('username'))
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    template_name="appointment/appointment_confirm_cancel.html"
class DeleteAppointmentPatient(DeleteView):
    model=Appointment
    def get_success_url(self):
        p=self.kwargs.get('username')
        return reverse_lazy('speed:for_patient',kwargs={'username':p})
    def delete(self, request, *args, **kwargs):
        pk=self.kwargs.get('pk')
        name=self.kwargs.get('username')
        k=get_object_or_404(Appointment,pk=pk)
        #name=k.patient.user.username
        k.delt=False
        k.save()
        context = Patient.objects.prefetch_related("appointments").get(user__username=self.kwargs.get('username'))
        return render(request,"appointment/user_appointment_list.html",{'appointment_user':context})
    template_name = "appointment/appointment_confirm_delete.html"

class  DeleteAppointmentDoctor(DeleteView):
    model=Appointment
    def get_success_url(self):
        p=self.request.user.username
        k=Doctor.objects.get(user__username=p)
        pk=k.pk
        return reverse_lazy('speed:detail_doctor',kwargs={'username':p,'pk':pk})
    def delete(self, request, *args, **kwargs):
        pk=self.kwargs.get('pk')
        name=self.kwargs.get('username')
        k=get_object_or_404(Appointment,pk=pk)
        #name=k.patient.user.username
        k.deldoc=False
        k.save()
        context = Doctor.objects.prefetch_related("doc_appointments").get(user__username=self.kwargs.get('username'))
        return render(request,"doctor/doctor_detail.html",{'doctor':context})
    template_name="appointment/appointment_confirm_deletedoc.html"

def searchmap(request):
    #is_cached = ('geodata' in request.session)

    if not False:
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '')
        params = {'access_key': settings.GOOGLE_MAPS_API_KEY}
        response = requests.get('https://www.google.com/maps/embed/v1/place', params=params)
        #data=json.loads(response.text)

    #geodata = request.session['geodata']
    if request.method=="POST":
        patient=MapForm(request.POST)
        if patient.is_valid:
            address=request.POST.get('address')
            #data=json.dumps(clinic)
            data=serialize('json',MapDetail.objects.all())
            y=json.loads(data)
            return render(request,"clinic/maps.html",{'address':address,'data':data,'y':y})
    else:
        patient=MapForm()
        return render(request,"clinic/address_form.html",{'patient':patient})

def TimeView(request):
   if request.method=="POST":
       form=Calendar(request.POST)
       if form.is_valid:
           return HttpResponseRedirect('home')
   else:
       form=Calendar()
       return render(request,"patient/timings.html",{'form':form})


class EventFeed(ICalFeed):

    #A simple event calender
    product_id = '-//example.com//Example//EN'
    timezone = 'UTC'
    file_name = "event.ics"

    def __call__(self, request, *args, **kwargs):
        self.request = request
        return super(EventFeed, self).__call__(request, *args, **kwargs)
    def items(self):
        return Event.objects.all().order_by('-date')

    def item_guid(self, item):
        return "{}{}".format(item.id, "global_name")

    def item_title(self, item):
        return "{}".format(item.name)

    def item_description(self, item):
        return item.description

    def item_start_datetime(self, item):
        return item.date

    def item_link(self, item):
        return "http://www.google.de"

#Payment Gateway Interface
class pay_firstpage(TemplateView):
    template_name="first_page.html"

def process_payment(request,pk):
    d=Appointment()
    #od_id =Order.get_id(obj)
    #print(od_id)
    d.doctor=Doctor.objects.prefetch_related("doc_appointments").get(user_id=pk)
    d.order_id=d.get_id()
    d.save()
    print(d.order_id)

    host=request.get_host()
    od_name="Appointment with"+d.doctor.name
    paypal_dict = {
        "business":settings.PAYPAL_RECEIVER_EMAIL,
        "order_id":d.order_id,
        "amount":d.doctor.fees,
        "item_name":od_name,
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('done',args=[d.order_id])),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('cancel',args=[d.doctor_id])),
        #"custom": "premium_plan",  # Custom command to correlate to some function later (optional)

    }
    form=PayPalPaymentsForm(initial=paypal_dict)
    return render(request,"payment/payment.html",{'form':form})

@csrf_exempt
def ret_view(request,pk):
    obj = Appointment.objects.get(order_id__iexact=pk)
    obj.pay_status = True
    return render(request,"payment/payment_done.html",{'obj':obj})

@csrf_exempt
def cancel_view(request,pk):
    obj=Appointment.objects.get(order_id__iexact=pk)
    obj.pay_status=False
    return render(request,"payment/payment_cancel.html",{'obj':obj})

#TIME SLOT VIEWS
"""class SlotList(ListView):
    model=TimeSlot
    template_name="slot/slot_list.html" """

class CreateSlot(CreateView):
    form_class=SlotForm
    template_name="slot/doctor_slot.html"

class Doctor_slot(ListView):
    model=TimeSlot
    template_name="slot/slot_list.html"
    def get_queryset(self):
        try:
            self.slots_of_doctor=Doctor.objects.prefetch_related("slots").get(user__username__iexact=self.kwargs.get('username'))
        except:
            raise Http404
        else:
            return self.slots_of_doctor.slots.all()

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['slot_doc']=self.slots_of_doctor
        return context














