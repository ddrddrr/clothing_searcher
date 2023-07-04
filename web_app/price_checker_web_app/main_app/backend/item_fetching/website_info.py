from typing import Dict, List, Tuple, Optional

SITE_NAME = COOKIE_BUTTON = SEARCH_BUTTON = SEARCH_FIELD \
    = SORT_SCRIPT = ALL_ITEMS_XPATH = PRICE_XPATH = NAME_XPATH = HREF_XPATH = str

COOKIE_SCRIPTS = SEARCH_SCRIPTS = Optional[List[str]]

COOKIE_INFO = Tuple[COOKIE_SCRIPTS, Optional[COOKIE_BUTTON]]
SEARCH_INFO = Tuple[SEARCH_SCRIPTS, Optional[SEARCH_BUTTON], Optional[SEARCH_FIELD]]
# ALL_ITEMS_XPATH should link to the biggest possible "item object", which will include the picture, name, price, href
XPATH_INFO = Tuple[ALL_ITEMS_XPATH, List[NAME_XPATH], PRICE_XPATH, HREF_XPATH]

SITES_INFO: Dict[SITE_NAME,
                 Tuple[
                     COOKIE_INFO,
                     SEARCH_INFO,
                     List[SORT_SCRIPT],
                     XPATH_INFO
                 ]
] = \
    {
        "https://www.footpatrol.com/":
            (
                (
                    None,
                    "//button[@class='btn btn-level1 accept-all-cookies']",
                ),

                (
                    None,
                    "//div[@id='searchButton']",
                    "//input[@id='srchInput']",
                ),

                [
                    "document.querySelector(\"[value='']\").removeAttribute('selected','')",
                    "document.querySelector(\"[value=price-low-high]\").setAttribute('selected','')",
                    "document.getElementById('sortFormTop').dispatchEvent(new Event('submit'))"
                ],

                (
                    "//ul[@id='productListMain']//li[@class='productListItem ' or @class='productListItem last']",
                    [".//a[@data-e2e='product-listing-name']"],
                    ".//span[@class='pri' and @data-e2e='product-listing-price'] | "
                    ".//span[@class='now']/span[@data-oi-price='']",
                    ".//a[@href]"
                )
            ),

        "https://www.size.co.uk/":
            (
                (
                    None,
                    "//button[@class='btn btn-level1 accept-all-cookies']",
                ),

                (
                    None,
                    "//div[@id='searchButton']",
                    "//input[@id='srchInput']",
                ),

                [
                    "document.querySelector(\"[value='']\").removeAttribute('selected','')",
                    "document.querySelector(\"[value=price-low-high]\").setAttribute('selected','')",
                    "document.getElementById('sortFormTop').dispatchEvent(new Event('submit'))"
                ],

                (
                    "//ul[@id='productListMain']//li[@class='productListItem ' or @class='productListItem last']",
                    [".//a[@data-e2e='product-listing-name']"],
                    ".//span[@class='pri' and @data-e2e='product-listing-price'] | "
                    ".//span[@class='now']/span[@data-oi-price='']",
                    ".//a[@href]"
                )
            ),

        # "https://www.urbanindustry.co.uk/":
        #     (
        #         (
        #             None,
        #             None,
        #         ),
        #
        #         (
        #             None,
        #             "//input[@id='Search-In-Modal']",
        #             "//input[@id='Search-In-Modal']",
        #         ),
        #
        #         [
        #             'document.getElementById("SortBy")[1].setAttribute("selected","selected")',
        #             'document.getElementById("SortBy")[0].removeAttribute("selected")',
        #             'document.getElementById("FacetSortForm").submit'
        #
        #         ],
        #
        #         (
        #             "//span[@class='snize-overhidden']",
        #             [".//span[contains(@class,'snize-title')]"],
        #             ".//span[contains(@class,'snize-price')] | .//span[contains(@class,'snize-discounted-price')]",
        #             "//li[contains(@id,'snize-product')]/a[@href]"
        #         )
        #     ),

        "https://www.global.jdsports.com/":
            (
                (
                    None,
                    None,
                ),

                (
                    None,
                    "//input[@id='srchInput']",
                    "//input[@id='srchInput']",
                ),

                [
                    "document.getElementsByClassName('sort')[0].children[0].removeAttribute('selected')",
                    "document.getElementsByClassName('sort')[0].children[4].setAttribute('selected','')",
                    "document.getElementsByClassName('sort')[0].dispatchEvent(new Event('change'))"
                ],

                (
                    "//li[contains(@class,'productListItem')]",
                    [".//a[@data-e2e='product-listing-name']"],
                    ".//span[@class='pri' and @data-e2e='product-listing-price'] | "
                    ".//span[@class='now']/span[@data-oi-price='']",
                    ".//a[@href]"
                )
            ),
        "https://en.afew-store.com/":
            (
                (
                    ["await new Promise(r => setTimeout(r, 2000));"],
                    "//button[@id='onetrust-reject-all-handler']",
                ),

                (
                    [],
                    None,
                    None
                ),

                [
                    "document.getElementsByClassName('findify-components--button btn collapsed')[0].click()",
                    "document.getElementsByClassName('findify-components--button btn nav-link').item(2).click()"
                ],
                (
                    "//div[@class='findify-components-search--lazy-results']//div[@class='row product-row']//div[@class='col']",
                    [".//p[@class='card-title']"],
                    ".//span[@class='price']",
                    ".//a[contains(@id,'findify') and @href]"
                )
            ),
        "https://answear.cz/c/on":
            (
                (
                    None,
                    "//button[@class='btn btn--default CookiesInfo__cookiesInfoBtnWrapperAccept__nyIJU CookiesInfo__cookiesInfoBtnWrapperAcceptMandatory__sMpwW']",
                ),

                (
                    None,
                    None,
                    "//input[@id='productsSearch']",
                ),
                [
                    "document.getElementsByClassName('BaseSelectDropdown__select__Wc73+ BaseSelectDropdown__selectHasAFilter__c2KcV Filters__filterItem__IhPPd')[0].click()",
                    "document.getElementById('price_asc_radio_0').click()",
                    "document.getElementsByClassName('btn xs-12 l-12 btn--fluid btn--spaced-bottom btn--sortingSubmit')[0].click()"
                ],
                (
                    "//div[@class='m-4 l-3 Products__productsFullWide__mix1Y xs-6']",
                    [".//div[@class='ProductItem__productCardName__DCKIH']"],
                    ".//div[@class='ProductItemPrice__priceSale__PueP7'] | .//div [@class='ProductItemPrice__priceRegular__7OKlG']",
                    ".//a[@aria-label and @href]"
                )
            ),
        "https://answear.cz/c/ona":
            (
                (
                    None,
                    None,
                ),

                (
                    None,
                    None,
                    "//input[@type='text']",
                ),
                [
                    "document.getElementsByClassName('BaseSelectDropdown__select__Wc73+ BaseSelectDropdown__selectHasAFilter__c2KcV Filters__filterItem__IhPPd')[0].click()",
                    "document.getElementById('price_asc_radio_0').click()",
                    "document.getElementsByClassName('btn xs-12 l-12 btn--fluid btn--spaced-bottom btn--sortingSubmit')[0].click()"
                ],
                (
                    "//div[@class='m-4 l-3 Products__productsFullWide__mix1Y xs-6']",
                    [".//div[@class='ProductItem__productCardName__DCKIH']"],
                    ".//div[@class='ProductItemPrice__priceSale__PueP7'] | .//div [@class='ProductItemPrice__priceRegular__7OKlG']",
                    ".//a[@aria-label and @href]"
                )
            ),
        # TODO a dumb captcha on ssense(easy to solve, but doesn't let you go further)

        # "https://www.ssense.com/en-cz/men":
        #     (
        #         (
        #             None,
        #             "//a[@class='hidden-tablet-landscape-2']",
        #             "//input[@id='search-form-input']"
        #         ),
        #         [
        #             "document.getElementsByClassName('accordion-links-right-nav__link')[3].click()"
        #         ],
        #         (
        #             "//div[@class='plp-products__column']",
        #             ".//span[contains(@data-test,'productName')]",
        #             ".//span[contains(@data-test,'productCurrentPrice')]",
        #             ".//a[@href]"
        #         )
        #     ),
        # "https://www.ssense.com/en-cz/women":
        #     (
        #         (
        #             None,
        #             "//a[@class='hidden-tablet-landscape-2']",
        #             "//input[@id='search-form-input']"
        #         ),
        #         [
        #             "document.getElementsByClassName('accordion-links-right-nav__link')[3].click()"
        #         ],
        #         (
        #             "//div[@class='plp-products__column']",
        #             ".//span[contains(@data-test,'productName')]",
        #             ".//span[contains(@data-test,'productCurrentPrice')]",
        #             ".//a[@href]"
        #         )
        #     )
        # TODO adapt to shadow DOM on this website
        # "https://www.asphaltgold.com/en/":
        #     (
        #         (
        #             None,
        #             None,
        #             "//input[@class='predictive-search__input']",
        #         ),
        #         [
        #             "document.evaluate('//sort-by-select[@class='filter-form']//div[@class='filter-group-toggle']',"
        #             " document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()",
        #
        #             "document.evaluate('//input[@id='Filter-price-ascending-2']', document, null,"
        #             " XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()"
        #         ],
        #         (
        #             "//div[@id='search-products-list']//a[@class='card']",
        #             ".//span[@class='card--title']",
        #             ".//div[@class='price'][1]",
        #             ".//self::a"
        #         )
        #     )
        # Many problems with this one, although it works
        "https://www.43einhalb.com/":
            (
                (
                    [
                        'document.getElementsByClassName("cmpboxbtn cmpboxbtncustom cmptxt_btn_settings")[0].click()',
                        'document.getElementsByClassName("cmpboxbtn cmpboxbtnyes cmpboxbtnyescustomchoices cmptxt_btn_save")[0].click()',
                        'document.getElementsByClassName("d-flex align-items-center text-decoration-none")[0].click()'
                    ],
                    None,
                ),

                (
                    [
                        "document.getElementById('navbar-main').className='navbar py-0 navbar-main navbar-dark bg-primary nav-search-active'",
                        "document.getElementsByClassName('nav-search')[0].className='nav-search active'",
                        "document.getElementsByClassName('dropdown-toggle form-control mr-sm-2')[0].className='dropdown-toggle form-control mr-sm-2 show'"
                    ],
                    None,
                    None
                ),
                [
                    "document.getElementsByClassName('btn btn-outline-primary dropdown-toggle')[0].click()",
                    "document.querySelector('label[data-value=price_asc]').click()"
                ],
                (
                    "//div[contains(@id,'item-') and contains(@class, 'col-6 col-sm-6 col-md-4 col-lg-4 col-xl-3 mb-3')]",
                    [".//span[@class='product-title__producer']", ".//span[@class='product-title__name']"],
                    ".//div[@class='product-price']/*[@class='product-price--new text-danger'] | .//div[@class='product-price'][not(*)]",
                    ".//a[@href]"
                )

            ),
        "https://www.hhv.de/shop/en":
            (
                (
                    None, None
                ),
                (
                    ['document.getElementsByClassName("header--localization--base-component localization")[0].click()',
                     'document.getElementsByClassName("button")[2].click()',
                     'document.getElementsByClassName("apply")[0].click()',
                     'document.getElementsByClassName("close icon-cross_m")[4].click()']
                    , "//div[@class='icon icon-search_m']", "//input[@type='search']"
                ),
                [
                    'document.getElementById(id="items--perspective--filter-list--base-component-strict").click()',
                    'document.getElementsByClassName("value no_child")[1].click()',
                    'document.getElementsByClassName("apply")[8].click()',
                    'document.getElementsByClassName("anchor")[2].click()',
                    'document.getElementsByClassName("shared--dropdown--options--base-component options flat")['
                    '3].children[4].click()',

                ],
                (
                    "//turbo-frame[contains(@data-controller,'items--shared--gallery-entry--base-component') and not(@data-action='')]",
                    [".//div[@class='lower'][1]//span[@class='artist']",
                     ".//div[@class='lower'][1]//span[@class='title']"],
                    "(.//div[@class='lower'][1]//span[@class='special' or @class='regular'])[1]",
                    ".//a[@href][1]"
                )
            )
    }
