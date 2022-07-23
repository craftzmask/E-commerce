from dataclasses import fields
from django.forms import ModelForm
from .models import Bid, Listing

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'photo']


class PlaceBidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['value']