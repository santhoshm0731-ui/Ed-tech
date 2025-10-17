from django import forms
from django.contrib.auth.models import User
from .models import School

class SignupForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    year = forms.IntegerField(min_value=1, max_value=2025, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Year (1-12)'}))
    school = forms.ModelChoiceField(queryset=School.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 != p2:
            raise forms.ValidationError("Passwords do not match")
        if User.objects.filter(username=cleaned.get('username')).exists():
            raise forms.ValidationError("Username already exists")
        if User.objects.filter(email=cleaned.get('email')).exists():
            raise forms.ValidationError("Email already exists")
        return cleaned

class TeacherSignupForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    school = forms.ModelChoiceField(queryset=School.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 != p2:
            raise forms.ValidationError("Passwords do not match")
        if User.objects.filter(username=cleaned.get('username')).exists():
            raise forms.ValidationError("Username already exists")
        if User.objects.filter(email=cleaned.get('email')).exists():
            raise forms.ValidationError("Email already exists")
        return cleaned
