from django import forms
from main_app.backend.item_fetching.search_config import HUMAN_READABLE_BRANDS, SUPPORTED_CURRENCIES
from django.core.exceptions import ValidationError


class PriceField(forms.IntegerField):
    def to_python(self, value):
        if value is None or value == "":
            return self.initial

        try:
            value = int(value)
        except ValueError:
            raise ValidationError("Price should be a whole number")

        if value < 0:
            raise ValidationError("Price should be a positive number")
        return value


class SearchForm(forms.Form):
    brand = forms.ChoiceField(label="Choose brand",
                              choices=HUMAN_READABLE_BRANDS)

    name = forms.CharField(label="Enter model here, you can leave it blank",
                           min_length=3, max_length=100, required=False,
                           widget=forms.TextInput(
                                   attrs={
                                       'type': 'search',
                                       'placeholder': 'e.g. Air Force 1',
                                   }), )

    currency = forms.ChoiceField(label="Choose your currency",
                                 choices=SUPPORTED_CURRENCIES)

    min_price = PriceField(label="What is the minimum you are willing to pay?",
                           required=False, initial=0,
                           min_value=0, max_value=100_000, step_size=1,
                           widget=forms.NumberInput(attrs={'placeholder': '0'}))
    max_price = PriceField(label="And what about maximum?",
                           required=False, initial=100_000,
                           min_value=0, max_value=100_000, step_size=1,
                           widget=forms.NumberInput(attrs={'placeholder': '100000'}))

    COUNTRIES = (("", "Doesn't matter"),
                 ("GER", "Germany"),
                 ("CZ", "Czech Republic"),
                 ("GB", "Britain"),
                 ("DK", "Denmark"),
                 ("FR", "France"))

    country = forms.ChoiceField(label="Looking for a website in specific country?",
                                required=False, initial="",
                                choices=COUNTRIES)

# class CreateItemForm(forms.Form):
#     brand = forms.ChoiceField(label="Choose brand",
#                               choices=HUMAN_READABLE_BRANDS)
#     name = forms.CharField(label="Write model name",
#                            min_length=3, max_length=100, required=True)
#     currency = forms.ChoiceField(label="Choose currency",
#                                  choices=SUPPORTED_CURRENCIES)
#     price = forms.FloatField(label="Enter price in selected currency", required=True)
#     WEBSITE_CHOICES = tuple([(web, web) for web in SUPPORTED_WEBSITES])
#     website = forms.ChoiceField(label="Choose website",
#                                 choices=WEBSITE_CHOICES)
#     link = forms.URLField(label="Enter URL", required=True)
