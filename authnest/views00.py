from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
# Create your views here.
from django.conf import settings
from authnest.forms import LoginForm
from authnest.models import *
from django.http import HttpResponse

def act_logging(nik,trx,func,key):
    ActLog = ActivityLog(c_nik=nik,c_trx=trx,c_func=func,c_key=key)
    ActLog.save()

def home(request,template='authnest/home.html'):
    return render(request,template,{'mnactive':'mnhome'})

def login(request,template='authnest/login.html'):
    if request.user.is_authenticated:
        if request.GET.get('next'):
            return redirect(request.GET.get('next'))
        return redirect('/')

    form = LoginForm(request.POST or None)
    if form.is_valid():
        user = authenticate(request, username=form.cleaned_data['nik'], password=form.cleaned_data['password'])
        if user is not None:
            auth_login(request, user)
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('/')
        else:
            messages.add_message(request, messages.ERROR, 'Login Failed, wrong NIK or password')    #change this
    return render(request,template,{'form':form})

def logout(request):
    auth_logout(request)
    return redirect('/')
