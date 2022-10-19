from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=100)


class Listing(models.Model):
    product = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='auctions/img/', default='default_image.png')
    description = models.TextField(max_length=255, null=True, blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField(max_length=255)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Bid(models.Model):
    amount = models.PositiveIntegerField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid_by = models.ForeignKey(User, on_delete=models.CASCADE)
