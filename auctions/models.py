from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=19, decimal_places=2)
    photo = models.ImageField(
        upload_to='images/listing-photos',
        blank=True, null=True
    )
    created_at = models.TimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')


class Bid(models.Model):
    value = models.DecimalField(max_digits=19, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')


class Comment(models.Model):
    content = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')


class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='categories')