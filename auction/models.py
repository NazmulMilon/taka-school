import datetime

from django.db import models
from django.utils.text import slugify

from authentication.models import User
from authentication.utils import random_hex_code


class AuditTrail(models.Model):
    hashed_id = models.CharField(null=True, blank=True, max_length=16, unique=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            # For each object a new unique hashed id will be generated.
            self.hashed_id = random_hex_code(length=16)

        super().save(*args, **kwargs)


class Product(AuditTrail):
    """
    Auction Product model: detail info of a auction item.
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=500, unique=True, null=True, blank=True)
    description = models.TextField()
    photo = models.ImageField(upload_to='product/%Y/%m/%d/',
                              default='product/product.png')
    min_bid_price = models.FloatField()
    auction_end_date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_user')

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.name} :: {self.user.username}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('auction:item-detail', kwargs={'slug': self.slug})

    def get_is_auction_time_ended(self):
        is_auction_date_ended = False
        # Converting the current time to timezone offset aware and compare
        if self.auction_end_date < datetime.datetime.now(
                self.auction_end_date.tzinfo):
            is_auction_date_ended = True

        return is_auction_date_ended

    def get_max_bid(self):
        max_bid = None
        bids = Bid.objects.filter(product=self)
        if bids.count() > 0:
            # getting maximum bid
            max_bid = bids.order_by('-price').first()

        return max_bid

    def get_total_bid(self):
        bid = Bid.objects.filter(product=self).count()
        return bid if bid else 0

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(f"{self.name}_{random_hex_code(16)}",
                                allow_unicode=True)
        super().save(*args, **kwargs)


class Bid(AuditTrail):
    """
    Bid for a auction item
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='bid_product'
    )
    bidder = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bid_bidder'
    )
    price = models.FloatField()

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.product.name}: {self.bidder.username}: {self.price}"
