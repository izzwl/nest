from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

def get_prev_url(request,default):
    try:
        url = request.GET.get('back').replace('///','&')
    except:
        url = default
    return url

def create_prev_url(request):
    try:
        url = request.get_full_path().replace('&','///')
    except:
        url = '/'
    return url

def check_permission(request,perm,prev_url,modal=False):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'Please login first')
        if modal: return redirect('%s?next=%s&modal=Y' % (settings.LOGIN_URL, request.path))
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if not request.user.has_perm(perm):
        messages.add_message(request, messages.ERROR, 'Operations not permitted')
        return redirect(prev_url)
    return False

def check_fk(request,fk,model,prev_url,modal=False):
    try:
        robj = model.objects.get(pk=fk)
    except:
        messages.add_message(request, messages.ERROR, 'Data not found')
        if modal : return render(request,"ui/message_only.html")
        return redirect(prev_url)
    if robj.c_nikappr == '':
        messages.add_message(request, messages.ERROR, 'Data must be approved')
        if modal : return render(request,"ui/message_only.html")
        return redirect(prev_url)
    return False
