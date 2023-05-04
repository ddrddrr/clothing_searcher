from django.db.models import Q, QuerySet
from .models import Product, Brand, Website
from typing import Dict


def find_items(query):
    print("in find_items", query)
    brand = query["brand"]
    name = query["name"]
    currency = query["currency"]
    min_price = query["min_price"]
    max_price = query["max_price"]
    country = query["country"]
    filter_args = {"price__gt": min_price,
                   "price__lt": max_price}
    # we can't simply chain filters here
    if country:
        filter_args["website__country"] = country
    if brand:
        filter_args["brands__name__contains"] = brand
    if name:
        filter_args["name__contains"] = name

    return Product.objects.filter(**filter_args)
