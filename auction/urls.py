from django.urls import path

from .views import (
    auction_gallery,
    item_details,
    create_auction,
    my_auctions,
    place_bid,
    update_bid
)


from .views import (
    dashboard,
    created_completed_auction_day_chart,
    created_completed_auction_hour_chart,
    created_completed_auction_minute_chart,
    total_auction_value_day_chart,
    total_auction_value_hour_chart,
    total_auction_value_minute_chart
)


app_name = 'auction'

urlpatterns = [
    path('auction-gallery/', auction_gallery, name='auction-gallery'),
    path('item/<str:slug>/', item_details, name='item-detail'),
    path('create-auction/', create_auction, name='create-auction'),
    path('my-auctions/', my_auctions, name='my-auctions'),
    path('item/<str:slug>/place-bid/', place_bid, name='place-bid'),
    path('item/<str:slug>/<str:hashed_id>/update-bid/',
        update_bid,
        name='update-bid'
    ),



    path('', dashboard, name='dashboard'),

    path('chart/created-completed-auctions-number-per-day/',
         created_completed_auction_day_chart,
         name='created-completed-auctions-number-per-day'),

    path('chart/created-completed-auctions-number-per-hour/',
         created_completed_auction_hour_chart,
         name='created-completed-auctions-number-per-hour'),

    path('chart/created-completed-auctions-number-per-minute/',
         created_completed_auction_minute_chart,
         name='created-completed-auctions-number-per-minute/'),

    path('chart/total-auction-value-per-day/',
         total_auction_value_day_chart,
         name='total-auction-value-per-day/'),

    path('chart/total-auction-value-per-hour/',
         total_auction_value_hour_chart,
         name='total-auction-value-per-hour/'),

    path('chart/total-auction-value-per-minute/',
         total_auction_value_minute_chart,
         name='total-auction-value-per-minute/'),
]




