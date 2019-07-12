from django import forms

class LoginForm(forms.Form):
    nik = forms.CharField(label='NIK',widget=forms.TextInput(attrs={'placeholder':'NIK'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
