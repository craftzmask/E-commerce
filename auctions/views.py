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
    return render(request, 'auctions/index.html', {
        'listings': Listing.objects.all()
    })


# Users
def login_view(request):
    if request.method == 'POST':
        
        form = LoginForm(request.POST)
        if form.is_valid():
            # Authenticate user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            # Ensure user exists
            if user is not None:
                login(request, user)
                messages.success(request, 'Welcome back! You successfully logged in')
                return redirect('index')
            else:
                messages.error(request, 'Invalid username and/or password')
                return redirect('login')
    else:
        return render(request, 'auctions/users/login.html', {'form': LoginForm()})


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


def register(request):
    if request.method == 'POST':
        
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            # Ensure password matches confirmation
            password = form.cleaned_data['password']
            confirmation = form.cleaned_data['confirmation']
            if password != confirmation:
                messages.error(request, 'Passwords must match')
                return redirect('register')

            # Attempt to create new user
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except IntegrityError:
                messages.error(request, 'Username already taken')
                return redirect('register')
            
            login(request, user)
            return redirect('index')
    else:
        return render(request, 'auctions/users/register.html', {
            'form': RegisterForm()
        })


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
            return render(request, 'auctions/listings/create.html', {
                'form': form
            })
    
    return render(request, 'auctions/listings/create.html', {
        'form': ListingForm()
    })
    

def view_categories(request):
    return render(request, 'auctions/categories/view.html', {
        'categories': Category.objects.all()
    })
    
def view_listings_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    listings = Listing.objects.filter(category=category)
    return render(request, 'auctions/categories/view_listings.html', {
        'category': category,
        'listings': listings
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
        
    return render(request, 'auctions/listings/view.html', {
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
    return render(request, 'auctions/watchlist/view.html', {
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
        