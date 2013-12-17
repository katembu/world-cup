from django import forms
from django.contrib.auth import authenticate
from user_management.models import CustomUser as User
from user_management.models import UserMessages
from tournament.models import CompetitiveGroups


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


class MessageForm(forms.Form):
    to = forms.CharField(required=False, max_length=255,
                         widget=forms.TextInput(attrs={'class': 'form-control typeahead',
                                                       'autocomplete': 'off'}))
    subject = forms.CharField(max_length=255, widget=forms.TextInput(attrs=({'class': 'form-control', })))
    body = forms.CharField(widget=forms.Textarea(attrs=({'class': 'form-control'})))
    group = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                          'readonly': 'readonly'}))
    message = forms.CharField(required=False, widget=forms.HiddenInput())

    def clean_to(self):
        if self.cleaned_data['to']:
            try:
                return User.objects.get(username=self.cleaned_data['to'])
            except:
                raise forms.ValidationError("User not found.")
        return None

    def clean_message(self):
        if self.cleaned_data['message']:
            try:
                return UserMessages.objects.get(id=self.cleaned_data['message'])
            except:
                raise forms.ValidationError("Message does not exist.")
        return None

    def clean_group(self):
        if self.cleaned_data['group']:
            try:
                return CompetitiveGroups.objects.get(name=self.cleaned_data['group'])
            except:
                raise forms.ValidationError("Group does not exist.")
        return None
