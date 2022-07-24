from django import forms
from django.forms import ModelForm, Select
from .models import Bid, Category, Listing, Comment, User


class LoginForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username']


class RegisterForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirmation = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email']


class ListingForm(ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'photo', 'category']
 
   
class PlaceBidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['value']
        

class AddCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']