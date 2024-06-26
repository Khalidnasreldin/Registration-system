from django.shortcuts import render, redirect

# for the signup process
from . forms import CreateUserForm

# for the login \ logout process
from . forms import LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout

# protect views
from django.contrib.auth.decorators import login_required

# Create your views here.
def homepage(request):
    return render(request, 'index.html')

def register(request):
    form = CreateUserForm

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()        
            return redirect('login')

    context = {'registerform':form}        
    return render(request, 'register.html', context=context)

def login(request):
    form = LoginForm()
    
    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')

    context = {'loginform':form}
    return render(request, 'login.html', context=context)

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')

def logout(request):
    auth.logout(request)
    return redirect('/')