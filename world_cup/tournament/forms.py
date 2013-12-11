from django.forms import ModelForm
from django import forms
from tournament.models import CompetitiveGroups, Brackets


class CompetitiveGroupForm(ModelForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs=({'class': 'form-control', })))
    brackets = forms.ModelChoiceField(queryset=Brackets.objects.all(),
                                      widget=forms.Select(attrs=({'class': 'form-control', })))

    class Meta:
        model = CompetitiveGroups
        fields = ['name', 'brackets']
