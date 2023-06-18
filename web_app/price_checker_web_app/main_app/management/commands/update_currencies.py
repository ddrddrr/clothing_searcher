from django.core.management.base import BaseCommand, CommandError
from typing import List, Tuple
from django.core.exceptions import ObjectDoesNotExist
from ._private import is_up_to_date
from main_app.models import Currency, ExchangeRate
from main_app.backend.currency_processing.currency_processing_main import get_exchange_rates
from main_app.backend.search_config import SUPPORTED_CURRENCIES


def create_exchange_rate(convert_from, convert_to, rate):
    created = ExchangeRate.objects.create(convert_from=convert_from,
                                          convert_to=convert_to,
                                          rate=rate)
    return created


class Command(BaseCommand):
    help = "Updates exchange rates of stored currencies"

    def handle(self, *args, **options):
        if len(args) > 1:
            raise CommandError("This command does not take any arguments")

        if is_up_to_date(True):
            self.stdout.write("Currencies are already up to date")

        else:
            new_currencies: List[str] = []
            new_exrates: List[Tuple[str, str]] = []
            db_currencies = Currency.objects.all()
            db_exrates = ExchangeRate.objects.all()
            for (currency, _) in SUPPORTED_CURRENCIES:
                fetched_exrates = get_exchange_rates(currency)

                try:
                    curr_currency = db_currencies.get(name=currency)

                except ObjectDoesNotExist:
                    new_currency = Currency.objects.create(name=currency)
                    new_currencies.append(currency)
                    for existing_currency in db_currencies:
                        create_exchange_rate(new_currency, existing_currency, fetched_exrates[existing_currency.brand])
                        new_exrates.append((currency, existing_currency.brand))
                except Exception as ex:
                    CommandError(f"Could not fetch currency {currency} - {ex}")

                else:
                    for existing_currency in db_currencies:

                        try:
                            exrate_to_update = db_exrates.get(convert_from=curr_currency,
                                                              convert_to=existing_currency)
                        except ObjectDoesNotExist:
                            create_exchange_rate(curr_currency, existing_currency,
                                                 fetched_exrates[existing_currency.brand])
                            new_exrates.append((currency, existing_currency.brand))
                        except Exception as ex:
                            CommandError(f"Could not fetch exchange rate for {currency}, {existing_currency.brand} "
                                         f"- {ex}")
                        else:
                            exrate_to_update.rate = fetched_exrates[existing_currency.brand]
                            exrate_to_update.save()
            self.stdout.write(
                    self.style.SUCCESS('Successfully updated currencies')
            )
            if new_currencies:
                self.stdout.write("Newly added currencies:")
                for curr in new_currencies:
                    self.stdout.write(curr)
            if new_exrates:
                self.stdout.write("Newly added exchange rates:")
                for (c1, c2) in new_exrates:
                    self.stdout.write(c1, c2)
