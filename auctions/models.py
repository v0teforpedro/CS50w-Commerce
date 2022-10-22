from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Max


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        db_table = 'categories'

    def __str__(self):
        return self.name


class Listing(models.Model):
    name = models.CharField(max_length=100)
    start_price = models.PositiveIntegerField()
    # curr_price = models.PositiveIntegerField(blank=True)
    image = models.ImageField(upload_to='auctions/img/', default='default_image.png')
    description = models.TextField(max_length=255, null=True, blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'listing'
        verbose_name_plural = 'listings'
        db_table = 'listings'

    def __str__(self):
        return f'Lot "{self.name}" by {self.created_by.username}'

    # def save(self, *args, **kwargs):
    #     if not self.curr_price:
    #         self.curr_price = self.start_price
    #     super().save(*args, **kwargs)

    @property
    def bid_count(self):
        return self.bids.count()

    @property
    def current_price(self):
        return self.bids.aggregate(Max('amount')).get('amount__max')


class Comment(models.Model):
    text = models.TextField(max_length=255)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
        db_table = 'comments'


class Bid(models.Model):
    amount = models.PositiveIntegerField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    bid_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'bid'
        verbose_name_plural = 'bids'
        db_table = 'bids'

    def __str__(self):
        return f'Bid by {self.bid_by.username} on {self.listing.name}'

    def clean(self):
        if self.amount <= self.listing.current_price:
            raise ValidationError('The bid must be greater than current price')

    # def save(self, *args, **kwargs):
    #     if self.amount > self.listing.curr_price:
    #         self.listing.curr_price = self.amount
    #         self.listing.save()
    #     super().save(*args, **kwargs)
