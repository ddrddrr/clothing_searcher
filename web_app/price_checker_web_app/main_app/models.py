from django.db import models
from django.utils import timezone


# from jsonfield import JSONField
# from collections import OrderedDict


class Website(models.Model):
    name = models.URLField(max_length=200)
    delivery_cost = models.FloatField(blank=True, null=True)
    country = models.CharField(max_length=50)

    def __str__(self):
        return f"Website: {self.name}; delivery cost: {self.delivery_cost}; website country: {self.country}"


# class Category(models.Model):
#     name = models.CharField(max_length=200)
#     class Meta:
#         verbose_name_plural='categories'
#
# class Gender(models.Model):
#     name = models.CharField(max_length=200)


class Brand(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


# class Attribute(models.Model):
#     name = models.CharField(max_length=200)
#
#
# class AttributeValue(models.Model):
#     name = models.ForeignKey(Attribute, on_delete=models.CASCADE)
#     value = models.CharField(max_length=200)


class Product(models.Model):
    # Name of the model, upper snake case
    name = models.CharField(max_length=300)
    # Price is always stored in euros
    price = models.FloatField()
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE)
    # The link to an item can be with a lot of query parameters
    link = models.URLField(max_length=1000)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    brands = models.ManyToManyField(Brand)

    # size = models.FloatField(null=True, blank=True)
    # attributes = models.ManyToManyField(AttributeValue)
    # category = models.ManyToManyField(Category)
    # gender = models.ForeignKey(Gender, on_delete=models.PROTECT, null=True, blank=True)
    class Meta:
        ordering = ('price',)

    def __str__(self):
        return self.name


# class SizeChart(models.Model):
#     brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
#     category = models.ForeignKey(Category, on_delete=models.PROTECT)
#     gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
#     # EU, US and UK size field must be aligned but needn't be equal in length
#     # All sizes should be in form of a decimal number with precision of 1
#     # e.g. 43,5 or 28,0
#     eu_sizes = JSONField(load_kwargs={'object_pairs_hook': OrderedDict})
#     us_sizes = JSONField(load_kwargs={'object_pairs_hook': OrderedDict})
#     uk_sizes = JSONField(load_kwargs={'object_pairs_hook': OrderedDict})
#     cm_sizes = JSONField(load_kwargs={'object_pairs_hook': OrderedDict})


class BrandStatistics(models.Model):
    search_count = models.PositiveIntegerField(default=0)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-search_count']
        verbose_name_plural = "Brand Statistics"

    def __str__(self):
        return self.brand


class Currency(models.Model):
    name = models.CharField(max_length=10)
    # symmetrical=false by default, when using through models
    exchange_rates = models.ManyToManyField('self', through='ExchangeRate')

    class Meta:
        verbose_name_plural = "Currencies"

    def __str__(self):
        return self.name


class ExchangeRate(models.Model):
    convert_from = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="src_currency")
    convert_to = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="dst_currency")
    rate = models.FloatField(default=0)

    def __str__(self):
        return f"{self.convert_from.name} - {self.convert_to.name}___{self.rate}"


class UpdateTime(models.Model):
    items_upd_time = models.DateTimeField()
    currencies_upd_time = models.DateTimeField()

    def upd_item_timestamp(self):
        self.items_upd_time = timezone.now()
        self.save()

    def upd_currencies_timestamp(self):
        self.currencies_upd_time = timezone.now()
        self.save()
