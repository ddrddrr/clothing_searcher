from django.shortcuts import render
from .forms import SearchForm
from .item_search import find_items


def search_page(request):
    search_form = SearchForm(request.GET)
    # is_valid() strips all data
    if search_form.is_valid():
        context = {"items": find_items(search_form.cleaned_data)}

    else:
        context = {"search_form": search_form}
    return render(request, r"main_app\search_page.html", context)
