from datetime import date
from django import forms
from django.db.models import Avg, Count, Min, Sum, Q

from purchasing.models import *

from django import forms
from django.forms.models import formset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class RangeDateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit("submit", "Submit"))

    begin_date = forms.DateField()
    end_date = forms.DateField()

class FMIN71(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        if 'action' in kwargs:
            self.action = kwargs.pop('action')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.fields['c_nikappr'].widget.attrs['readonly'] = True
        if self.action in ['add'] :
            self.helper.add_input(Submit("submit", "Save"))
        elif self.action in ['change'] :
            self.helper.add_input(Submit("submit", "Save"))
            self.fields['c_po'].widget.attrs['readonly'] = True
            self.fields['d_received'].widget.attrs['readonly'] = True
        elif self.action in ['detail','print']:
            for k,v in self.fields.items() :
                v.widget.attrs['readonly'] = True
                v.widget.attrs['disabled'] = True

    def is_future(self,value,field):
        today = date.today()
        if value and value > today:
            self.add_error(field,'date cannot be in the future')
            return True

    def clean_c_nikappr(self):
        return ''

    def clean_c_po(self):
        return self.instance.c_po if self.instance.pk else self.cleaned_data['c_po']

    def clean_d_received(self):
        return self.instance.d_received if self.instance.pk else self.cleaned_data['d_received']

    def clean_c_po(self):
        return self.cleaned_data['c_po'].upper()

    def clean(self):
        cleaned_data = super().clean()
        self.is_future(cleaned_data.get('d_received'),'d_received')
        ivr7020h = IVR7020H.objects.filter(master=cleaned_data['c_po'])
        if ivr7020h :
            if ivr7020h[0].s1 in ['0','1','2','C']:
                self.add_error('c_po','PO berstatus %s'%ivr7020h[0].s1)
            else:
                field_foreign_c = ["c_awb","c_hawb","c_bc23","c_aju"]
                field_foreign_d = ["d_awb","d_hawb","d_bc23","d_aju"]
                if ivr7020h[0].f1 == 'F':
                    msg = "Please fill out this field"
                    for f in [ *field_foreign_c,*field_foreign_d ]:
                        if not cleaned_data.get(f):
                            self.add_error(f,msg)
                    for d in field_foreign_d:
                        self.is_future(cleaned_data.get(d),d)
                else:
                    for fc in field_foreign_c:
                        cleaned_data[fc] = ''
                    for fd in field_foreign_d:
                        cleaned_data[fd] = None

                if self.action in ['add','change']:
                    msg = "Please fill out this field"
                    for f in ["c_invoice","c_packinglist","c_negaraasal"]:
                        if not cleaned_data.get(f):
                            self.add_error(f,msg)
        else:
            self.add_error('c_po','Master PO Not found')

                # raise forms.ValidationError("Invoice harus di isi")

    class Meta:
        model = TMIN71
        exclude = ['d_create','c_nik']
        labels = {
            'd_create' : 'CREATE',
            'c_nikappr' : 'APPR',
            'c_po' : 'MASTER#',
            'd_received' : 'DATE-RECEIVED',
            'b_isclosedr' : 'CLOSE-DR(Y)',
            'c_invoice' : 'INVOICE#',
            'c_packinglist' : 'PACKING-LIST#',
            'c_boxno' : 'BOX-NO',
            'e_certificate' : 'CERTIFICATE',
            'e_other' : 'OTHER',
            'c_awb' : 'AWB/BL/SJ',
            'd_awb' : 'AWB-DATE',
            'c_hawb' : 'HAWB',
            'd_hawb' : 'HAWB-DATE',
            'c_bc23' : 'BPBI/BL-BC23',
            'd_bc23' : 'TGL-BC23',
            'c_negaraasal' : 'NEGARA-ASAL',
            'c_aju' : 'NOMOR-AJU',
            'd_aju' : 'TGL-AJU',
        }


class FMIN72(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        if 'action' in kwargs:
            self.action = kwargs.pop('action')
        if 'fk' in kwargs:
            self.fk = kwargs.pop('fk')
            self.robj = TMIN71.objects.get(pk=self.fk)
            self.ivr7020h = IVR7020H.objects.filter(master=self.robj.c_po)
            self.i_itemno_choices = []
            for iv in self.ivr7020h:
                exist = TMIN72.objects.filter(f_in71=self.robj,i_itemno=iv.itm)
                if not exist:
                    obj = TMIN72.objects.filter(f_in71__c_po=self.robj.c_po,i_itemno=iv.itm).aggregate(Sum('i_qship'),Sum('i_qreceived'))
                    if not obj['i_qreceived__sum'] or iv.qty > obj['i_qreceived__sum'] :
                        self.i_itemno_choices.append((iv.itm,'ITEM %s - %s'%(iv.itm,iv.partnumber)))

        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.fields['c_nikappr'].widget.attrs['readonly'] = True
        if self.action in ['add'] :
            self.fields['i_itemno'].widget.choices = self.i_itemno_choices
            self.helper.add_input(Submit("submit", "Save"))
        if self.action in ['change'] :
            self.fields['i_itemno'].widget.choices = [(self.instance.i_itemno,'ITEM %s - %s'%(self.instance.i_itemno,self.instance.c_partnumber))]
            self.fields['i_itemno'].widget.attrs['readonly'] = True
            self.helper.add_input(Submit("submit", "Save"))

    def clean_c_nikappr(self):
        return ''

    def clean_c_partin(self):
        return self.instance.c_partin if self.instance.pk else self.cleaned_data['c_partin'].upper()

    def clean_i_itemno(self):
        return self.instance.i_itemno if self.instance.pk else self.cleaned_data['i_itemno']

    def clean(self):
        cleaned_data = super().clean()
        exclude = Q(pk=self.instance.pk) if self.instance.pk else Q()
        if cleaned_data.get('i_itemno'):
            ivr = IVR7020H.objects.get(master=self.robj.c_po,itm=self.cleaned_data.get('i_itemno'))
            obj = TMIN72.objects.exclude(exclude).filter(f_in71__c_po=self.robj.c_po,i_itemno=self.cleaned_data.get('i_itemno')).aggregate(Sum('i_qship'),Sum('i_qreceived'))
            cleaned_data['c_partnumber'] = ivr.partnumber
            cleaned_data['n_um'] = ivr.um
            qship = cleaned_data.get('i_qship')
            qreceived = cleaned_data.get('i_qreceived')
            total_qship = obj.get('i_qship__sum') or 0
            if (total_qship + qship) > ivr.qty:
                self.add_error('i_qship','QTY Ship tidak boleh lebih besar dari QTY PO (%s), QTY Ship kedatangan sebelumnya (%s), QTY Ship valid (%s)'%(ivr.qty,total_qship,(ivr.qty - total_qship)))
            if qreceived > qship:
                self.add_error('i_qreceived','QTY Received tidak boleh lebih besar dari QTY Ship')
        else:
            self.add_error('i_itemno','Please fill out this field')

    class Meta:
        model = TMIN72
        fields = ('c_nikappr','i_itemno','i_qship','i_qreceived','c_partin','n_um','c_partnumber',)
        labels = {
            'c_nikappr' : 'APPR',
            'i_itemno' : 'ITEM#',
            'i_qship' : 'SHIP',
            'i_qreceived' : 'RECEIVED',
            'c_partin' : 'PART-IN#',
        }
        widgets = {
            'n_um' : forms.HiddenInput(),
            'c_partnumber' : forms.HiddenInput(),
            'i_itemno' : forms.Select(),
            'i_qship' : forms.NumberInput(attrs={'step':'0.01','placeholder':'0.00','required':'required'}),
            'i_qreceived' : forms.NumberInput(attrs={'step':'0.01','placeholder':'0.00','required':'required'}),
        }

class FMIN73(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        if 'action' in kwargs:
            self.action = kwargs.pop('action')
        if 'fk' in kwargs:
            self.fk = kwargs.pop('fk')
            self.robj = TMIN71.objects.get(pk=self.fk)
        if 'ook' in kwargs:
            self.ook = kwargs.pop('ook')
            self.oobj = TMIN72.objects.get(pk=self.ook)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit("submit", "Save"))
        self.fields['f_in72'].queryset=TMIN72.objects.filter(pk=self.ook)
        self.fields['f_in72'].initial=self.oobj

    def clean_c_cert(self):
        return self.cleaned_data['c_cert'].upper()
    def clean_c_e(self):
        return self.cleaned_data['c_e'].upper()
    def clean_c_cond(self):
        return self.cleaned_data['c_cond'].upper()

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['i_qacc'] > self.oobj.i_qship:
            self.add_error('i_qacc','QTY Accept tidak boleh lebih besar dari QTY Ship (%s)'%self.oobj.i_qship)

    class Meta:
        model = TMIN73
        fields = ('f_in72','i_qacc','c_cert','c_e','c_cond')
        labels = {
            'f_in72' : 'ITEM# - P/N#',
            'i_itemno' : 'ITEM#',
            'i_qacc' : 'ACCEPT',
            'c_cert' : 'CERTIFICATE',
            'c_e' : 'ELIGIBILITY',
            'c_cond' : 'CONDITION',
        }
        widgets = {
            'i_qacc' : forms.NumberInput(attrs={'required':'required'}),

        }
