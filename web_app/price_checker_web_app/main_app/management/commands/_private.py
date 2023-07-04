from datetime import timedelta
from main_app.models import UpdateTime
from django.utils import timezone
from django.conf import settings
import shutil
import os

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


def clear_screenshot_dir():
    for filename in os.listdir(settings.SCREENSHOTS_DIR):
        file_path = os.path.join(settings.SCREENSHOTS_DIR, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def move_image_to_static(orig_path):
    try:
        new_path = shutil.copy(orig_path, os.path.join(settings.SCREENSHOTS_DIR, os.path.basename(orig_path)))
    except Exception as ex:
        print(f"Could not copy image to static\n{ex}")
        return os.path.join(settings.SCREENSHOTS_DIR, 'placeholder.png')
    try:
        os.remove(orig_path)
    except Exception as ex:
        print(f"Could not remove original image\n{ex}")
        return os.path.join(settings.SCREENSHOTS_DIR, 'placeholder.png')
    return os.path.join("item_screenshots", os.path.basename(new_path))
