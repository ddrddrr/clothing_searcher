from django import forms


class SearchForm(forms.Form):
    brand = forms.CharField(label="Enter brand here, you can leave it blank",
                            min_length=3, max_length=100, required=False,
                            widget=forms.TextInput(
                                    attrs={
                                        'type': 'search',
                                        'placeholder': 'e.g. Nike',
                                        'autofocus': 'True',
                                    }), )
    name = forms.CharField(label="Enter model here, you can leave it blank",
                           min_length=3, max_length=100, required=False,
                           widget=forms.TextInput(
                                   attrs={
                                       'type': 'search',
                                       'placeholder': 'e.g. Air Force 1',
                                   }), )

    CURRENCIES = (("EUR", "Euro"),
                  ("GBP", "British pound"),
                  ("CZK", "Czech crown"),
                  ("RUB", "Russian ruble"))
    currency = forms.ChoiceField(label="Choose your currency",
                                 choices=CURRENCIES)

    min_price = forms.IntegerField(label="What is the minimum you are willing to pay?",
                                   localize=False,
                                   initial=0, min_value=0, max_value=100_000, step_size=1)
    max_price = forms.IntegerField(label="And what about maximum?",
                                   localize=False,
                                   initial=500, min_value=0, max_value=100_000, step_size=1)

    COUNTRIES = (("", "Doesn't matter"),
                 ("GER", "Germany"),
                 ("CZ", "Czech Republic"),
                 ("GB", "Britain"),
                 ("DK", "Denmark"),
                 ("FR", "France"))

    country = forms.ChoiceField(label="Looking for a website in specific country?",
                                required=False, initial="",
                                choices=COUNTRIES)

# class CurrencySelector(forms.Form):
#     CURRENCIES = (("EUR", "Euro"),
#                   ("GBP", "British pound"),
#                   ("CZK", "Czech crown"),
#                   ("RUB", "Russian ruble"))
#     currency = forms.ChoiceField(label="Choose your currency",
#                                  choices=CURRENCIES)
#
#
# class PriceSelector(forms.Form):
#     min_val = forms.IntegerField(label="What is the minimum you are willing to pay?",
#                                  localize=False, initial=0,
#                                  min_value=0, max_value=100_000, step_size=1)
#     max_val = forms.IntegerField(label="And what about maximum?",
#                                  localize=False, initial=500,
#                                  min_value=0, max_value=100_000, step_size=1)
#
#
# class CountrySelector(forms.Form):
#     COUNTRIES = (("", "Doesn't matter"),
#                  ("GER", "Germany"),
#                  ("CZ", "Czech Republic"),
#                  ("GB", "Britain"),
#                  ("DK", "Denmark"),
#                  ("FR", "France"))
#
#     country = forms.ChoiceField(label="Looking for a website in specific country?",
#                                 required=False, initial="",
#                                 choices=COUNTRIES)
#
#
# class QueryForm(forms.Form):
#     query = forms.CharField(label="What are you looking for today?", min_length=3, max_length=100)
