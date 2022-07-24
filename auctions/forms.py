from django import forms
from django.forms import ModelForm, Select
from .models import Bid, Category, Listing, Comment, User


class LoginForm(forms.Form):
    template_name = 'auctions/form_snippet.html'
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirmation = forms.CharField(widget=forms.PasswordInput())


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