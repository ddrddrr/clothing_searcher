from typing import Dict, List, Tuple, Optional

SITE_NAME = COOKIE_BUTTON = SEARCH_BUTTON = SEARCH_FIELD \
    = SORT_SCRIPT = ALL_ITEMS_XPATH = PRICE_XPATH = NAME_XPATH = HREF_XPATH = str

COOKIE_SCRIPTS = SEARCH_SCRIPTS = Optional[List[str]]

COOKIE_INFO = Tuple[COOKIE_SCRIPTS, Optional[COOKIE_BUTTON]]
SEARCH_INFO = Tuple[SEARCH_SCRIPTS, Optional[SEARCH_BUTTON], Optional[SEARCH_FIELD]]
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
                    "//ul[@id='productListMain']/li//span[contains(@class,'itemInformation')]",
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
                    "//ul[@id='productListMain']/li//span[contains(@class,'itemInformation')]",
                    [".//a[@data-e2e='product-listing-name']"],
                    ".//span[@class='pri' and @data-e2e='product-listing-price'] | "
                    ".//span[@class='now']/span[@data-oi-price='']",
                    ".//a[@href]"
                )
            ),

        "https://www.urbanindustry.co.uk/":
            (
                (
                    None,
                    None,
                ),

                (
                    None,
                    "//input[@id='search-field']",
                    "//input[@id='search-field']",
                ),

                [
                    "document.getElementsByClassName('snize-main-panel-dropdown-content')[0]"
                    ".setAttribute('style', 'display: block')",

                    "document.getElementsByClassName('snize-main-panel-dropdown-relevance-desc current')[0]"
                    ".classList.remove('current')",

                    "document.getElementsByClassName('snize-main-panel-dropdown-price-asc')[0]"
                    ".classList.add('current')",

                    "document.getElementsByClassName('snize-main-panel-dropdown-price-asc current')[0]"
                    ".click()"
                ],

                (
                    "//span[@class='snize-overhidden']",
                    [".//span[contains(@class,'snize-title')]"],
                    ".//span[contains(@class,'snize-price')] | .//span[contains(@class,'snize-discounted-price')]",
                    "//li[contains(@id,'snize-product')]/a[@href]"
                )
            ),

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
                    None,
                    None,
                ),

                (
                    None,
                    "//input[@name='q' and @type='search']",
                    "//input[@name='q' and @type='search']",
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
        # TODO There are problems with item names on this website, solve somehow

        # "https://www.glami.cz/":
        #     (
        #         ("//button[@id='CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll']",
        #          "//input[@id='frm-searchForm-squery']",
        #          "//input[@id='frm-searchForm-squery']"
        #          ),
        #         [
        #             "document.getElementById('category-filter-order-change').children[0].removeAttribute('selected')",
        #             "document.getElementById('category-filter-order-change').children[1].setAttribute('selected','')",
        #             "document.getElementById('category-filter-order-change').dispatchEvent(new Event('change'))"
        #         ],
        #         (
        #             "//div[contains(@class,'tracker-item')]",
        #             ".//div[@class='item__title layer-3 title']",
        #             "(.//span[@class='price']/span[@class='item-price__new'])[1] | .//span[@class='price']"
        #         )
        #     ),
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
                    [], "//div[@class='icon icon-search_m']", "//input[@type='search']"
                ),
                [
                    "document.evaluate('//span[@class=\"title\" and contains(text(),\"HHV Clothing\")]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()",

                    "document.evaluate('//div[@class=\"title\" and contains(text(),\"Strict Search\")]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()",

                    "document.evaluate('//div[@class=\"apply\" and contains(text(),\"Apply\")]', document, null,XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()",

                    "document.evaluate('//span[@class=\"title\" and contains(text(),\"Relevance\")]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()",

                    "document.evaluate('//span[@class=\"title\" and contains(text(),\"Price (ascending)\")]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()"
                ],
                (
                    "//turbo-frame[contains(@id,'item_gallery_entry')]",
                    [".//span[@class='artist']", ".//span[@class='title']"],
                    "(.//span[@class='special' or @class='regular'])[1]",
                    ".//a[@href]"
                )
            )
    }
