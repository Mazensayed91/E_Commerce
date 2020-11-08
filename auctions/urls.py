from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:user_id>/create_listing", views.create_listing, name="create_listing"),
    path("<int:listing_id>/<int:user_id>/listing", views.listing, name="listing"),
    path("<int:user_id>/watch_list", views.watch_list, name="watch_list"),
    path("categories", views.categories, name="categories"),
    path("category", views.category, name="category"),

]
