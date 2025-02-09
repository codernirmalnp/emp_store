from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import TalentProfile, ParentalConsent
from .models import Subscription
from .models import BlogPost

class TalentRegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=100)
    age = forms.IntegerField()
    portfolio = forms.URLField(required=False)
    bio = forms.CharField(widget=forms.Textarea)
    skills = forms.CharField(max_length=200)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'full_name', 'age', 'portfolio', 'bio', 'skills']

class ParentalConsentForm(forms.ModelForm):
    class Meta:
        model = ParentalConsent
        fields = ['parent_name', 'parent_email']



class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['plan']



class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content']