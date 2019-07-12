from django.shortcuts import render, redirect
from django.db.models import F,Q,Max
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.forms import modelformset_factory
from purchasing.forms00 import *
from purchasing.models import *
from authnest.views00 import act_logging
from ui.forms import *
from datetime import datetime

def in71(request,template='purchasing/f_in71.html'):
    instance = None
    #instantiate form based on request
    if request.method == "POST":
        func = request.POST.get('func') or None
        c_po = request.POST.get('c_po') or None
        d_received = request.POST.get('d_received') or None
        try:
            instance = TMIN71.objects.get(c_po=c_po,d_received=datetime.strptime(d_received,"%d %m %y"))
            if func == 'inquiry':
                messages.add_message(request, messages.SUCCESS, 'Inquiry Success') #change this
                form = FMIN71(instance=instance,error_class=DivErrorList)
            else:
                form = FMIN71(request.POST,instance=instance,error_class=DivErrorList)
        except:
            if func == 'inquiry':
                messages.add_message(request, messages.ERROR, '%s - %s NOT FOUND' % (c_po.upper(),d_received))
            form = FMIN71(request.POST,error_class=DivErrorList)

        # cek auth and permission
        if func in ['add','change','approve','print']:
            if not request.user.is_authenticated:
                messages.add_message(request, messages.ERROR, 'Please login first') #change this
                return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
            if not request.user.has_perm('purchasing.%s_tmin71'%func):
                messages.add_message(request, messages.ERROR, 'Operations not permitted') #change this
                return redirect(request.path)

        #cek po in IVR7020H
        if func in ['add','print']:
            ivr7020h = IVR7020H.objects.filter(master=c_po)
            if not ivr7020h:
                messages.add_message(request, messages.ERROR, 'MASTER %s not found' % c_po.upper()) #change this
                return redirect(request.path)

        # form validation and operations
        if form.is_valid():
            clean_func = form.cleaned_data['func']
            obj = form.save(commit=False)
            if clean_func == 'add':
                obj.c_nik = request.user.get_username()
                obj.pk = None
                obj.d_create = timezone.now()
                try:
                    obj.save()
                    act_logging(request.user.get_username(),'IN71',clean_func,str(obj))
                    messages.add_message(request, messages.SUCCESS, 'Successfully Added') #change this
                except:
                    messages.add_message(request, messages.ERROR, 'Operations Failed, Duplicate Entry') #change this
                for ivr in ivr7020h:
                    in72 = TMIN72(f_in71=obj,i_itemno=ivr.itm,c_partnumber=ivr.partnumber,n_um=ivr.um,i_qship=0,i_qreceived=0)
                    try:
                        in72.save()
                    except:
                        pass
            elif clean_func == 'change':
                obj.c_nik = request.user.get_username()
                obj.c_nikappr = ''
                obj.save()
                act_logging(request.user.get_username(),'IN71',clean_func,str(obj))
                messages.add_message(request, messages.SUCCESS, 'Successfully Changed') #change this
            elif clean_func == 'approve':
                obj.c_nikappr = request.user.get_username()
                obj.save()
                act_logging(request.user.get_username(),'IN71',clean_func,str(obj))
                messages.add_message(request, messages.SUCCESS, 'Successfully Approved') #change this
            elif clean_func == 'print':
                in71 = TMIN71.objects
                return render(request,'purchasing/f_in71_print.html',{'in71':in71,'ivr7020h':ivr7020h,})
            else:
                pass
    else:
        form = FMIN71(error_class=DivErrorList)

    ctx = {
        'datetime_picker':True,
        'form':form,
        'instance':instance,
    }
    return render(request,template,ctx)

def in72(request,template='purchasing/f_in72.html'):
    now = datetime.now()
    year = now.strftime("%Y")
    in71_instance = None
    in72_instances = None
    ivr7020h = None
    #instantiate form based on request
    if request.method == "POST":
        func = request.POST.get('func') or None
        c_po = request.POST.get('c_po') or None
        d_received = request.POST.get('d_received') or None

        ivr7020h = IVR7020H.objects.filter(master=c_po).order_by('itm')
        if not ivr7020h:
            messages.add_message(request, messages.ERROR, 'MASTER %s not found' % c_po.upper()) #change this
            return redirect(request.path)

        try:
            in71_instance = TMIN71.objects.get(c_po=c_po,d_received=datetime.strptime(d_received,"%d %m %y"))
            in72_instances = TMIN72.objects.filter(f_in71=in71_instance).order_by('i_itemno')
            # messages.add_message(request, messages.SUCCESS, 'Inquiry Success')
        except:
            messages.add_message(request, messages.ERROR, '%s - %s NOT FOUND' % (c_po.upper(),d_received))

        FMIN72_set = modelformset_factory(TMIN72,form=FMIN72)
        in71_form = FMIN71Q(instance=in71_instance,error_class=DivErrorList)
        if func in ['add']:
            in72_formset = FMIN72_set(request.POST,queryset=in72_instances,error_class=DivErrorList)
        else:
            in72_formset = FMIN72_set(queryset=in72_instances,error_class=DivErrorList)

        # in72_formset = FMIN72_set(queryset=in72_instances,error_class=DivErrorList)
        # cek auth and permission
        if func in ['add','approve']:
            if not request.user.is_authenticated:
                messages.add_message(request, messages.ERROR, 'Please login first') #change this
                return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
            if not request.user.has_perm('purchasing.%s_tmin72'%func):
                messages.add_message(request, messages.ERROR, 'Operations not permitted') #change this
                return redirect(request.path)

        # Approve Operations
        if func == 'approve':
            try:
                TMIN72.objects.filter(f_in71=in71_instance).update(c_asterik="*",c_nikappr=request.user.get_username())
                messages.add_message(request, messages.SUCCESS, 'Successfully Approved')
            except:
                messages.add_message(request, messages.ERROR, 'Approve Failed')
        else:
            try:
                TMIN72.objects.filter(f_in71=in71_instance).update(c_asterik="",c_nikappr="")
            except:
                pass

        # form validation and operations
        if in72_formset.is_valid() and func == 'add':
            # return HttpResponse(in72_formset)
            if not in71_instance.c_nikappr:
                messages.add_message(request, messages.ERROR, 'Failed, IN71 record must be approved') #change this
                return redirect(request.path)

            i = 0
            for form in in72_formset:
                clean_func = form.cleaned_data.get('func_sacd')
                obj = form.save(commit=False)

                related_added_in73 = TMIN73.objects.filter(f_in72=obj,c_asterik='*')
                if related_added_in73:
                    if clean_func:
                        messages.add_message(request, messages.ERROR, 'Operation Failed, Data has IN73 record') #change this
                else:
                    if clean_func == 'add':
                        obj.c_nik = request.user.get_username()
                        obj.d_create = now
                    elif clean_func == 'same':
                        obj.c_nik = request.user.get_username()
                        obj.i_qreceived = obj.i_qship
                    elif clean_func == 'change':
                        obj.c_nik = request.user.get_username()
                    elif clean_func == 'delete':
                        obj.i_qship = 0
                        obj.i_qreceived = 0

                    if clean_func:
                        try:
                            obj.save()
                            act_logging(request.user.get_username(),'IN72',clean_func,str(obj))
                            in72_is_saved = True
                            messages.add_message(request, messages.SUCCESS, 'Successfully') #change this
                        except:
                            in72_is_saved = False
                            messages.add_message(request, messages.ERROR, 'Operations Failed') #change this

                        if in72_is_saved:
                            if clean_func in ['same','add','change']:
                                try:
                                    in73_oo = TMIN73(f_in72=obj)
                                    in73_oo.save()
                                except:
                                    pass
                            elif clean_func == 'delete':
                                related_in73 = TMIN73.objects.get(f_in72=obj)
                                related_in73.delete()
                i += 1
            in72_instances = TMIN72.objects.filter(f_in71=in71_instance).order_by('i_itemno')
            in72_formset = FMIN72_set(queryset=in72_instances,error_class=DivErrorList)
            # return redirect(request.path)

    else:
        FMIN72_set = modelformset_factory(TMIN72,form=FMIN72)
        in71_form = FMIN71Q(error_class=DivErrorList)
        in72_formset = FMIN72_set(error_class=DivErrorList,queryset=TMIN72.objects.none())

    ctx = {
        'datetime_picker':True,
        'in71_form':in71_form,
        'in72_formset':in72_formset,
        'in71_instance':in71_instance,
        'in72_instances':in72_instances,
        'ivr7020h':ivr7020h,
        # 'instance':instance,
    }
    return render(request,template,ctx)

def in73(request,template='purchasing/f_in73.html'):
    now = datetime.now()
    year = now.strftime("%Y")
    in71_instance = None
    in73_instances = None
    ivr7020h = None
    #instantiate form based on request
    if request.method == "POST":
        func = request.POST.get('func') or None
        c_po = request.POST.get('c_po') or None
        d_received = request.POST.get('d_received') or None

        ivr7020h = IVR7020H.objects.filter(master=c_po).order_by('itm')
        if not ivr7020h:
            messages.add_message(request, messages.ERROR, 'MASTER %s not found' % c_po.upper()) #change this
            return redirect(request.path)

        try:
            in71_instance = TMIN71.objects.get(c_po=c_po,d_received=datetime.strptime(d_received,"%d %m %y"))
            in73_instances = TMIN73.objects.select_related('f_in72').filter(f_in72__f_in71=in71_instance).order_by('f_in72__i_itemno')


            # messages.add_message(request, messages.SUCCESS, 'Inquiry Success')
        except:
            messages.add_message(request, messages.ERROR, '%s - %s NOT FOUND' % (c_po.upper(),d_received))

        FMIN73_set = modelformset_factory(TMIN73,form=FMIN73)
        in71_form = FMIN71Q(instance=in71_instance,error_class=DivErrorList)
        if func in ['add']:
            in73_formset = FMIN73_set(request.POST,queryset=in73_instances,error_class=DivErrorList)
        else:
            in73_formset = FMIN73_set(queryset=in73_instances,error_class=DivErrorList)

        # in72_formset = FMIN72_set(queryset=in72_instances,error_class=DivErrorList)
        # cek auth and permission
        if func in ['add','approve']:
            if not request.user.is_authenticated:
                messages.add_message(request, messages.ERROR, 'Please login first') #change this
                return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
            if not request.user.has_perm('purchasing.%s_tmin73'%func):
                messages.add_message(request, messages.ERROR, 'Operations not permitted') #change this
                return redirect(request.path)

        # form validation and operations
        if in73_formset.is_valid():
            # return HttpResponse(in72_formset)
            i = 0
            for form in in73_formset:
                clean_func = form.cleaned_data.get('func_sacd')
                obj = form.save(commit=False)

                if clean_func and not obj.f_in72.c_nikappr:
                    messages.add_message(request, messages.ERROR, 'Failed, IN72 record must be approved') #change this
                    return redirect(request.path)

                if clean_func == 'add':
                    obj.c_nik = request.user.get_username()
                    obj.d_create = now
                    obj.c_asterik = '*'

                if clean_func:
                    try:
                        obj.save()
                        act_logging(request.user.get_username(),'IN73',clean_func,str(obj))
                        in73_is_saved = True
                        messages.add_message(request, messages.SUCCESS, 'Successfully') #change this
                    except:
                        in73_is_saved = False
                        messages.add_message(request, messages.ERROR, 'Operations Failed') #change this

                    if obj.i_qacc != obj.f_in72.i_qship:
                        if clean_func == 'add' and in73_is_saved:
                            no = TMIN76.objects.filter(Q(d_release__gte=str(year)+'-01-01') & Q(d_release__lte=str(year)+'-12-31')).aggregate(Max('c_drno'))['c_drno__max']
                            drno = int(no) + 1 if no else 1
                            reject = obj.f_in72.i_qship - obj.i_qacc
                            in76_oo = TMIN76(f_in73=obj,c_nik=request.user.get_username(),d_release=obj.f_in72.f_in71.d_create,i_qreject=reject,c_npo='0',c_drno=drno,c_sts=0)
                            try:
                                in76_oo.save()
                                act_logging(request.user.get_username(),'IN76',clean_func,str(in76_oo))
                            except:
                                pass

                i += 1
            in73_instances = TMIN73.objects.select_related('f_in72').filter(f_in72__f_in71=in71_instance).order_by('f_in72__i_itemno')
            in73_formset = FMIN73_set(queryset=in73_instances,error_class=DivErrorList)
            # return redirect(request.path)

    else:
        FMIN73_set = modelformset_factory(TMIN73,form=FMIN73)
        in71_form = FMIN71Q(error_class=DivErrorList)
        in73_formset = FMIN73_set(error_class=DivErrorList,queryset=TMIN73.objects.none())

    ctx = {
        'datetime_picker':True,
        'in71_form':in71_form,
        'in73_formset':in73_formset,
        'in71_instance':in71_instance,
        'in73_instances':in73_instances,
        'ivr7020h':ivr7020h,
        # 'instance':instance,
    }
    return render(request,template,ctx)

def in74(request,template='purchasing/f_in74.html'):
    if request.method == 'POST':
        func_cs = request.POST.get('func_cs')
        in73_id = request.POST.get('in73_id')
        if func_cs == 's':
            return redirect('/purchasing/in75/%s/' % in73_id)
        elif func_cs == 'c':
            return redirect('/purchasing/in69/%s/' % in73_id)

    in73_instances = TMIN73.objects.select_related('f_in72__f_in71').filter(Q(tmin75=None) & Q(d_create__isnull=False))
    in74_instances = []
    for ins in in73_instances:
        in74_instance = {}
        in74_instance['in73'] = ins
        in74_instance['ivr7020h'] = IVR7020H.objects.get(master=ins.f_in72.f_in71.c_po,itm=ins.f_in72.i_itemno)
        in74_instances.append(in74_instance)
    ctx = {
        'in74_instances':in74_instances,
        # 'instance':instance,
    }
    return render(request,template,ctx)
    # return HttpResponse(in74_instances.query)

def in75(request,in73_id,template='purchasing/f_in75.html'):
    if not request.user.has_perm('purchasing.add_tmin75'):
        messages.add_message(request, messages.ERROR, 'Operations not permitted') #change this
        return redirect('/purchasing/in74/')

    now = datetime.now()
    year = now.strftime("%Y")
    try:
        in73_instance = TMIN73.objects.select_related('f_in72__f_in71').get(pk=in73_id)
    except:
        in73_instance = None
    try:
        ivr7020h = IVR7020H.objects.get(master=in73_instance.f_in72.f_in71.c_po,itm=in73_instance.f_in72.i_itemno)
    except:
        ivr7020h = None
    try:
        in75_instance = TMIN75.objects.get(f_in73=in73_instance)
    except:
        in75_instance = None

    if request.method=="POST":
        form = FMIN75(request.POST,error_class=DivErrorList)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.f_in73 = in73_instance
            no = TMIN75.objects.filter(Q(d_create__gte=str(year)+'-01-01') & Q(d_create__lte=str(year)+'-12-31')).aggregate(Max('c_recvno'))['c_recvno__max']
            recvno = int(no) + 1 if no else 1
            obj.c_recvno = recvno
            obj.d_create = now
            obj.c_nik = request.user.get_username()
            try:
                obj.save()
                act_logging(request.user.get_username(),'IN75','store',str(obj))
                messages.add_message(request, messages.SUCCESS, 'Successfully') #change this

            except:
                messages.add_message(request, messages.ERROR, 'Failed, data already exist') #change this
            return redirect(request.path)
    else:
        form = FMIN75(instance=in75_instance,error_class=DivErrorList)

    ctx = {'in73_instance':in73_instance,'ivr7020h':ivr7020h,'form':form}
    return render(request,template,ctx)
    # return HttpResponse(ivr7020h)

def in76(request,template='purchasing/f_in76.html'):
    in76_instances = TMIN76.objects.select_related('f_in73__f_in72__f_in71').all()
    ctx = {
        'in76_instances':in76_instances,
        # 'instance':instance,
    }
    return render(request,template,ctx)

def in77(request,template='purchasing/f_in77.html'):
    in77_instance = None
    ivr7020h = None
    if request.method == "POST":
        func = request.POST.get('func')
        recv = request.POST.get('recv')
        year = datetime.strptime(recv[1:3],"%y")
        # return HttpResponse(in77_instance)
        try:
            in77_instance = TMIN75.objects.select_related('f_in73__f_in72__f_in71').get(Q(d_create__gte=year.strftime("%Y")+'-01-01') & Q(d_create__lte=year.strftime("%Y")+'-12-31') & Q(c_recvno=int(recv[3:8])) )
            ivr7020h = IVR7020H.objects.get(master=in77_instance.f_in73.f_in72.f_in71.c_po,itm=in77_instance.f_in73.f_in72.i_itemno)
        except:
            pass
    ctx = {
        'obj':in77_instance,
        'ivr7020h':ivr7020h,
        # 'instance':instance,
    }
    return render(request,template,ctx)
