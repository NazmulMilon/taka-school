import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from auction.models import Product, Bid

''''''
import datetime
from django.contrib.auth.decorators import login_required
from django.db.models.functions import (
    ExtractDay,
    ExtractHour,
    ExtractMinute
)
from django.http import JsonResponse
from django.shortcuts import render

from auction.models import Product, Bid
from authentication.utils import (
    days,
    colorPrimary,
    colorPrimaryBorder,
    colorDanger,
    colorDangerBorder,
    get_day_dict,
    hours,
    get_hour_dict,
    minutes,
    get_minute_dict
)


@login_required(login_url='authentication:user-login')
def auction_gallery(request):
    
    # List of all the auction items
    products = Product.objects.filter(is_active=True).order_by('-created_at')
    context = {'products': products, 'active': 'auction_gallery'}
    return render(request, 'auction_gallery.html', context)


@login_required(login_url='authentication:user-login')
def item_details(request, slug):

    #Auction item detail info
    selected_product = get_object_or_404(Product, slug=slug)
    selected_products_bids = Bid.objects.filter(
        product=selected_product
    ).order_by('-price')

    context = {
        'selected_product': selected_product,
        'bids': selected_products_bids,
    }
    return render(request, 'detail.html', context)


@login_required(login_url='authentication:user-login')
def create_auction(request):

    # Create a new auction for a product.
    if request.method == "POST":
        product_name = request.POST.get('product_name')
        product_description = request.POST.get('product_description')
        product_photo = request.FILES.get('product_photo')
        min_bid_price = request.POST.get('min_bid_price')
        auction_end_date = request.POST.get('auction_end_date')
        auction_end_time = request.POST.get('auction_end_time')

        context = {
            'product_name': product_name,
            'product_description': product_description,
            'min_bid_price': min_bid_price,
            'auction_end_date': auction_end_date,
            'auction_end_time': auction_end_time
        }
        create_auction_template = 'create_auction.html'

        if product_name.strip() == '':
            messages.error(request, 'Please give a product name!')
            return render(request, create_auction_template, context)
        if product_description.strip() == '':
            messages.error(
                request,
                'Please write some description about the product!'
            )
            return render(request, create_auction_template, context)
        if product_photo == '':
            messages.error(request, 'Please add a photo of the product!')
            return render(request, create_auction_template, context)
        if min_bid_price == '':
            messages.error(request, 'Please give minimum bid price!')
            return render(request, create_auction_template, context)
        if auction_end_date == '':
            messages.error(request, 'Please give auction end date!')
            return render(request, create_auction_template, context)
        if auction_end_time == '':
            messages.error(request, 'Please give auction end time!')
            return render(request, create_auction_template, context)
        else:
            try:
                # format the auction_end_date with date time
                auction_end_date_time = datetime.datetime.strptime(
                    f"{auction_end_date} {auction_end_time}",
                    "%Y-%m-%d %H:%M"
                )
                timezone_aware_auction_end_datetime = timezone.make_aware(
                    auction_end_date_time,
                    timezone.get_current_timezone()
                )
                # Create a new product object
                Product.objects.create(
                    name=product_name,
                    description=product_description,
                    photo=product_photo,
                    min_bid_price=min_bid_price,
                    auction_end_date=timezone_aware_auction_end_datetime,
                    user=request.user,
                )
                messages.success(
                    request,
                    "New auction Item is added to auction gallery."
                )
                return redirect('auction:dashboard')
            except Exception as e:
                # print(e)
                messages.error(request, f"Error: {e}")
                redirect('auction:create-auction')

    return render(request, 'create_auction.html')


@login_required(login_url='authentication:user-login')
def my_auctions(request):

    #List of the auction of single user.

    products = Product.objects.filter(user=request.user, is_active=True)
    context = {
        'products': products,
        'active': 'my_auctions'
    }
    return render(request, 'auction_gallery.html', context)


@login_required(login_url='authentication:user-login')
def place_bid(request, slug):

    # Place bid for selected auction product/item.
    product = get_object_or_404(Product, slug=slug)
    if request.method == "POST":
        bid_price = request.POST.get('bid_price')

        # Validating bid value
        if not isinstance(int(bid_price), int):
            messages.error(request, 'Please place correct bid.')
            return redirect(product)
        try:
            Bid.objects.create(
                product=product,
                bidder=request.user,
                price=bid_price
            )
            messages.success(request, 'You have placed the bid successfully')
            return redirect(product)
        except Exception as e:
            # print(e)
            messages.error(request, f'Error: {e}')
            return redirect(product)
    return redirect(product)


@login_required(login_url='authentication:user-login')
def update_bid(request, slug, hashed_id):

    # Update the bid
    product = get_object_or_404(Product, slug=slug)
    bid = get_object_or_404(Bid, hashed_id=hashed_id)

    if request.method == "POST":
        updated_bid_price = request.POST.get("updated_bid_price")
        try:
            bid.price = updated_bid_price
            bid.save()
            messages.success(
                request,
                f"You have update the bid price to {updated_bid_price}"
            )
            return redirect('auction:item-detail', slug=slug)
        except Exception as e:
            # print(e)
            messages.error(request, f'Error: {e}')
            return redirect(product)

    return redirect(product)

'''' '''
''''''
''''''

@login_required(login_url='authentication:user-login')
def dashboard(request):
    """
    User and Admin Dashboard
    :param request:
    :type request:
    :return:
    :rtype:
    """
    products = Product.objects.filter(is_active=True).order_by('-created_at')
    total_auctions = products.count()
    running_auctions_count = 0
    running_auctions_total_value = 0
    if products.count() > 0:
        # ***Running Auctions
        running_auctions = products.filter(
            auction_end_date__gt=datetime.datetime.now(
                products.first().auction_end_date.tzinfo
            )
        )
        running_auctions_count = running_auctions.count()

        # ***Running Auction's total value
        for product in running_auctions:
            max_bid_price_for_product = Bid.objects.filter(
                product=product
            ).order_by('-price').first()  # Max bid

            if max_bid_price_for_product is None:  # If no bid for the auction
                running_auctions_total_value += product.min_bid_price
            else:
                running_auctions_total_value += max_bid_price_for_product.price

    context = {
        'products': products,
        'active': 'dashboard',
        'running_auctions_count': running_auctions_count,
        'total_auctions': total_auctions,
        'running_auctions_total_value': int(running_auctions_total_value),
    }

    return render(request, 'dashboard.html', context)


@login_required(login_url='authentication:user-login')
def created_completed_auction_day_chart(request):
    """
    Chart for number of created and completed auctions in each day
    :param request:
    :type request:
    :return:
    :rtype:
    """
    # NUMBER OF AUCTION CREATED DATA GENERATION FOR DAY CHART
    list_of_product_created_date_dict = Product.objects.filter(
        created_at__month=datetime.datetime.today().month).annotate(
        day=ExtractDay('created_at')).values('day').order_by('created_at')
    # print(list_of_product_created_date_dict)
    number_of_auction_created_in_days_dict = create_data_for_chart(
        list_of_product_created_date_dict, 'day', get_day_dict)

    # NUMBER OF AUCTION COMPLETED DATA GENERATION FOR DAY CHART
    list_of_product_completed_date_dict = Product.objects.filter(
        created_at__month=datetime.datetime.today().month).filter(
        auction_end_date__lt=datetime.datetime.now(
            Product.objects.first().auction_end_date.tzinfo)).annotate(
        day=ExtractDay(
            'auction_end_date'
        )).values('day').order_by('auction_end_date')

    number_of_auction_completed_in_days_dict = create_data_for_chart(
        list_of_product_completed_date_dict, 'day', get_day_dict)

    return JsonResponse({
        'data': {
            'labels': list(number_of_auction_created_in_days_dict.keys()),
            'datasets': [{
                'label': 'Number of Created Auction',
                'data': list(number_of_auction_created_in_days_dict.values()),
                'backgroundColor': colorDanger,
                'borderColor': colorDangerBorder,
                'borderWidth': 1,
            },
                {
                    'label': 'Number of Completed Auction',
                    'data': list(
                        number_of_auction_completed_in_days_dict.values()),
                    'backgroundColor': colorPrimary,
                    'borderColor': colorPrimaryBorder,
                    'borderWidth': 1,
                }
            ]
        },
    })


@login_required(login_url='authentication:user-login')
def created_completed_auction_hour_chart(request):
    """
    Chart for number of created and completed auctions in each hour
    :param request:
    :type request:
    :return:
    :rtype:
    """

    # NUMBER OF AUCTION CREATED DATA GENERATION FOR HOUR CHART
    list_of_product_created_hour_dict = Product.objects.filter(
        created_at__month=datetime.datetime.today().month).filter(
        created_at__day=datetime.datetime.today().date().day).annotate(
        hour=ExtractHour('created_at')).values('hour').order_by('created_at')

    number_of_auction_created_in_hour_dict = create_data_for_chart(
        list_of_product_created_hour_dict,
        'hour',
        get_hour_dict
    )

    # NUMBER OF AUCTION COMPLETED DATA GENERATION FOR HOUR CHART
    list_of_product_completed_hour_queryset = Product.objects.filter(
        created_at__month=datetime.datetime.today().month).filter(
        auction_end_date__lt=datetime.datetime.now(
            Product.objects.first().auction_end_date.tzinfo)).filter(
        auction_end_date__day=datetime.datetime.today().day).annotate(
        hour=ExtractHour('auction_end_date')).values('hour').order_by(
        'auction_end_date')

    number_of_auction_completed_in_hour_dict = create_data_for_chart(
        list_of_product_completed_hour_queryset,
        'hour',
        get_hour_dict
    )

    return JsonResponse({
        'data': {
            'labels': list(number_of_auction_created_in_hour_dict.keys()),
            'datasets': [{
                'label': 'Number of Created Auction',
                'data': list(number_of_auction_created_in_hour_dict.values()),
                'backgroundColor': colorDanger,
                'borderColor': colorDangerBorder,
                'borderWidth': 1,
            },
                {
                    'label': 'Number of Completed Auction',
                    'data': list(
                        number_of_auction_completed_in_hour_dict.values()),
                    'backgroundColor': colorPrimary,
                    'borderColor': colorPrimaryBorder,
                    'borderWidth': 1,
                }
            ]
        },
    })


@login_required(login_url='authentication:user-login')
def created_completed_auction_minute_chart(request):
    """
    Chart for number of created and completed auctions in each minute
    :param request:
    :type request:
    :return:
    :rtype:
    """

    # NUMBER OF AUCTION CREATED DATA GENERATION FOR MINUTE CHART
    list_of_product_created_minute_dict = Product.objects.filter(
        created_at__month=datetime.datetime.today().month).filter(
        created_at__day=datetime.datetime.today().date().day).filter(
        created_at__hour=datetime.datetime.today().hour).annotate(
        minute=ExtractMinute('created_at')).values('minute').order_by(
        'created_at')
    # print(list_of_product_created_minute_dict)
    number_of_auction_created_in_minute_dict = create_data_for_chart(
        list_of_product_created_minute_dict,
        'minute',
        get_minute_dict
    )

    # NUMBER OF AUCTION COMPLETED DATA GENERATION FOR MINUTE CHART
    list_of_product_completed_minute_queryset = Product.objects.filter(
        created_at__month=datetime.datetime.today().month).filter(
        auction_end_date__lt=datetime.datetime.now(
            Product.objects.first().auction_end_date.tzinfo)).filter(
        auction_end_date__day=datetime.datetime.today().day).filter(
        auction_end_date__hour=datetime.datetime.today().hour).annotate(
        minute=ExtractMinute('auction_end_date')).values('minute').order_by(
        'auction_end_date')

    number_of_auction_completed_in_minute_dict = create_data_for_chart(
        list_of_product_completed_minute_queryset,
        'minute',
        get_minute_dict
    )

    return JsonResponse({
        'data': {
            'labels': list(number_of_auction_created_in_minute_dict.keys()),
            'datasets': [{
                'label': 'Number of Created Auction',
                'data': list(
                    number_of_auction_created_in_minute_dict.values()),
                'backgroundColor': colorDanger,
                'borderColor': colorDangerBorder,
                'borderWidth': 1,
            },
                {
                    'label': 'Number of Completed Auction',
                    'data': list(
                        number_of_auction_completed_in_minute_dict.values()),
                    'backgroundColor': colorPrimary,
                    'borderColor': colorPrimaryBorder,
                    'borderWidth': 1,
                }
            ]
        },
    })


def create_data_for_chart(list_of_product, time_range, time_range_dict):
    """
    Helper function to generate data for chart
    :param list_of_product: list of all auction products
    :type list_of_product: list
    :param time_range: chart data time range
    :type time_range: str
    :param time_range_dict: dictionary of all time range with value zero
    :type time_range_dict: func
    :return: number of the created or completed auction product with time range
    :rtype: dict
    """
    time_freq = {}
    for item in list_of_product:
        if item[time_range] in time_freq:
            time_freq[item[time_range]] += 1
        else:
            time_freq[item[time_range]] = 1

    number_of_auction_in_time_range_dict = time_range_dict()

    if time_range == 'day':
        for product_time_range in list_of_product:
            number_of_auction_in_time_range_dict[
                days[product_time_range[time_range] - 1]] = time_freq[
                product_time_range[time_range]]

        return number_of_auction_in_time_range_dict

    if time_range == 'hour':
        for product_time_range in list_of_product:
            number_of_auction_in_time_range_dict[
                hours[product_time_range[time_range]]] = time_freq[
                product_time_range[time_range]]

        return number_of_auction_in_time_range_dict

    if time_range == 'minute':
        for product_time_range in list_of_product:
            number_of_auction_in_time_range_dict[
                minutes[product_time_range[time_range]]] = time_freq[
                product_time_range[time_range]]

        return number_of_auction_in_time_range_dict


@login_required(login_url='authentication:user-login')
def total_auction_value_day_chart(request):
    """
    Chart for total auctions value based on the latest bid placed in each day
    :param request:
    :type request:
    :return:
    :rtype:
    """
    products = Product.objects.filter(is_active=True).order_by('-created_at')
    auction_day_value = {}
    if products.count() > 0:
        for day in days:
            auctions_total_value = 0
            for product in products:
                # Max bid
                max_bid_price_for_product = Bid.objects.filter(
                    product=product).filter(
                    created_at__month=datetime.datetime.today().month).filter(
                    created_at__day=day).order_by('-price').first()
                if max_bid_price_for_product is None:  # If no bid for the auction
                    auctions_total_value += 0

                else:
                    auctions_total_value += max_bid_price_for_product.price
                auction_day_value[day] = auctions_total_value

    return JsonResponse({
        'data': {
            'labels': list(auction_day_value.keys()),
            'datasets': [{
                'label': 'Total value of Auctions',
                'data': list(auction_day_value.values()),
                'fillColor': "#fff",
                'backgroundColor': 'rgba(255, 255, 255, .3)',
                'borderColor': 'rgba(255, 255, 255)',
            },
            ]
        },
    })


@login_required(login_url='authentication:user-login')
def total_auction_value_hour_chart(request):
    """
    Chart for total auctions value based on the latest bid placed in each hour
    :param request:
    :type request:
    :return:
    :rtype:
    """
    products = Product.objects.filter(is_active=True).order_by('-created_at')
    hours_total_price = {}
    if products.count() > 0:
        for hour in range(0, 24):
            price = 0
            for p in products:
                product_max_bid_per_day = Bid.objects.filter(product=p).filter(
                    created_at__month=datetime.datetime.today().month).filter(
                    created_at__day=datetime.datetime.today().day).filter(
                    created_at__hour=hour).values('price').first()

                if product_max_bid_per_day is not None:
                    price += product_max_bid_per_day['price']

            hours_total_price[hour] = price

    return JsonResponse({
        'data': {
            'labels': list(hours_total_price.keys()),
            'datasets': [{
                'label': 'Total value of Auctions',
                'data': list(hours_total_price.values()),
                'fillColor': "#fff",
                'backgroundColor': 'rgba(255, 255, 255, .3)',
                'borderColor': 'rgba(255, 255, 255)',
            },
            ]
        },
    })


@login_required(login_url='authentication:user-login')
def total_auction_value_minute_chart(request):
    """
    Chart for total auctions value based on the latest bid placed in each minute
    :param request:
    :type request:
    :return:
    :rtype:
    """
    products = Product.objects.filter(is_active=True).order_by('-created_at')
    minutes_total_price = {}
    if products.count() > 0:
        for minute in range(1, 61):
            price = 0

            for p in products:
                product_max_bid_per_day = Bid.objects.filter(product=p).filter(
                    created_at__month=datetime.datetime.today().month).filter(
                    created_at__day=datetime.datetime.today().day).filter(
                    created_at__hour=datetime.datetime.today().hour) \
                    .filter(created_at__minute=minute).values('price').first()

                if product_max_bid_per_day is not None:
                    price += product_max_bid_per_day['price']

            minutes_total_price[minute] = price
        # print(minutes_total_price)

    return JsonResponse({
        'data': {
            'labels': list(minutes_total_price.keys()),
            'datasets': [{
                'label': 'Total value of Auctions',
                'data': list(minutes_total_price.values()),
                'fillColor': "#fff",
                'backgroundColor': 'rgba(255, 255, 255, .3)',
                'borderColor': 'rgba(255, 255, 255)',
            },
            ]
        },
    })

