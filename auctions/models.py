from django.contrib.auth.models import AbstractUser
from django.db import models


# Custom User Model
class User(AbstractUser):
    pass


# Category Model
class Category(models.Model):
    name = models.CharField(max_length=50, unique=False)

    def __str__(self):
        return self.name


# Listing Model
class Listing(models.Model):
    # Unique item number for each listing (auction ID)
    item_no = models.CharField(max_length=15, unique=True)

    title = models.CharField(max_length=100)
    desc = models.TextField()
    img = models.URLField(max_length=500, blank=True, null=True)

    # Relationships
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="listings")
    winner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="won_auctions")

    # Status
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.item_no})"


# Bid Model
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    start_bid = models.DecimalField(max_digits=10, decimal_places=2)
    cur_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bidder = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.listing.title} — ₹{self.cur_bid or self.start_bid}"


# Comment Model
class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    commenter = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return self.comment[:30]


# Watchlist Model
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlisted_by")

    def __str__(self):
        return f"{self.user.username} → {self.listing.title}"
