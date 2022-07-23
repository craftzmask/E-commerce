from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages

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
    user_watchlist = request.user.watchlist.filter(listing=listing).first()
    
    if user_watchlist:
        user_listing = user_watchlist.listing
          
    return render(request, 'auctions/view_listing.html', {
        'listing': Listing.objects.get(pk=listing_id),
        'user_listing': user_listing,
        'form': PlaceBidForm()
    })
    

# Watchlist
def add_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    owner = request.user
    watchlist = Watchlist.objects.filter(owner=owner, listing=listing)
    if not watchlist.exists():
        watchlist = Watchlist(owner=owner, listing=listing)
        watchlist.save()
    
    return redirect('view_listing', listing_id=listing_id)


def remove_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    request.user.watchlist.filter(listing=listing).delete()
    
    return redirect('view_listing', listing_id=listing_id) 