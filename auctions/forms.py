from django.forms import ModelForm
from .models import Bid, Listing, Comment

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'photo']


class PlaceBidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['value']
        

class AddCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']