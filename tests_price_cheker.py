import importlib
import re


def test_does_html_element_comply_regex(html_element: str):
    assert bool(re.fullmatch(r'^//(\*|[a-zA-Z]+)\[.*]$', html_element))


def test_are_html_elements_in_the_right_form():
    with open("module_names", 'r') as mn:
        for module_name in mn:
            module_name = module_name[:module_name.find(";")]
            curr_module = importlib.import_module(module_name)
            for element in [curr_module.cookie_button,
                            curr_module.search_button,
                            curr_module.search_field]:
                assert test_does_html_element_comply_regex(element)

