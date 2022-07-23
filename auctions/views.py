from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

def index(request):
    return render(request, "auctions/index.html", {
        'listings': Listing.objects.all()
    })


# Users
def login_view(request):
    if request.method == "POST":
        
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# Listings
@login_required
def create_listing(request):
    if request.method == 'POST':
        
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()       
            messages.success(request, f'{listing.title} added to active listings')
            return redirect('index')
        else:
            return render(request, 'auctions/create_listing.html', {
                'form': form
            })
    
    return render(request, 'auctions/create_listing.html', {
        'form': ListingForm()
    })
    
    
def view_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user_listing = None
    user_watchlist = None
    highest_bid = None
    
    if request.user.is_authenticated:
        user_listing = request.user.listings.filter(id=listing_id).first()
        user_watchlist = request.user.watchlist.filter(listing=listing).first()
    
    if user_watchlist:
        user_watchlist = user_watchlist.listing
    
    if not listing.is_active:
        highest_bid = listing.bids.latest('created_at')
        if highest_bid.owner.username == request.user.username:
            messages.info(request, 'You are the winner of this auction')
        
    return render(request, 'auctions/view_listing.html', {
        'listing': Listing.objects.get(pk=listing_id),
        'user_watchlist': user_watchlist,
        'user_listing': user_listing,
        'place_bid_form': PlaceBidForm(),
        'comment_form': AddCommentForm()
    })
    

@login_required    
def close_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.is_active = False
    listing.save()
    return redirect('view_listing', listing_id=listing_id)


# Watchlist
@login_required
def add_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    owner = request.user
    watchlist = Watchlist.objects.filter(owner=owner, listing=listing)
    if not watchlist.exists():
        watchlist = Watchlist(owner=owner, listing=listing)
        watchlist.save()
    
    return redirect('view_listing', listing_id=listing_id)


@login_required
def view_watchlist(request):
    watchlist = request.user.watchlist.all()
    listings = [w.listing for w in watchlist]
    return render(request, 'auctions/view_watchlist.html', {
        'listings': listings
    })


@login_required
def remove_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    request.user.watchlist.filter(listing=listing).delete()
    
    return redirect('view_listing', listing_id=listing_id)


@login_required
def place_bid(request, listing_id):
    if request.method == 'POST':
        form = PlaceBidForm(request.POST)
        if form.is_valid():
            bid_value = form.cleaned_data['value']
            listing = Listing.objects.get(pk=listing_id)

            # Find any bid that is greater than the placed bid
            bids = listing.bids.filter(value__gte=bid_value)
            if bids or bid_value < listing.starting_bid:
                messages.error(request, f'The placed bid must be greater than current bid')
            else:
                Bid(value=bid_value, owner=request.user, listing=listing).save()
                listing.starting_bid = bid_value
                listing.save()
                messages.success(request, f'Placed bid successfully')
                
        return redirect('view_listing', listing_id=listing_id)
            
    
@login_required
def add_comment(request, listing_id):
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            listing = Listing.objects.get(pk=listing_id)
            Comment(content=content, owner=request.user, listing=listing).save()
        else:
            return render(request, 'auctions/view_listing.html', {
                form: AddCommentForm()
            })
            
        return redirect('view_listing', listing_id=listing_id)
        