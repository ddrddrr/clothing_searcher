from django.core.management.base import BaseCommand, CommandError
from typing import List, Tuple
from main_app.backend.item_fetching.get_items import get_item_info
from main_app.backend.item_fetching.item_processing import FoundItem
from ._private import is_up_to_date, ITEMS, move_image_to_static, clear_screenshot_dir
from main_app.models import Product, Website, Brand, Currency


class Command(BaseCommand):
    help = "Update item database"

    def handle(self, *args, **options):
        if len(args) > 1:
            raise CommandError("This command does not take any arguments")

        # if is_up_to_date(ITEMS):
        #     self.stdout.write("Items are already up to date")

        else:
            for item in Product.objects.all():
                item.delete()
            clear_screenshot_dir()
            for res in get_item_info():
                res: Tuple[str, str, List[FoundItem]]
                website_name, brand, items = res
                for item in items:
                    try:
                        new_path = move_image_to_static(item.image_path)
                        new_item = Product.objects.create(name=item.name,
                                                          price=item.price,
                                                          currency=Currency.objects.get(name=item.currency),
                                                          link=item.link,
                                                          image_path=new_path,
                                                          website=Website.objects.get(name=website_name))
                        new_item.brands.add(Brand.objects.get(name=brand))
                    except Exception as ex:
                        print(f"Could not create item {brand, item.name} from {website_name}\n{ex}")
                    else:
                        print(f"Created {item.name}, {item.price}, {item.currency}, {item.link},{website_name},{brand}")
                        new_item.save()
