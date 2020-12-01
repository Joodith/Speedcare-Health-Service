from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import logout

class HomePage(TemplateView):
    template_name="home.html"
class TestPage(TemplateView):
    template_name="test.html"
def ThanksPage(request):
   logout(request)
   return render(request,"thanks.html")