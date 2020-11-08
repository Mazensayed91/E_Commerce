from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *


def index(request):
    return render(request, "auctions/index.html",{
        "listings" : Listing.objects.all()
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
        
@login_required(login_url='/login')
def create_listing(request,user_id):
    if request.method == 'POST':
        user = User.objects.get(pk = user_id)
        start_bid = request.POST["start_bid"]
        title = request.POST["title"]
        desc = request.POST["desc"]
        url = request.POST["url"]
        cat = request.POST["cat"]
        listing = Listing(title = title,image_url = url,user_id = user,describtion = desc)
        listing.save()
        category= Category(listing_id = listing,category=cat)
        bids = Bid(listing_id = listing,max_bid=start_bid,starting_bid=start_bid,user_id = user)
        category.save()
        bids.save()
        return render(request,"auctions/index.html",{
            "listings":Listing.objects.all()
            })
    else:
        return render(request,"auctions/create_listing.html")


def listing(request,listing_id,user_id):

    listing = Listing.objects.get(pk = listing_id)
    user = User.objects.get(pk = user_id)

    if request.method == 'POST':
        if 'remove' in request.POST:
            remove = request.POST['remove']
            if remove == 'no':
                if WatchListItem.objects.filter(listing_id = listing_id).exists():
                    WatchListItem.objects.get(listing_id = listing_id).users.add(user)
                else:
                    watchlistitem = WatchListItem(listing_id = listing_id)
                    watchlistitem.save()
                    watchlistitem.users.add(user)
            elif remove == 'yes':
                watchlistitem = WatchListItem.objects.get(listing_id = listing_id)
                watchlistitem.users.remove(user)
                user.watchlistitems.remove(watchlistitem)

        elif 'bid' in request.POST:
            Bid.objects.filter(listing_id = listing_id).update(max_bid=request.POST['bid'])
            Bid.objects.filter(listing_id = listing_id).update(user_id=user_id)

        elif 'cancel' in request.POST:
            winner = Bid.objects.get(listing_id = listing_id).user_id
            Listing.objects.filter(pk = listing_id).update(active = False)
            return HttpResponseRedirect(reverse("index"))

        elif 'comment' in request.POST:
            text_area = request.POST['comment']
            comment= Comment(listing_id = listing,comment=text_area)
            comment.save()


    return render(request,"auctions/listing.html",{
            "listing" : listing,
            "user" : user
        }) 

@login_required(login_url='/login')
def watch_list(request,user_id):
    user = User.objects.get(pk = user_id)
    return render(request,"auctions/watch_list.html",{
        "user" : user
        })

@login_required(login_url='/login')
def categories(request):
    if request.method == 'POST':
        return render(request,'auctions/category.html',{
            'cat':Category.objects.filter(category = request.POST['cat'])
            })

    unique_categories = Category.objects.values('category').distinct()

    return render(request,"auctions/categories.html",{
        "categories" : unique_categories
        })

@login_required(login_url='/login')
def category(request):
    return render(request,'auctions/category.html')