from django.forms import ModelForm
from django import forms
from .models import Twitterapi

class Twitter_Api(forms.Form):
       Hashtags = forms.CharField(max_length=100, label='Hashtag')
       since_Date = forms.CharField(max_length=15, label='Since_Date',required=False)
       until_Date = forms.CharField(max_length=15, label='Until_Date',required=False)
       consumer_key = forms.CharField(max_length=100, label='Consumer_key')
       consumer_secret = forms.CharField(max_length=100,label='Consumer_secret')
       access_token = forms.CharField(max_length=100,label='Access_token')
       access_token_secret = forms.CharField(max_length=100,label='Access_token_secret ')


class Twitter_Api_Hashtags(forms.Form):
       Hashtags = forms.CharField(max_length=100, label='Hashtag')
       since_Date = forms.CharField(max_length=15, label='YYYY-MM-DD')
       until_Date = forms.CharField(max_length=15, label='YYYY-MM-DD')