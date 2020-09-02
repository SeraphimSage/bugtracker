from django import forms
from bugtracker_app.models import MyDev, Bug


class AddBugForm(forms.ModelForm):
    class Meta:
        model = Bug
        fields = ['title', 'description']


class InProgressBugForm(forms.ModelForm):
    class Meta:
        model = Bug
        fields = ['assigned_to_dev']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput)
