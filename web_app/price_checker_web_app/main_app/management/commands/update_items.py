from django.core.management.base import BaseCommand, CommandError
from typing import List, Tuple
from django.core.exceptions import ObjectDoesNotExist
from ._private import is_up_to_date
from main_app.models import Product, Website, Brand, Currency
from main_app.backend.get_items import get_item_info
from main_app.backend.misc import human_readable_to_saveable


class Command(BaseCommand):
    help = "Update item database"

    def handle(self, *args, **options):
        if len(args) > 1:
            raise CommandError("This command does not take any arguments")

        if is_up_to_date(False):
            self.stdout.write("Items are already up to date")

        else:
            for item in Product.objects.all():
                item.delete()

            for res in get_item_info():
                res: Tuple[str, str, Tuple[str, List[Tuple[str, float, str]]]]
                website_name, brand, (currency, items) = res
                for (name, price, href) in items:
                    new_item = Product.objects.create(name=name,
                                                      price=price,
                                                      currency=Currency.objects.get(name=currency),
                                                      link=href,
                                                      website=Website.objects.get(name=website_name))
                    new_item.brands.add(Brand.objects.get(name=human_readable_to_saveable(brand)))
                    print(f"Created {name}, {price}, {currency}, {href},{website_name}, {brand}")
                    new_item.save()
