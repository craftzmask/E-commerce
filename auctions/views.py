from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect, render


from .models import *
from .forms import *

def index(request):
    return render(request, 'auctions/index.html', {
        'listings': Listing.objects.all(),
        'categories': Category.objects.all()
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
            return render(request, 'auctions/users/login.html', {
                'form': form
            })
    else:
        return render(request, 'auctions/users/login.html', {
            'form': LoginForm()
        })


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
                'form': form
            })
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
 
 
def view_listing(request, listing_id, place_bid_form=PlaceBidForm(), comment_form=AddCommentForm()):
    listing = Listing.objects.get(pk=listing_id)
    user = request.user

    if user.is_authenticated:
        if not listing.is_active and listing.bids.last().owner == user:
            messages.info(request, 'You are the winner of this auction')
            
        return render(request, 'auctions/listings/view.html', {
            'listing': listing,
            'user_watchlist_exits': user.watchlist.filter(listing=listing).exists(),
            'user_listing_contains': user.listings.contains(listing),
            'form': place_bid_form,
            'form_1': comment_form
        })

    return render(request, 'auctions/listings/view.html', {
        'listing': listing,
        'form': place_bid_form,
        'form_1': comment_form
    })

    
def view_listings_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    listings = Listing.objects.filter(category=category)
    return render(request, 'auctions/categories/view_listings.html', {
        'category': category,
        'listings': listings,
        'categories': Category.objects.all()
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
    Watchlist.objects.get_or_create(owner=owner, listing=listing)
    return redirect('view_listing', listing_id=listing_id)


def view_watchlist(request):
    listings = []
    if request.user.is_authenticated:
        watchlist = request.user.watchlist.all()
        listings = [w.listing for w in watchlist]
        
    return render(request, 'auctions/watchlist/view.html', {
        'listings': listings
    })

@login_required
def remove_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    request.user.watchlist.filter(listing=listing).delete()
    return redirect('view_watchlist')


@login_required
def remove_watchlist_from_listing(request, listing_id):
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
        else:
            return redirect('view_listing', listing_id=listing_id, place_bid_form=form)
            
    
@login_required
def add_comment(request, listing_id):
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            listing = Listing.objects.get(pk=listing_id)
            Comment(content=content, owner=request.user, listing=listing).save()
        else:
            return redirect('view_listing', listing_id=listing_id, comment_form=form)
            
        return redirect('view_listing', listing_id=listing_id)
        