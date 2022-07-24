from django import forms
from django.forms import ModelForm, Select
from .models import Bid, Category, Listing, Comment

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