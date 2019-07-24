import io
from django.shortcuts import render, redirect
from django.db.models import F,Q,Max,Prefetch
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.forms import modelformset_factory
from django.core.paginator import Paginator
from purchasing.forms01 import *
from purchasing.models import *
from purchasing.views01E import in71_export_prn,in72_export_prn,in73_export_prn
from authnest.views00 import act_logging
from authnest.helper import get_prev_url,create_prev_url,check_permission,check_fk
from ui.forms import *
from datetime import datetime

default_mnactive = 'mnpurchasing1'

def in71_list(request,template='ui/list_default.html'):
    if request.method == 'POST':
        kw = request.POST.get('kw')
        obj = TMIN71.objects.filter(Q(c_po__icontains=kw) | Q(d_received__icontains=kw))
    else :
        objs = TMIN71.objects.all()
        paginator = Paginator(objs, 100) # Show 25 contacts per page
        page = request.GET.get('page')
        obj = paginator.get_page(page)

    judul = 'IN71 List'
    field = {
        'c_po':'Master#',
        'd_received':'Received',
        'd_create':'Created',
        'c_invoice':'Invoice',
        'c_packinglist':'Packing List',
        'c_nikappr':'Appr By',
    }
    act_link = "/purchasing-v1/in71/"
    action = ['detail','change','delete','approve','print',]
    act_method = {'detail':'modal','change':'modal','delete':'link','approve':'link','print':'modal',}

    relation = {'IN72':'/purchasing-v1/in72/','IN73':'/purchasing-v1/in73/'}

    full_path = create_prev_url(request)
    ctx = {
        'obj':obj,
        'judul':judul,
        'mnactive':default_mnactive,
        'field':field,
        'action':action,
        'act_link':act_link,
        'act_method':act_method,
        'full_path':full_path,
        'relation':relation,
        'can_add':True,
        'export':'/purchasing-v1/in71/in72/in73/prn/',
    }
    return render(request,template,ctx)

def in71_print(request,pk,template='purchasing/in71_print.html'):
    from weasyprint import HTML, CSS
    from io import StringIO,BytesIO
    from django.template.loader import get_template
    now = datetime.now()
    judul = 'IN71 Print'
    prev_url = get_prev_url(request,'/purchasing-v1/in71/list')
    perm = check_permission(request,'purchasing.print_tmin71',prev_url,True)
    if perm: return perm
    # prev_url = request.META.get('HTTP_REFERER') or '/purchasing-v1/in71/list'
    try:
        obj = TMIN71.objects.prefetch_related(Prefetch('tmin72_set',queryset=TMIN72.objects.select_related('tmin73').all())).get(pk=pk)
        ivr = IVR7020H.objects.filter(master=obj.c_po)[0]
    except:
        return redirect(prev_url)


    for in72 in obj.tmin72_set.all():
        in72.ivr = IVR7020H.objects.get(master=obj.c_po,itm=in72.i_itemno)

    ctx = {
        'judul':judul,
        'mnactive':default_mnactive,
        'obj':obj,
        'ivr':ivr,
        'prev_url':prev_url,
        'datepickerScript': True,
    }
    tpl = get_template(template)
    html = tpl.render(ctx)
    css = CSS(string=
                """
                @page {
                    size: A4; margin-top: 2cm; margin-bottom: 2cm;
                    @bottom{
                        font-size:10pt;
                    }
                    @bottom-left{
                        content: "FORM NO. PRO3-2";
                    }
                    @bottom-center{
                        content: "PRINTED: %s   BY: %s";
                    }
                    @bottom-right{
                        content: "Page " counter(page) " of " counter(pages);
                    }
                 }
                """%(now.strftime("%d%b%y %H:%M").upper(),request.user.get_username())
            )
    # fonts = CSS(settings.STATICFILES_DIRS[0] +  '/struk_gaji/fonts/font.css', font_config=font_config)
    pdf_file = HTML(string=html,base_url=request.build_absolute_uri()).write_pdf(stylesheets=[css])
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="IN71.pdf"'
    return response

    # return render(request,template,ctx)


def in71_detail(request,pk,template='ui/form_default.html'):
    judul = 'IN71 Detail'
    prev_url = get_prev_url(request,'/purchasing-v1/in71/list')
    # prev_url = request.META.get('HTTP_REFERER') or '/purchasing-v1/in71/list'
    try:
        obj = TMIN71.objects.get(pk=pk)
    except:
        return redirect(prev_url)
    form = FMIN71(instance=obj,action='detail')
    ctx = {
        'judul':judul,
        'mnactive':default_mnactive,
        'form':form,
        'prev_url':prev_url,
        'datepickerScript': True,
    }
    return render(request,template,ctx)

def in71_add(request,template='ui/form_default.html'):
    prev_url = get_prev_url(request,'/purchasing-v1/in71/list')
    perm = check_permission(request,'purchasing.add_tmin71',prev_url,True)
    if perm: return perm

    judul = 'IN71 Add'
    form = FMIN71(request.POST or None,action='add')
    if form.is_valid():
        obj = form.save(commit=False)
        # return HttpResponse(obj.d_received)
        obj.d_create = datetime.now()
        obj.save()
        messages.add_message(request, messages.SUCCESS, 'kedatangan %s berhasil ditambahkan'%obj)
        return redirect(request.path)
    ctx = {
        'judul':judul,
        'mnactive':default_mnactive,
        'form':form,
        'prev_url':prev_url,
        'datepickerScript': True,
        'submit': True,
    }
    return render(request,template,ctx)

def in71_change(request,pk,template='ui/form_default.html'):
    prev_url = get_prev_url(request,'/purchasing-v1/in71/list')
    perm = check_permission(request,'purchasing.change_tmin71',prev_url)
    if perm: return perm

    judul = 'IN71 Change'
    try:
        obj = TMIN71.objects.get(pk=pk)
    except:
        return redirect(prev_url)
    form = FMIN71(request.POST or None,instance=obj,action='change')
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.add_message(request, messages.SUCCESS, 'kedatangan %s berhasil diubah'%obj)
        return redirect(request.path)
    ctx = {
        'judul':judul,
        'mnactive':default_mnactive,
        'form':form,
        'prev_url':prev_url,
        'datepickerScript': True,
        'submit': True,
    }
    return render(request,template,ctx)

def in71_delete(request,pk):
    prev_url = get_prev_url(request,'/purchasing-v1/in71/list')
    perm = check_permission(request,'purchasing.delete_tmin71',prev_url)
    if perm: return perm

    try:
        obj = TMIN71.objects.get(pk=pk)
        obj.delete()
        messages.add_message(request, messages.SUCCESS, 'Successfully Deleted')
    except:
        messages.add_message(request, messages.ERROR, 'Opertaion Failed')
    return redirect(prev_url)

def in71_approve(request,pk):
    prev_url = get_prev_url(request,'/purchasing-v1/in71/list')
    perm = check_permission(request,'purchasing.approve_tmin71',prev_url)
    if perm: return perm

    try:
        obj = TMIN71.objects.get(pk=pk)
        obj.c_nikappr = request.user.get_username()
        obj.d_appr = datetime.now()
        obj.save()
        messages.add_message(request, messages.SUCCESS, 'Successfully Approved')
    except:
        messages.add_message(request, messages.ERROR, 'Opertaion Failed')
    return redirect(prev_url)


def in72_list(request,fk,template='ui/list_default.html'):
    prev_url = get_prev_url(request,'/purchasing-v1/in71/list')
    fk_not_related = check_fk(request,fk,TMIN71,prev_url)
    if fk_not_related: return fk_not_related

    filter = Q(f_in71__pk=fk)
    if request.method == 'POST':
        kw = request.POST.get('kw')
        obj = TMIN72.objects.filter(filter & (Q(i_itemno__icontains=kw) | Q(i_partnumber__icontains=kw)))
    else :
        objs = TMIN72.objects.filter(filter)
        paginator = Paginator(objs, 100) # Show 25 contacts per page
        page = request.GET.get('page')
        obj = paginator.get_page(page)

    judul = 'IN72 List'
    field = {
        'i_itemno':'Item#',
        'c_partnumber':'PartNumber#',
        'i_qship':'Ship',
        'n_um':'UM',
        'i_qreceived':'Received',
        'c_partin':'PartIn#',
        'c_nikappr':'Appr By',
    }
    act_link = "/purchasing-v1/in72/%s/"%fk
    action = ['change','delete','approve',]
    act_method = {'change':'modal','delete':'link','approve':'link',}
    full_path = create_prev_url(request)
    ctx = {
        'obj':obj,
        'judul':judul,
        'mnactive':default_mnactive,
        'field':field,
        'prev_url':prev_url,
        'action':action,
        'act_link':act_link,
        'act_method':act_method,
        'full_path':full_path,
        'can_add':True,
        'can_approve_all':True,
    }
    return render(request,template,ctx)

def in72_add(request,fk,template='ui/form_default.html'):
    prev_url = get_prev_url(request,'/purchasing-v1/in72/%s/list'%fk)
    perm = check_permission(request,'purchasing.add_tmin72',prev_url)
    if perm: return perm

    judul = 'IN72 Add'
    form = FMIN72(request.POST or None,action='add',fk=fk)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.d_create = datetime.now()
        obj.c_nik = request.user.get_username()
        obj.f_in71 = form.robj
        obj.save()
        messages.add_message(request, messages.SUCCESS, '%s berhasil ditambahkan, silahkan tambah item selanjutnya'%obj)
        return redirect(request.path)
    ctx = {
        'judul':judul,
        'mnactive':default_mnactive,
        'form':form,
        'prev_url':prev_url,
        'datepickerScript': True,
        'submit': True,
    }
    return render(request,template,ctx)

def in72_change(request,fk,pk,template='ui/form_default.html'):
    prev_url = get_prev_url(request,'/purchasing-v1/in72/%s/list'%fk)
    perm = check_permission(request,'purchasing.change_tmin72',prev_url)
    if perm: return perm
    try:
        obj = TMIN72.objects.get(pk=pk)
    except:
        return redirect(prev_url)
    judul = 'IN72 Change'
    form = FMIN72(request.POST or None,instance=obj,action='change',fk=fk)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.c_nik = request.user.get_username()
        obj.save()
        messages.add_message(request, messages.SUCCESS, '%s berhasil diubah'%obj)
        return redirect(request.path)
    ctx = {
        'judul':judul,
        'mnactive':default_mnactive,
        'form':form,
        'prev_url':prev_url,
        'datepickerScript': True,
        'submit': True,
    }
    return render(request,template,ctx)


def in72_delete(request,fk,pk):
    prev_url = get_prev_url(request,'/purchasing-v1/in72/%s/list'%fk)
    perm = check_permission(request,'purchasing.delete_tmin72',prev_url)
    if perm: return perm

    try:
        obj = TMIN72.objects.get(pk=pk)
        obj.delete()
        messages.add_message(request, messages.SUCCESS, 'Successfully Deleted')
    except:
        messages.add_message(request, messages.ERROR, 'Opertaion Failed')
    return redirect(prev_url)

def in72_approve(request,fk,pk):
    prev_url = get_prev_url(request,'/purchasing-v1/in72/%s/list'%fk)
    perm = check_permission(request,'purchasing.approve_tmin72',prev_url)
    if perm: return perm

    try:
        obj = TMIN72.objects.get(pk=pk)
        obj.c_nikappr = request.user.get_username()
        obj.d_appr = datetime.now()
        obj.save()
        messages.add_message(request, messages.SUCCESS, 'Successfully Approved')
    except:
        messages.add_message(request, messages.ERROR, 'Opertaion Failed')
    return redirect(prev_url)

def in72_approve_all(request,fk):
    prev_url = get_prev_url(request,'/purchasing-v1/in72/%s/list'%fk)
    perm = check_permission(request,'purchasing.approve_tmin72',prev_url)
    if perm: return perm

    try:
        objs = TMIN72.objects.filter(f_in71__pk=fk)
        for obj in objs:
            obj.c_nikappr = request.user.get_username()
            obj.d_appr = datetime.now()
            obj.save()
        messages.add_message(request, messages.SUCCESS, 'Successfully Approved')
    except:
        messages.add_message(request, messages.ERROR, 'Opertaion Failed')
    return redirect(prev_url)

def in73_list(request,fk,template='ui/list_default.html'):
    prev_url = get_prev_url(request,'/purchasing-v1/in71/list')
    fk_not_related = check_fk(request,fk,TMIN71,prev_url)
    if fk_not_related: return fk_not_related

    filter = Q(Q(f_in71__pk=fk) & ~Q(c_nikappr=''))
    if request.method == 'POST':
        kw = request.POST.get('kw')
        obj = TMIN72.objects.select_related('tmin73').filter(filter & (Q(i_itemno__icontains=kw) | Q(i_partnumber__icontains=kw)))
    else :
        objs = TMIN72.objects.select_related('tmin73').filter(filter)
        paginator = Paginator(objs, 100) # Show 25 contacts per page
        page = request.GET.get('page')
        obj = paginator.get_page(page)

    judul = 'IN73 List'
    field = {
        'i_itemno':'Item#',
        'c_partnumber':'PartNumber#',
        'i_qship':'Ship',
        'tmin73.i_qacc':'Accept',
        'tmin73.c_cert':'Certificate',
        'tmin73.c_e':'Eligibility',
        'tmin73.c_cond':'Condition',
        'c_partin':'PartIn#',
        'c_nikappr':'Appr By',
    }
    act_link = "/purchasing-v1/in73/%s/"%fk
    action = ['add',]
    act_method = {'add':'modal',}

    full_path = create_prev_url(request)
    ctx = {
        'obj':obj,
        'judul':judul,
        'mnactive':default_mnactive,
        'field':field,
        'prev_url':prev_url,
        'action':action,
        'act_link':act_link,
        'act_method':act_method,
        'full_path':full_path,
    }
    return render(request,template,ctx)

def in73_add(request,fk,ook,template='ui/form_default.html'):
    prev_url = get_prev_url(request,'/purchasing-v1/in73/%s/list'%fk)
    perm = check_permission(request,'purchasing.add_tmin73',prev_url)
    if perm: return perm
    fk_not_related = check_fk(request,ook,TMIN72,prev_url,True)
    if fk_not_related: return fk_not_related
    try :
        obj = TMIN73.objects.get(f_in72__pk=ook)
    except :
        obj = None
    judul = 'IN73 Add'
    form = FMIN73(request.POST or None,action='add',fk=fk,ook=ook,instance=obj)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.d_create = datetime.now()
        obj.c_nik = request.user.get_username()
        obj.save()
        messages.add_message(request, messages.SUCCESS, '%s berhasil ditambahkan'%obj)
        return redirect(request.path)
    ctx = {
        'judul':judul,
        'mnactive':default_mnactive,
        'form':form,
        'prev_url':prev_url,
        'datepickerScript': True,
        'submit': True,
    }
    return render(request,template,ctx)

def in71_in72_in73_prn_get(request,template='ui/form_default.html'):
    prev_url = get_prev_url(request,'/purchasing-v1/in71/list')
    perm = check_permission(request,'purchasing.add_tmin73',prev_url,True)
    if perm: return perm
    import zipfile
    judul = 'IN71 IN72 IN73 PRN Download'
    form = RangeDateForm(request.POST or None)
    if form.is_valid():
        zip_filename = "IN71_IN72_IN73"
        b = form.cleaned_data['begin_date']
        e = form.cleaned_data['end_date']
        io_zip = io.BytesIO()
        myzip = zipfile.ZipFile(io_zip, 'w')
        myzip.writestr('in71.txt',in71_export_prn(b,e))
        myzip.writestr('in72.txt',in72_export_prn(b,e))
        myzip.writestr('in73.txt',in73_export_prn(b,e))
        myzip.close()
        resp = HttpResponse(io_zip.getvalue(), content_type="application/x-zip-compressed")
        resp['Content-Disposition'] = 'attachment; filename=%s_%s-%s.zip' % (zip_filename,b.strftime("%y%m%d"),e.strftime("%y%m%d"))
        return resp
    ctx = {
        'judul':judul,
        'mnactive':default_mnactive,
        'form':form,
        'prev_url':prev_url,
        'datepickerScript': True,
        'submit': True,
    }
    return render(request,template,ctx)
