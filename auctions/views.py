from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import CategoriesForm, ListingsForm, BidsForm, CommentsForm
from .models import User, Category, Listing, Bid,Watchlist,Comment
from django.contrib import messages




def index(request):
    listings = Listing.objects.all()
    watchlist_items = set()

    for listing in listings:
        # get the first bid for this listing
        bid = Bid.objects.filter(listing=listing).order_by('-cur_bid').first()

        if bid:
            listing.cur_bid = bid.cur_bid or bid.start_bid
        else:
            listing.cur_bid = None   # no bids yet

    if request.user.is_authenticated:
        user_watchlist = Watchlist.objects.filter(user=request.user)
        watchlist_items = set(w.listing.item_no for w in user_watchlist)

    return render(request, "auctions/index.html", {
        "listings": listings,
        "watchlist_items": watchlist_items
    })





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


def create(request):
    if request.method == 'POST':
        form1 = CategoriesForm(request.POST)
        form2 = ListingsForm(request.POST)
        form3 = BidsForm(request.POST)

        if form1.is_valid() and form2.is_valid() and form3.is_valid():
            # Get or create category
            category_name = form1.cleaned_data['name']
            category, _ = Category.objects.get_or_create(name=category_name)

            # Create listing
            listing = form2.save(commit=False)
            listing.user = request.user
            listing.category = category
            listing.save()

            # Create bid
            bid = form3.save(commit=False)
            bid.listing = listing
            bid.bidder = request.user
            bid.save()

            return redirect('index')
    else:
        form1 = CategoriesForm()
        form2 = ListingsForm()
        form3 = BidsForm()

    return render(request, 'auctions/create.html', {
        'form1': form1,
        'form2': form2,
        'form3': form3
    })



def product(request, item_no):
    # Get listing directly by its item_no
    listing = get_object_or_404(Listing, item_no=item_no)

    # Get the latest/highest bid for this listing
    bid = Bid.objects.filter(listing=listing).order_by('-cur_bid').first()
    comments = Comment.objects.filter(listing=listing)
    in_watchlist = False
    form = None
    
    
    if request.user.is_authenticated:
        in_watchlist = Watchlist.objects.filter(user=request.user, listing=listing).exists()
        if request.method == 'POST':
            form = CommentsForm(request.POST)
            if form.is_valid():
                com = form.save(commit = False)
                com.commenter = request.user
                com.listing = listing
                com.save()
                return redirect('product',item_no=item_no)
        else:
            form = CommentsForm()

        

    return render(request, "auctions/product.html", {
        "listing": listing,
        "starting_bid": bid.start_bid if bid else "N/A",
        "current_bid": bid.cur_bid if bid and bid.cur_bid else bid.start_bid if bid else "N/A",
        "in_watchlist": in_watchlist,
        "form" : form,
        "comments" : comments
    })




def toggle_watchlist(request, item_no):
    if request.method == "POST" and request.user.is_authenticated:
        listing = get_object_or_404(Listing, item_no=item_no)

        watchlist_item = Watchlist.objects.filter(user=request.user, listing=listing).first()
        if watchlist_item:
            watchlist_item.delete()
        else:
            Watchlist.objects.create(user=request.user, listing=listing)
    
    return redirect(request.META.get('HTTP_REFERER', 'index'))




def watchlist_page(request):
    if not request.user.is_authenticated:
        return redirect("login")
    user_watchlist = Watchlist.objects.filter(user=request.user)
    listings = [item.listing for item in user_watchlist]
    for listing in listings:
        bid = Bid.objects.filter(listing =listing).first()
        listing.start_bid=bid.start_bid
        listing.cur_bid = bid.cur_bid 
    
    
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })



def place_bid(request, item_no):
    listing = get_object_or_404(Listing, item_no=item_no)
    bid = Bid.objects.filter(listing =listing).first()

    # Safeguard in case no bid exists
    if bid is None:
        messages.error(request, "This item has no bids yet.")
        return redirect("index")

    if request.method == "POST" and request.user.is_authenticated:
        try:
            new_bid = int(request.POST.get("bid"))
        except (TypeError, ValueError):
            return render(request, "auctions/product.html", {
                "listing": listing,
                "bid": bid,
                "error_message": "Please enter a valid number.",
            })
        
        if new_bid < bid.start_bid:
            messages.error(request, "bid must be atleast the starting bid.")
            return redirect("product", item_no=item_no)
        if bid.cur_bid is None:
            bid.cur_bid=0
        if new_bid <= bid.cur_bid:
            messages.error(request, "bid must be greater than the current highest bid.")
            return redirect("product", item_no=item_no)

        # ✅ All checks passed – update the bid
        bid.cur_bid = new_bid
        bid.bidder = request.user
        bid.save()

        # Optional: You could store who placed the bid, timestamp, etc.

        messages.success(request, "Bid placed successfully!")
        return redirect("product", item_no=item_no)

    # GET request or invalid user
    return render(request, "auctions/product.html", {
        "listing": listing,
        "bid": bid
    })

def close_auction(request, item_no):
    if request.method == "POST" and request.user.is_authenticated:
        listing = get_object_or_404(Listing, item_no=item_no)

        # Ensure only creator can close the auction
        if request.user != listing.user:
            messages.error(request, "You are not allowed to close this auction.")
            return redirect("product", item_no=item_no)

        # Get highest bid
        highest_bid = Bid.objects.filter(listing=listing).order_by('-cur_bid').first()

        # Mark auction as closed
        listing.active = False
        if highest_bid:
            listing.winner = highest_bid.bidder

        listing.save()

        
        return redirect("product", item_no=item_no)

    return redirect("product")

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html",{
        "categories": categories
    })

            
def category(request,name):
    cat = get_object_or_404(Category, name=name)
    listings = Listing.objects.filter(category =cat, active=True)
    for listing in listings:
        # get the first bid for this listing
        bid = Bid.objects.filter(listing=listing).order_by('-cur_bid').first()

        if bid:
            listing.cur_bid = bid.cur_bid or bid.start_bid
        else:
            listing.cur_bid = None
    return render(request,"auctions/category_listings.html",{
        "listings" :listings 
    }) 