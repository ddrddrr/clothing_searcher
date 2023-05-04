import currency_processing_main as cp
import currency_proc_misc as cpm


def test_get_exchange_rate():
    for currency_from in cpm.CURRENCY_NAMES:
        for currency_to in cpm.CURRENCY_NAMES:
            res = cp.get_exchange_rate(currency_from, currency_to)
            assert isinstance(res, float)


