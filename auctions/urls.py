from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.create, name = "create"),
    path("product/<str:item_no>",views.product, name = "product"),
    path("watchlist/toggle/<str:item_no>/", views.toggle_watchlist, name="toggle_watchlist"),
    path("watchlist/", views.watchlist_page, name="watchlist"),
    path("product/<str:item_no>/bid", views.place_bid, name="place_bid"),
    path("product/<str:item_no>/closeauction", views.close_auction, name ="close_auction"),
    path("categories",views.categories, name="categories" ),
    path("categories/<str:name>",views.category, name= "ctgpage")
]
