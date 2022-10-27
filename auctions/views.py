from django.contrib.auth import authenticate, login, logout, get_user
from django.db import IntegrityError
from django.shortcuts import render, redirect

from .forms import ListingCreateForm, BidCreateForm
from .models import User, Listing, Category


def index(request):
    products = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", context={'data': products, 'title': 'Active Listings'})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("auctions:index")
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return redirect("auctions:index")


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
        return redirect("auctions:index")
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    if request.method == 'GET':
        form = ListingCreateForm()
    else:
        form = ListingCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.created_by = request.user
            form.save()
            return redirect('auctions:index')

    return render(
        request,
        'auctions/create_listing.html',
        context={'title': 'Create Listing', 'form': form}
    )


def categories(request):
    data = Category.objects.all()
    return render(request, 'auctions/categories.html', context={'title': 'List of Categories', 'data': data})


def category_listing(request, pk):
    data = Listing.objects.filter(categories=pk)
    category = Category.objects.get(pk=pk)
    name = category.name
    return render(request, 'auctions/index.html', context={'title': name, 'data': data})


def listing_page(request, pk):
    data = Listing.objects.get(pk=pk)
    title = f'Lot №{data.id} ({data.name})'
    form = BidCreateForm()

    if request.method == 'POST':
        form = BidCreateForm(request.POST)
        form.instance.listing = data
        if form.is_valid():
            form.instance.bid_by = request.user
            form.save()
            return redirect('auctions:lot_page', data.pk)

    return render(request, 'auctions/listing_page.html', context={'data': data, 'title': title, 'form': form})
