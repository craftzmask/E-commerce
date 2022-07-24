from django import forms
from django.forms import ModelForm
from .models import Bid, Category, Listing, Comment


class LoginForm(forms.Form):
    template_name = 'auctions/snippets/form.html'
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(forms.Form):
    template_name = 'auctions/snippets/form.html'
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirmation = forms.CharField(widget=forms.PasswordInput())


class ListingForm(ModelForm):
    template_name = 'auctions/snippets/form.html'
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'photo', 'category']
 
   
class PlaceBidForm(ModelForm):
    template_name = 'auctions/snippets/form.html'
    class Meta:
        model = Bid
        fields = ['value']
        

class AddCommentForm(ModelForm):
    template_name = 'auctions/snippets/form.html'
    content = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Comment
        fields = ['content']