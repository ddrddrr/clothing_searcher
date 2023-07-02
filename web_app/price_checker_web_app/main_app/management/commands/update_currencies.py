from django.core.management.base import BaseCommand, CommandError
from typing import List, Tuple, Dict
from django.core.exceptions import ObjectDoesNotExist
from ._private import is_up_to_date, CURRENCIES
from main_app.models import Currency, ExchangeRate
from main_app.backend.currency_processing.currency_processing_main import get_exchange_rates
from main_app.backend.search_config import SUPPORTED_CURRENCIES


def create_currency(name, fetched_exrates, db_currencies):
    new_currency = Currency.objects.create(name=name)
    for existing_currency in db_currencies:
        exrate = fetched_exrates[existing_currency.name]
        create_exchange_rate(new_currency, existing_currency, exrate)
        yield name, existing_currency.name, exrate


def create_exchange_rate(convert_from, convert_to, rate):
    created = ExchangeRate.objects.create(convert_from=convert_from,
                                          convert_to=convert_to,
                                          rate=float(rate))
    return created


class Command(BaseCommand):
    help = "Updates exchange rates of stored currencies"

    def handle(self, *args, **options):
        if len(args) > 1:
            raise CommandError("This command does not take any arguments")

        if is_up_to_date(CURRENCIES):
            self.stdout.write("Currencies are already up to date")

        else:
            new_currencies: List[str] = []
            new_exrates: List[Tuple[str, str, str]] = []
            db_currencies = Currency.objects.all()
            db_exrates = ExchangeRate.objects.all()
            for (currency, _) in SUPPORTED_CURRENCIES:
                fetched_exrates: Dict[str, str] = get_exchange_rates(currency)

                try:
                    curr_currency = db_currencies.get(name=currency)
                except ObjectDoesNotExist:
                    for new_exrate in create_currency(currency, fetched_exrates, db_currencies):
                        new_exrates.append(new_exrate)
                    new_currencies.append(currency)
                except Exception as ex:
                    CommandError(f"Could not fetch currency {currency} - {ex}")

                else:
                    for existing_currency in db_currencies:
                        exrate = fetched_exrates[existing_currency.name]
                        try:
                            exrate_to_update = db_exrates.get(convert_from=curr_currency,
                                                              convert_to=existing_currency)
                        except ObjectDoesNotExist:
                            create_exchange_rate(curr_currency, existing_currency,
                                                 fetched_exrates[existing_currency.name])
                            new_exrates.append((currency, existing_currency.name, exrate))
                        except Exception as ex:
                            CommandError(f"Could not fetch exchange rate for {currency}, {existing_currency.name} "
                                         f"- {ex}")
                        else:
                            exrate_to_update.rate = fetched_exrates[existing_currency.name]
                            exrate_to_update.save()
                            new_exrates.append((currency, existing_currency.name, exrate))
            self.stdout.write(
                    self.style.SUCCESS('Successfully updated currencies')
            )
            if new_currencies:
                self.stdout.write("Newly added currencies:")
                for curr in new_currencies:
                    self.stdout.write(curr)
            if new_exrates:
                self.stdout.write("Newly added exchange rates:")
                for (c1, c2, exrate) in new_exrates:
                    self.stdout.write(f"{c1} - {c2} : {exrate}")
