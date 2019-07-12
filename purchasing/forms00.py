from django import forms
from purchasing.models import *


class FMIN71(forms.ModelForm):
    func = forms.ChoiceField(label='FUNC',choices=(('','-'),('add','A'),('change','C'),('inquiry','I'),('print','P'),('approve','R')),widget=forms.Select(attrs={'maxlength':'1','class':'field-func','id':'field-func'}))

    def _required(self):
        cleaned_data = super().clean()
        msg = "Please fill out this field"
        for f in ["c_invoice","c_packinglist","c_boxno","c_negaraasal"]:
            if not cleaned_data.get(f):
                self.add_error(f,msg)

    def clean_c_po(self):
        return self.cleaned_data['c_po'].upper()

    def clean(self):
        cleaned_data = super().clean()
        func = cleaned_data.get("func")

        if func in ['change','print','approve']:
            if self.instance.pk == None:
                self.add_error('func','Plese inquiry data first')
            else:
                if func == 'change':
                    self._required()

        if func in ['add']:
            self._required()
                    # raise forms.ValidationError("Invoice harus di isi")

    class Meta:
        model = TMIN71
        exclude = ['d_create','c_nikappr']
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
        widgets = {
            'c_po' : forms.TextInput(attrs={'size':'10','required':'true'}),
            'd_received' : forms.DateInput(attrs={'class':'masked dateinput-dmy','pattern':'([0-2]\d|3[0-1])\s(1[0-2]|0[1-9])\s([0-2]\d|[7-9]\d)','size':'10','required':'true'}),
            'e_other' : forms.TextInput(attrs={'size':'29'}),
            'd_awb' : forms.DateInput(attrs={'class':'masked dateinput-dmy','pattern':'([0-2]\d|3[0-1])\s(1[0-2]|0[1-9])\s([0-2]\d|[7-9]\d)'}),
            'd_hawb' : forms.DateInput(attrs={'class':'masked dateinput-dmy','pattern':'([0-2]\d|3[0-1])\s(1[0-2]|0[1-9])\s([0-2]\d|[7-9]\d)'}),
            'd_bc23' : forms.DateInput(attrs={'class':'masked dateinput-dmy','pattern':'([0-2]\d|3[0-1])\s(1[0-2]|0[1-9])\s([0-2]\d|[7-9]\d)'}),
            'd_aju' : forms.DateInput(attrs={'class':'masked dateinput-dmy','pattern':'([0-2]\d|3[0-1])\s(1[0-2]|0[1-9])\s([0-2]\d|[7-9]\d)'}),
        }

class FMIN71Q(forms.ModelForm):
    func = forms.ChoiceField(label='FUNCTION',choices=(('','-'),('add','A'),('inquiry','I'),('approve','R')),widget=forms.Select(attrs={'maxlength':'1','class':'field-func','id':'field-func'}))

    class Meta:
        model = TMIN71
        fields = ['c_po','d_received']
        labels = {
            'c_po' : 'MASTER# ',
            'd_received' : 'RECEIVED',
        }
        widgets = {
            'c_po' : forms.TextInput(attrs={'size':'10','required':'true'}),
            'd_received' : forms.DateInput(attrs={'class':'masked dateinput-dmy','pattern':'([0-2]\d|3[0-1])\s(1[0-2]|0[1-9])\s([0-2]\d|[7-9]\d)','size':'10','required':'true'}),
        }

class FMIN72(forms.ModelForm):
    func_sacd = forms.ChoiceField(label='SACD',required=False,choices=(('',''),('same','S'),('add','A'),('change','C'),('delete','D')),widget=forms.Select(attrs={'maxlength':'1','class':'field-func','id':'field-func-sacd'}))

    def clean_c_asterik(self):
        return self.instance.c_asterik if self.instance.pk else self.cleaned_data['c_asterik'].upper()
    def clean_c_partnumber(self):
        return self.instance.c_partnumber if self.instance.pk else self.cleaned_data['c_partnumber'].upper()
    def clean_c_partin(self):
        return self.instance.c_partin if self.instance.pk else self.cleaned_data['c_partin'].upper()
    def clean_n_um(self):
        return self.instance.n_um if self.instance.pk else self.cleaned_data['n_um'].upper()
    def clean_i_itemno(self):
        return self.instance.i_itemno if self.instance.pk else self.cleaned_data['i_itemno']

    def clean(self):
        cleaned_data = super().clean()
        func_sacd = cleaned_data.get("func_sacd")

        if func_sacd == 'change':
            if self.cleaned_data.get("c_asterik") != '*':
                self.add_error('func_sacd','Please add data first before change')

    class Meta:
        model = TMIN72
        fields = ('c_asterik','c_partnumber','c_partin','n_um','i_itemno','i_qreceived','i_qship')
        widgets = {
            'c_asterik' : forms.TextInput(attrs={'readonly':'readonly'}),
            'c_partnumber' : forms.TextInput(attrs={'readonly':'readonly'}),
            'c_partin' : forms.TextInput(attrs={'readonly':'readonly'}),
            'n_um' : forms.TextInput(attrs={'readonly':'readonly'}),
            'i_itemno' : forms.TextInput(attrs={'readonly':'readonly','size':'3','style':'color:turquoise','class':'zeropad text-right','data-zeropad':'3'}),
            'i_qreceived' : forms.TextInput(attrs={'size':'9','class':'text-right','pattern':'([0-9]{0,6})|([0-9]{0,6}\.[0-9]{0,2})'}),
            'i_qship' : forms.TextInput(attrs={'size':'9','class':'text-right','pattern':'([0-9]{0,6})|([0-9]{0,6}\.[0-9]{0,2})'}),
        }

class FMIN73(forms.ModelForm):
    func_sacd = forms.ChoiceField(label='Add',required=False,choices=(('',''),('add','A')),widget=forms.Select(attrs={'maxlength':'1','class':'field-func','id':'field-func-sacd',}))

    def clean_c_cert(self):
        return self.cleaned_data['c_cert'].upper()

    def clean(self):
        cleaned_data = super().clean()
        func_sacd = cleaned_data.get("func_sacd")

        if func_sacd == 'add':
            if self.cleaned_data.get("c_asterik") == '*':
                self.add_error('func_sacd','Data already added')
    class Meta:
        model = TMIN73
        fields = ('c_asterik','i_qacc','c_cert','c_e','c_cond',)
        widgets = {
            'c_asterik' : forms.TextInput(attrs={'readonly':'readonly'}),
            'i_qacc' : forms.TextInput(attrs={'size':'9','class':'text-right','pattern':'([0-9]{0,6})|([0-9]{0,6}\.[0-9]{0,2})'}),
            'c_cert' : forms.TextInput(attrs={'size':'1','class':'text-right','pattern':'([1-9]|[a-r]|[A-R]){1}'}),
            'c_e' : forms.TextInput(attrs={'size':'1','class':'text-right','pattern':'([1-8]){0,1}'}),
            'c_cond' : forms.TextInput(attrs={'size':'1','class':'text-right','pattern':'([1-9]{1})'}),
        }

class FMIN75(forms.ModelForm):

    class Meta:
        model = TMIN75
        fields = ('c_owner','c_bin',)
        widgets = {
            'c_owner' : forms.TextInput(attrs={'size':'4'}),
            'c_bin' : forms.TextInput(attrs={'size':'10'}),
        }
