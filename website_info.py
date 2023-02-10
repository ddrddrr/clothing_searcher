from typing import Dict, List, Tuple, Optional

SITE_NAME = COOKIE_BUTTON = SEARCH_BUTTON = SEARCH_FIELD \
    = SORT_SCRIPT = ALL_ITEMS_XPATH = PRICE_XPATH = NAME_XPATH = HREF_XPATH = str

SITES_INFO: Dict[SITE_NAME,
                 Tuple
                 [
                     Tuple[Optional[COOKIE_BUTTON], SEARCH_BUTTON, SEARCH_FIELD],
                     List[SORT_SCRIPT],
                     Tuple[ALL_ITEMS_XPATH, NAME_XPATH, PRICE_XPATH, HREF_XPATH]]
] = \
    {
        "https://www.footpatrol.com/":
            (
                (
                    "//button[@class='btn btn-level1 accept-all-cookies']",
                    "//div[@id='searchButton']",
                    "//input[@id='srchInput']"
                ),

                [
                    "document.querySelector(\"[value='']\").removeAttribute('selected','')",
                    "document.querySelector(\"[value=price-low-high]\").setAttribute('selected','')",
                    "document.getElementById('sortFormTop').dispatchEvent(new Event('submit'))"
                ],

                (
                    "//ul[@id='productListMain']/li//span[contains(@class,'itemInformation')]",
                    ".//a[@data-e2e='product-listing-name']",
                    ".//span[@class='pri' and @data-e2e='product-listing-price'] | "
                    ".//span[@class='now']/span[@data-oi-price='']",
                    ".//a[@href]"
                )
            ),

        "https://www.size.co.uk/":
            (
                (
                    "//button[@class='btn btn-level1 accept-all-cookies']",
                    "//div[@id='searchButton']",
                    "//input[@id='srchInput']"
                ),

                [
                    "document.querySelector(\"[value='']\").removeAttribute('selected','')",
                    "document.querySelector(\"[value=price-low-high]\").setAttribute('selected','')",
                    "document.getElementById('sortFormTop').dispatchEvent(new Event('submit'))"
                ],

                (
                    "//ul[@id='productListMain']/li//span[contains(@class,'itemInformation')]",
                    ".//a[@data-e2e='product-listing-name']",
                    ".//span[@class='pri' and @data-e2e='product-listing-price'] | "
                    ".//span[@class='now']/span[@data-oi-price='']",
                    ".//a[@href]"
                )
            ),

        "https://www.urbanindustry.co.uk/":
            (
                (
                    None,
                    "//input[@id='search-field']",
                    "//input[@id='search-field']"
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
                    ".//span[contains(@class,'snize-title')]",
                    ".//span[contains(@class,'snize-price')] | .//span[contains(@class,'snize-discounted-price')]",
                    "//li[contains(@id,'snize-product')]/a[@href]"
                )
            ),

        "https://www.global.jdsports.com/":
            (
                (
                    "//span[@class='closeLightbox' and contains(text(),'CLOSE X')]",
                    "//input[@id='srchInput']",
                    "//input[@id='srchInput']"
                ),

                [
                    "document.getElementsByClassName('sort')[0].children[0].removeAttribute('selected')",
                    "document.getElementsByClassName('sort')[0].children[4].setAttribute('selected','')",
                    "document.getElementsByClassName('sort')[0].dispatchEvent(new Event('change'))"
                ],

                (
                    "//li[contains(@class,'productListItem')]",
                    ".//a[@data-e2e='product-listing-name']",
                    ".//span[@class='pri' and @data-e2e='product-listing-price'] | "
                    ".//span[@class='now']/span[@data-oi-price='']",
                    ".//a[@href]"
                )
            ),
        "https://en.afew-store.com/":
            (
                (
                    None,
                    "//input[@name='q' and @type='search']",
                    "//input[@name='q' and @type='search']"
                ),

                [
                    "document.getElementsByClassName('findify-components--button btn collapsed')[0].click()",
                    "document.getElementsByClassName('findify-components--button btn nav-link').item(2).click()"
                ],
                (
                    "//div[@class='findify-components-search--lazy-results']//div[@class='row product-row']//div[@class='col']",
                    ".//p[@class='card-title']",
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
                    "//button[@class='btn btn--default CookiesInfo__cookiesInfoBtnWrapperAccept__nyIJU CookiesInfo__cookiesInfoBtnWrapperAcceptMandatory__sMpwW']",
                    None,
                    "//input[@id='productsSearch']"
                ),
                [
                    "document.getElementsByClassName('BaseSelectDropdown__select__Wc73+ BaseSelectDropdown__selectHasAFilter__c2KcV Filters__filterItem__IhPPd')[0].click()",
                    "document.getElementsByClassName('BaseSelectDropdown__selectList__MnbHH undefined ')[0].children[3].click()",
                    "document.getElementsByClassName('btn col-xs-12 col-lg-12 btn--fluid btn--spaced-bottom btn--sortingSubmit')[0].click()"
                ],
                (
                    "//div[@class='m-4 l-3 Products__productsFullWide__mix1Y xs-6']",
                    ".//div[@class='ProductItem__productCardName__DCKIH']",
                    ".//div[@class='Price__salePrice__FCFFF ProductItem__priceSale__XP3ik'] | .//div [@class='Price__price__CbfdW ProductItem__priceRegular__21q11']",
                    ".//a[@aria-label and @href]"
                )
            ),
        "https://answear.cz/c/ona":
            (
                (
                    None,
                    None,
                    "//input[@type='text']"
                ),
                [
                    "document.getElementsByClassName('BaseSelectDropdown__select__Wc73+ BaseSelectDropdown__selectHasAFilter__c2KcV Filters__filterItem__IhPPd')[0].click()",
                    "document.getElementsByClassName('BaseSelectDropdown__selectList__MnbHH undefined ')[0].children[3].click()",
                    "document.getElementsByClassName('btn col-xs-12 col-lg-12 btn--fluid btn--spaced-bottom btn--sortingSubmit')[0].click()"
                ],
                (
                    "//div[@class='m-4 l-3 Products__productsFullWide__mix1Y xs-6']",
                    ".//div[@class='ProductItem__productCardName__DCKIH']",
                    ".//div[@class='Price__salePrice__FCFFF ProductItem__priceSale__XP3ik'] | .//div [@class='Price__price__CbfdW ProductItem__priceRegular__21q11']",
                    ".//a[@aria-label and @href]")
            )
    }
