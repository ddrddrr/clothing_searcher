from .models import Product, BrandStatistics, Brand, ExchangeRate
from django.core.exceptions import ObjectDoesNotExist


def update_brand_search_count(brand_name: str):
    stat = BrandStatistics.objects.get(brand__name=brand_name)
    stat.search_count += 1
    stat.save()


def find_items(query):
    brand = query["brand"]
    name = query["name"]
    currency = query["currency"]
    min_price = query["min_price"]
    max_price = query["max_price"]
    country = query["country"]

    update_brand_search_count(brand)
    # we can't simply chain filters here
    filter_args = {"price__gt": min_price,
                   "price__lt": max_price,
                   "brands__name__contains": brand}
    # optional attributes
    if country:
        filter_args["website__country"] = country
    if name:
        filter_args["name__contains"] = name

    exchange_rates = ExchangeRate.objects.all().filter(convert_from__name=currency)
    products_prices = []
    found_products = Product.objects.filter(**filter_args)
    for product in found_products:
        new_prices = [f"{exrate.convert_to} - {product.price * exrate.rate}  " for exrate in exchange_rates]
        products_prices.append((product, new_prices))

    return products_prices
