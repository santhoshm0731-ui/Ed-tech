from django import forms
from django.contrib.auth.models import User
from .models import School  # import your School model

class SignupForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    year = forms.IntegerField(
        min_value=1,
        max_value=2025,  # assuming school year 1-12
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    school = forms.ModelChoiceField(
        queryset=School.objects.all(),  # fetch all schools from DB
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Passwords do not match')

        if User.objects.filter(username=cleaned.get('username')).exists():
            raise forms.ValidationError('Username already exists')

        if User.objects.filter(email=cleaned.get('email')).exists():
            raise forms.ValidationError('Email already exists')

        return cleaned
