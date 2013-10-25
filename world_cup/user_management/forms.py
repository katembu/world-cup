from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class CreateUserForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Verify Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']

        raise forms.ValidationError("Username taken.")

    def clean_email(self):
        try:
            User.objects.get(email=self.cleaned_data['email'])
        except:
            return self.cleaned_data['email']

        raise forms.ValidationError("Email being used.")

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match.")

        return self.cleaned_data

    def save(self):
        new_user = User.objects.create_user(self.cleaned_data['username'],
                                            self.cleaned_data['email'],
                                            self.cleaned_data['password1'])
        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        new_user.save()
        new_user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password1'])
        return new_user
