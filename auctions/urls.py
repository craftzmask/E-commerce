from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('watchlist/add/<int:listing_id>', views.add_watchlist, name='add_watchlist'),
    path('watchlist/remove/<int:listing_id>', views.remove_watchlist, name='remove_watchlist'),
    path('listings/create', views.create_listing, name='create_listing'),
    path('listings/<int:listing_id>', views.view_listing, name='view_listing')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)