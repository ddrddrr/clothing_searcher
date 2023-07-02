from datetime import timedelta
from main_app.models import UpdateTime
from django.utils import timezone

CURRENCIES, ITEMS = True, False
UPDATE_INTERVAL = timedelta(hours=1)


def is_up_to_date(currencies: bool):
    upd_time_obj = UpdateTime.objects.get()
    if currencies:
        if timezone.now() - upd_time_obj.currencies_upd_time < UPDATE_INTERVAL:
            return True
        else:
            upd_time_obj.currencies_upd_time = timezone.now()
            upd_time_obj.save()
            return False

    if timezone.now() - upd_time_obj.items_upd_time < UPDATE_INTERVAL:
        return True
    else:
        upd_time_obj.items_upd_time = timezone.now()
        upd_time_obj.save()
        return False
