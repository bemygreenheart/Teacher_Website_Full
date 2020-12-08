from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib.auth import login, authenticate

# Create your views here.
class HomeTemplateView(TemplateView):
  template_name = 'index.html'

class AboutTemplateView(TemplateView):
  template_name = 'about.html'

class ContactView(View):
  template_name = 'contact.html'

  def get(self, request):
     return render(request, self.template_name)

  def post(self, request):
    return 

    
def login_user(request):
  if request.method=='GET':
    return render(request, 'login.html')
  else:
    

  

def signup_user(request):
  return None