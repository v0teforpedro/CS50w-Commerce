from django.urls import path

from . import views

app_name = 'auctions'

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="add"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:pk>", views.category_listing, name="cat_list"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("lot/<int:pk>", views.listing_page, name="lot_page"),
]
