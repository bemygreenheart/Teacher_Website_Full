from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, View
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http.response import Http404
from django.db import IntegrityError

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
  if request.method=="POST":
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username=username, password=password)
    if user is not None:
      login(request = request, user=user)
      return redirect(reverse('home'))
    else:
      context = {'error' : 'Invalid username or password, make sure to both fields correct!', 'login_data':
      {'username' : username, 'password': password}}
      return render(request, 'login.html', context=context)
  

def signup_user(request):
  if request.method == "GET":
    return render(request, 'signup.html')

  if request.method == "POST":
    first_name = request.POST.get('first_name', '')
    last_name = request.POST.get('last_name', '')
    email = request.POST.get('email', '')
    username = request.POST.get('username', '')
    password = request.POST.get('password', None)
    password_confirm = request.POST.get('password_confirm', None)

    errors = []
    if username:
      if password and password == password_confirm:
        others = {}
        if first_name:
          others['first_name'] = first_name
        if last_name:
          others['last_name'] = last_name
        if email:
          others['email'] = email
        try:
          User.objects.create_user(username = username, password=password, **others)
          #Redirecting to the home page after successfull record creation
          return redirect(reverse('home')) 
        except IntegrityError:
          errors.append(f'This username is already taken, please try another one!')
      else:
        errors.append('Please enter the same password for the confirmation!')
    else:
      errors.append('You should enter a username')
    if errors and len(errors)>0:
      sign_data = {'username' : username ,'first_name' : first_name, 
      'last_name' : last_name, 'email' : email, 'password' : password, 'password_confirm' : password_confirm}
    
      context = {'errors' : errors,'sign_data' : sign_data}
      return render(request, 'signup.html', context=context)
