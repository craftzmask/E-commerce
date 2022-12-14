from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('watchlist/view', views.view_watchlist, name='view_watchlist'),
    path('watchlist/add/<int:listing_id>', views.add_watchlist, name='add_watchlist'),
    path('watchlist/remove/<int:listing_id>', views.remove_watchlist, name='remove_watchlist'),
    path('listings/create', views.create_listing, name='create_listing'),
    path('listings/view/<int:listing_id>', views.view_listing, name='view_listing'),
    path('listings/close/<int:listing_id>', views.close_listing, name='close_listing'),
    path('listings/place-bid/<int:listing_id>', views.place_bid, name='place_bid'),
    path('listings/watchlist/remove/<int:listing_id>', views.remove_watchlist_from_listing, name='remove_watchlist_from_listing'),
    path('categories/view-listings/<int:category_id>', views.view_listings_category, name='view_listings_category'),
    path('comments/add/<int:listing_id>', views.add_comment, name='add_comment')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)