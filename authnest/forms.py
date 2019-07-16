from django import forms

class LoginForm(forms.Form):
    nik = forms.CharField(label='NIK',widget=forms.TextInput(attrs={'placeholder':'NIK','class':'form-control col border-bottom-0','id':'nik'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control col','id':'password'}))
