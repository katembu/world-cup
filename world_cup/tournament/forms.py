from django import forms
from django.contrib.auth.models import User
from tournament.models import CompetitiveGroups, Brackets


class CompetitiveGroupForm(forms.ModelForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs=({'class': 'form-control', })))
    password = forms.CharField(required=False, widget=forms.TextInput(attrs=({'class': 'form-control', })),
                               label='Password (Optional)')
    brackets = forms.ModelChoiceField(queryset=Brackets.objects.all(),
                                      widget=forms.Select(attrs=({'class': 'form-control', })))

    class Meta:
        model = CompetitiveGroups
        fields = ['name', 'brackets', 'password']


class BracketSelectForm(forms.Form):
    brackets = forms.ModelChoiceField(queryset=Brackets.objects.all(),
                                      widget=forms.Select(attrs=({'class': 'form-control', })))


class GroupLoginForm(forms.Form):
    password = forms.CharField(max_length=255, widget=forms.TextInput(attrs=({'class': 'form-control', })))
