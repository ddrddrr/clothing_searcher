from django.shortcuts import render
from .models import BrandStatistics
from .forms import SearchForm
from .model_processing import find_items
from main_app.backend.item_fetching.misc import saveable_to_human_readable


def search_page(request):
    search_template = r"main_app\search_page.html"
    search_form = SearchForm(request.GET)
    context = {}
    # is_valid() strips all data
    print(request.GET)
    if "search_submit" in request.GET:
        print("Search  button clicked")
        if search_form.is_valid():
            found_items = find_items(search_form.cleaned_data)
            if not found_items:
                context = {"no_items": True}
            else:
                context = {"qitems": found_items}
    else:
        brand_statisctics = BrandStatistics.objects.all()[:5]
        stats = [(saveable_to_human_readable(stat.brand.name), stat.search_count) for
                 stat in brand_statisctics]
        context = {"search_form": search_form,
                   "brand_stats": stats}

    return render(request, search_template, context)
