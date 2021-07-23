import os
import sys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver import Firefox, Chrome, Opera, Safari, Proxy
main_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
from selenium.webdriver.common.action_chains import ActionChains
from pyvirtualdisplay import Display

sys.path.append(main_dir)
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import random
import pdb
import json
from datetime import date
import re as r


class SeleniumScrapper(object):
    """
    This class provides the capabilities
    of buying shoes in the nike website.

    for now it only manages to buy sneakers
    """

    start_urls = [
        "https://www.alkosto.com/electrodomesticos/grandes-electrodomesticos/"
        "refrigeracion/neveras/c/BI_A29_ALKOS?page=1&pageSize=100&sort=relevance"
    ]
    PROXY_OBJ = Proxy

    def random_agent(self):
        """
        generates a random agent for avoiding blocking
        :return: random agent object
        """
        software_names = [SoftwareName.FIREFOX.value]
        operating_systems = [
            OperatingSystem.WINDOWS.value,
            OperatingSystem.LINUX.value,
        ]
        user_agent_rotator = UserAgent(
            software_names=software_names,
            operating_systems=operating_systems,
            limit=100,
        )
        user_agent = user_agent_rotator.get_random_user_agent()
        return user_agent

    def load_proxy_settings(self):
        """
        gets  the proxy capabilities
        in order to avoid getting blacklisted
        :return: dict
        """

    def type_words(self, element, value):
        """
        types the words in the given element simulating
        the keyboard inputs
        :param element: selenium element
        representing html object
        :param value: str: value to input
        :return: tuple
        """
        success = False
        result = {}
        try:
            element.clear()
            for word in value:
                element.send_keys(word)
                time.sleep(0.1)
            success = True
        except Exception as X:
            result["error"] = f"There was an error: {X}"
        return success, result


    def scroll_to_item(
        self,
        driver: object,
        option: str,
        element_xpath: str = None,
        css_selector: str = None,
        iterable: int = 100,
    ) -> dict:
        """
        scrolls to the item until it's visible
        :param driver: selenium class
        :param element_xpath: str: xpath: element to scroll to
        :param option: str: action to perform to the item when it's visible:
        you can either click or fill it with a random_value or
         get the full_data of the page
        :return: dict
        """
        result = {}
        page_scrollable_size = int(
            driver.execute_script("return document.body.scrollHeight")
        )
        try:
            while iterable < page_scrollable_size:
                driver.execute_script(f"window.scrollTo(0, {iterable})")
                print("Scrolling", iterable)
                iterable += 100
                if option == "click":
                    driver.find_element_by_xpath(element_xpath).click() if element_xpath else \
                        driver.find_element_by_css_selector(css_selector).click()
                    result["message"] = "success"
                    result["driver"] = driver
                    result["status"] = True
                    return result
            else:
                if iterable >= page_scrollable_size:
                    if option == 'full_data':
                        import pdb;pdb.set_trace()
                        result['page'] = driver.find_element_by_tag_name('body').text

                    else:
                        result["status"] = False
                        result["error"] = "The item was not located properly"

        except ElementNotInteractableException:
            iterable += 105
            print("Scrolling EX", iterable)
            driver.execute_script(f"window.scrollTo(0, {iterable})")
            status, result = self.scroll_to_item(
                driver=driver,
                element_xpath=element_xpath,
                iterable=iterable,
                option=option,
            )

        except Exception as X:
            result["status"] = False
            result["error"] = f"There was an unexpected error: {X}"
        return result


    def _get_drivers(self):
        """
        loads the drivers based on the options and
        operative system
        :return: dict
        """
        result = {}
        if sys.platform == "linux":
            result = {
                "firefox": f"{main_dir}/scout_monitor_fetcher/browser_drivers/geckodriver",
                "opera": f"{main_dir}/scout_monitor_fetcher/browser_drivers/operadriver",
                "chrome": f"{main_dir}/scout_monitor_fetcher/browser_drivers/chromedriver",
            }

        # elif "win" in sys.platform:
        #     result = {
        #         "firefox": f"{main_dir}/scout_monitor_fetcher/browser_drivers/geckodriver_win",
        #         "opera": f"{main_dir}/scout_monitor_fetcher/browser_drivers/operadriver_win",
        #         "chrome": f"{main_dir}/scout_monitor_fetcher/browser_drivers/chromedrive_win",
        #     }

        else:
            result = {
                "firefox": f"{main_dir}/scout_monitor_fetcher/browser_drivers/geckodriver_mac",
                "opera": f"{main_dir}/scout_monitor_fetcher/browser_drivers/operadriver_mac",
                "chrome": f"{main_dir}/scout_monitor_fetcher/browser_drivers/chromedriver_mac",
            }

        return result

    def get_driver_configurations(
        self, driver_option, production=False, **kwargs
    ) -> tuple:
        """
        generates the driver option based on the driver and the parameters
        provided
        :param driver_option: str
        :param production: bool: whether it should launch the browser or not
        :param kwargs: dict of arguments related to the driver
        :return: tuple
        """
        available_driver_options = {
            "firefox": webdriver.FirefoxOptions(),
            "opera": {},
            "safari": {},
            "chrome": webdriver.ChromeOptions(),
        }
        status, result = False, {}
        try:
            option = available_driver_options[driver_option]
            if not isinstance(option, dict):
                if production:
                    option.add_argument("--headless")

                if "proxy" in kwargs.keys():
                    option.add_argument(
                        f'--proxy-server={kwargs.pop("proxy")}'
                    )

                for key in kwargs.keys():
                    option.add_argument(f"{kwargs[key]}")

                option.add_argument(f"user-agent={self.random_agent()}")
            result = option
            status = True
        except Exception:
            result["error"] = f"{Exception}"

        return status, result

    def _load_driver(self, web_driver_option, **driver_config):
        """
        loads the driver object and makes sure the driver provided is supported
        :param driver_option: str: only available firefox, phantom, safari, chrome, opera
        :return: tuple
        """
        driver = None
        available_web_drivers = {
            "firefox": Firefox,
            "opera": Opera,
            "safari": Safari,
            "chrome": Chrome,
        }
        available_driver_options = {
            "firefox": webdriver.FirefoxOptions(),
            "opera": {},
            "safari": {},
            "chrome": webdriver.ChromeOptions(),
        }
        drivers = self._get_drivers()
        # print(drivers)
        if web_driver_option not in available_web_drivers.keys():
            result = {
                "message": f"The given web driver is not supported,"
                f"the supported one are:{available_web_drivers.keys()}"
            }
            return False, result

        elif web_driver_option == "firefox":
            available_driver_options[web_driver_option].add_argument(
                f"user-agent={self.random_agent()}"
            )
            if "proxy" in driver_config.keys():
                available_driver_options[web_driver_option].add_argument(
                    f'--proxy-server={driver_config["proxy"]}'
                )

            # available_driver_options[web_driver_option].add_argument(
            #     f"--port={4444}"
            # )

            if "production" in driver_config.keys():
                available_driver_options[web_driver_option].add_argument(
                    f"--headless"
                )
                available_driver_options[web_driver_option].add_argument("--no-sandbox")
                available_driver_options[web_driver_option].add_argument("--disable-dev-shm-usage")
                available_driver_options[web_driver_option].add_argument("--disable-gpu")

            # local
            # driver = available_web_drivers[web_driver_option](
            #     firefox_options=available_driver_options[web_driver_option],
            #     executable_path=drivers[web_driver_option],
            #     service_log_path=f'{main_dir}/scout_monitor_fetcher/driver_logs/geckodriver.log',
            # )

            # remote
            driver = webdriver.Remote(desired_capabilities=webdriver.DesiredCapabilities.FIREFOX,
            options= available_driver_options[web_driver_option])



        elif web_driver_option == "chrome":
            available_driver_options[web_driver_option].add_argument(
                f"user-agent={self.random_agent()}"
            )
            if "proxy" in driver_config.keys():
                available_driver_options[web_driver_option].add_argument(
                    f'--proxy-server={driver_config["proxy"]}'
                )

            if "production" in driver_config.keys():
                available_driver_options[web_driver_option].add_argument(
                    f"--headless"
                )
                available_driver_options[web_driver_option].add_argument("--no-sandbox")
                available_driver_options[web_driver_option].add_argument("--disable-dev-shm-usage")
                available_driver_options[web_driver_option].add_argument("--disable-gpu")


            driver = available_web_drivers[web_driver_option](
                chrome_options=available_driver_options[web_driver_option],
                executable_path=drivers[web_driver_option],
                service_log_path=f'{main_dir}/scout_monitor_fetcher/driver_logs/chromedriver.log'

            )

        else:
            driver = available_web_drivers[web_driver_option]()

        return True, driver

    def select_item_in_select_element(
        self, select_element: object, option: str
    ) -> tuple:
        """
        selects the item in the select element
        and returns whether it was successful or not
        :param select_element: webdriver element
        :param option: str
        :return: tuple
        """
        status = False
        result = {}
        try:
            selector = Select(select_element)
            selector.select_by_visible_text(option)
            status = True
        except Exception as X:
            result["error"] = f"There was an error with the selection{X}"
        finally:
            return status, result

    def fill_out_form(
        self, elements: dict, data: dict, selects: list = [], checks: list = []
    ) -> tuple:
        """
        fill out the form for the given elements
        :param elements: dict of fields coming from selenium
        :param data: dict: user data
        :param selects: list: a list of the items which are a select
        :param checks: list: list of checkboxes
        :return: tuple: status and message if any
        """
        status = False
        result = {}
        try:
            for key in elements.keys():
                if key not in selects and key not in checks:
                    status, result = self.type_words(elements[key], data[key])
                    if not status:
                        break
                elif key in selects:
                    for item in selects:
                        if item == key:
                            status, result = self.select_item_in_select_element(
                                elements[item], data[key]
                            )
                            if not status:
                                break
                elif key in checks:
                    for item in checks:
                        if item == key and not item.is_selected():
                            item.click()
            else:
                result["message"] = "Success"
        except Exception as X:
            result["error"] = f"There has been an error: {X}"
        finally:
            return status, result

    def wait_until_clickable(
        self, driver, xpath=None, class_name=None, duration=100, frequency=0.01
    ):
        """
        waits until the item becomes clickable
        :param driver: object driver
        :param xpath: str
        :param class_name: css class
        :param duration: time to wait for the execution if not then it passes, it's timed in seconds
        :param frequency: how quick it should pass
        :return: None
        """
        if xpath:
            WebDriverWait(driver, duration, frequency).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
        elif class_name:
            WebDriverWait(driver, duration, frequency).until(
                EC.element_to_be_clickable((By.CLASS_NAME, class_name))
            )

    def wait_until_visible(
        self, driver, xpath=None, class_name=None, duration=100, frequency=0.01
    ):
        """
        waits until the given elemenent with the xpath is visible in order to execute an specific
        acction
        :param driver: object driver
        :param xpath: str
        :param class_name: css class
        :param duration: time to wait for the execution if not then it passes, it's timed in seconds
        :param frequency: how quick it should pass
        :return: None
        """
        if xpath:
            WebDriverWait(driver, duration, frequency).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
        elif class_name:
            WebDriverWait(driver, duration, frequency).until(
                EC.visibility_of_element_located((By.CLASS_NAME, class_name))
            )

    def get_full_site_content(self, url, **options):
        """
        gets all information from the site, this should be used
        whenever there's an issue with the scraper which doesn't bring
        the full data from the site therefore we need to wait for the data
        to be full loaded

        :param url:
        :param options: dict: keyword arguments to add customisation
        to the execution to the bot itself.
        :return: str the full body of the site
        """
        driver = self.get_driver()
        driver.get(url)
        status, data =self.handler.scroll_to_item(
            iterable=100,
            option='full_data',
            element_xpath=options['xpath'],
            driver=driver
        )
        # if not status:
        #     pdb.set_trace()
        return data['page']

    def verify_exists(self, css_selector: str, driver: webdriver)->bool:
        """
        basically we check whether the item given
        exists
        :param item: str: css_selector for the moment
        :param driver: web driver to interact with
        :return: bool
        """
        result = False
        try:
            driver.find_element_by_css_selector(css_selector)
            result = True

        except NoSuchElementException:
            pass

        return result

    def scrape_items(self):
        """
        this is the method that is going to implement all of the
        methods related of fetching the data from the site.
        :return: dict
        """
        # display = Display(visible=False, size=(800, 600))
        # display.start()
        flag, driver = self._load_driver('firefox', production=True)
        # flag, driver = self._load_driver('firefox')  # debugging
        scrapped_data = []
        result = {}

        try:
            if flag:
                for url in self.start_urls:
                    driver.get(url)
                    if self.verify_exists("div[id~='js-cookie-notification']", driver=driver):
                        cookies = driver.find_element_by_css_selector("div[id~='js-cookie-notification']")
                        cookies.find_element_by_tag_name('button').click()
                    # products = self.get_products_from_page(driver=driver) # modified
                    products = self.get_items_from_main_page(driver=driver) # modified
                    for i, product in enumerate(products):
                        print(f"Fetching Data From product: {product} {i+1} out of {len(products)}")
                        scrapped_product = self.get_product_details(driver=driver, product_url=product)
                        print(scrapped_product)
                        if scrapped_product:
                            scrapped_data.append(scrapped_product)

                result.update(status=True)
                result.update(message='The data has been successfully Extracted!!.')
                result.update(data=scrapped_data)
                # pdb.set_trace()
                driver.quit()
                # display.stop()
            else:
                raise Exception(driver['message'])

        except TimeoutException:
            driver.quit()
            # display.stop()
            # self.force_purge()
            return self.scrape_items()

        except Exception as X:
            result['status'] = False
            result['error'] = f"{X}"
            driver.quit()
        # pdb.set_trace()

        # self.force_purge()
        return result


    def get_product_details(self, driver, product_url):
        """
        parses the details for the product
        :param driver:  web driver
        :param product_url: str
        :return: dict
        """
        driver.get(product_url)
        time.sleep(3)
        product_main_element_prices_status = driver.find_element_by_css_selector("div[class~='product-main-info']")
        # pdb.set_trace()
        product = {
            'product_url': product_url,
            'name': self.get_product_name(driver),
            'sku': driver.find_element_by_class_name('product-name').find_element_by_class_name('product-name__sku-code')\
                .find_element_by_class_name('code').text.replace(' ',''),
            'prices': self.get_product_prices(main_element=product_main_element_prices_status),
        }
        if product['prices'] == {}:
            return {}

        # product['status'] = self.get_product_status(product_main_element_prices_status) # this doesn't exist anymore
        product['images'] = self.get_product_images(driver=driver)
        # pdb.set_trace()

        # need to redesign the whole methods to make it work.

        product['details'] = self.get_product_specs(driver=driver)
        # product['reviews'] = self.get_product_reviews(driver=driver)

        return product

    def get_product_status(self, main_element):
        """
        gets the status of the product so that
        if there's any errors, it will be easy to
        fix that
        :param main_element:
        :return: str
        """
        status =""
        try:
            status = main_element.find_element_by_css_selector(
                "p[class~='availability']").text.split(':')[1]
        except:
            pass
        return status

    def get_product_name(self, driver):
        """
        parses the product name from the
        product site
        :param driver: web driver
        :return: str
        """
        try:
            names = driver.find_elements_by_css_selector(
                "div[class~='product-name']")
            return names[1].find_element_by_tag_name('h1').text if len(names) > 1 \
                else names[0].find_element_by_tag_name('h1').text
        except IndexError:
            # pdb.set_trace()
            raise IndexError

    def get_product_prices(self, main_element):
        """
        gets the prices for the product
        :param main_element: web driver
        :return: dict
        """
        prices = {}
        try:
            prices['normal_price'] = self.serialize_price(
                main_element.find_element_by_css_selector("span[class~='before-price']").text)
        except:
            pass

        try:
            prices['daily_price'] = self.serialize_price(
                main_element.find_element_by_css_selector("span[class~='price-alkosto']").text)
        except:
            pass

        try:
            prices['special_price'] = self.serialize_price(
                main_element.find_element_by_css_selector("span[class~='card-price']").text)
        except:
            pass

            # pdb.set_trace()

        return prices

    def serialize_price(self, price:str)->float:
        """
        serializes the price given so that the
        storage doesn't have to worry about it.
        :param price: str
        :return: float
        """
        final_price = price.replace('$', '')

        if 'A' in price:
            final_price =  final_price.split(' ')[0]
            final_price = final_price.replace('.', '')

        elif '\n':
            final_price = final_price.split('\n')[0]
            final_price = final_price.replace('.', '')

        else:
            final_price = price.replace('.','')
        return float(final_price)

    def get_product_images(self, driver):
        """
        gathers all images for the product
        :param driver: web driver
        :return: list
        """
        main_pictures_container = driver.find_element_by_class_name("image-gallery__thumb-gallery")
        pictures = []
        for picture in main_pictures_container.find_elements_by_class_name("owl-item"):

            try:
                pictures.append(picture.find_element_by_tag_name('a')\
                                .find_element_by_tag_name('img').get_attribute('src'))

            except NoSuchElementException:
                continue

        return pictures

    # modified
    def get_product_specs(self, driver):
        """
        finds and loads all products specifications
        :param driver: web driver
        :return: dict
        """
        specs_tab = driver.find_element_by_css_selector("div[id~='js-AnchorSpecsTab']")
        driver.execute_script(f"window.scrollTo(0, {specs_tab.location['y']-400})")
        specs_tab.click()
        result = {}
        time.sleep(2)
        data_containers = driver.find_element_by_css_selector(
            "div[class~='product-classifications']").find_elements_by_css_selector("div[class~='js-specsHeadline']")
        # pdb.set_trace()
        for index, container in enumerate(data_containers):
            container.click()
            data_containers_dt = driver.find_element_by_class_name(
                "product-classifications").find_elements_by_class_name("js-specsContent")

            datatable = data_containers_dt[index].find_element_by_css_selector("table[class~='table-striped']")
            for row in datatable.find_elements_by_tag_name('tr'):
                data = row.find_elements_by_tag_name('td')
                # print(data[0].text,data[1].text)
                result[data[0].text.lower()] = data[1].text
            container.click()
        # pdb.set_trace()

        return result

    def get_product_reviews(self, driver):
        """
        loads the reviews for the product
        :param driver: web driver
        :return: dict
        """
        try:
            selector = driver.find_element_by_css_selector('dt[id~="review-yotpo"]')
            driver.execute_script(f"window.scrollTo(0, {selector.location['y']-200})")
            selector.click()
            time.sleep(2)
            pages = self.get_pages_from_reviews_pagination(driver=driver)
            review = {
                'total_qualification': driver.find_element_by_css_selector("span[class~='yotpo-star-digits']").text,
                'total_reviews': driver.find_element_by_css_selector("span[class~='yotpo-sum-reviews']"
                                                                     ).find_element_by_tag_name('span').text,
                'review_list': []
            }
            if pages:
                for page in pages:
                    try:
                        next_btn = driver.find_element_by_css_selector("a[class~='yotpo_next']")
                        r = self.get_reviews_from_page(driver=driver)
                        for item in r:
                            review['review_list'].append(item)
                        driver.execute_script(f"window.scrollTo(0, {next_btn.location['y']-1500})")
                        time.sleep(3)
                        next_btn.click()

                    except StaleElementReferenceException:
                        next_btn = driver.find_element_by_css_selector("a[class~='yotpo_next']")
                        # print(next_btn.location)
                        driver.execute_script(f"window.scrollTo(0, {next_btn.location['y']-1500})")
                        time.sleep(3)
                        next_btn.click()
            else:
                r = self.get_reviews_from_page(driver=driver)
                for item in r:
                    review['review_list'].append(item)
        except Exception as X:
            execp = X
            print(execp)
            review = {}
            # pdb.set_trace()
        return review

    def get_pages_from_reviews_pagination(self, driver):
        """
        gets all of the pages to load in order to get the items
        from the driver itself.
        :param driver: driver
        :return: list
        """
        try:
            pager = driver.find_element_by_css_selector('div[class~="yotpo-pager"]')
            return [element for element in pager.find_elements_by_class_name("yotpo-page-element")
                if element.get_attribute("href") and '#' in element.get_attribute("href")
                ]
        except NoSuchElementException:
            return None


    def get_reviews_from_page(self, driver):
        """
        gets all of the pages to load in order to get the items
        from the driver itself.
        :param driver: driver
        :return: list
        """
        main_review_container = driver.find_element_by_css_selector("div[class~='yotpo-nav-content']")
        reviews = [
            {
                'qualification': self.generate_review_score(review_element=element),
                'review_date': element.find_element_by_css_selector("span[class~='yotpo-review-date']"
                                                                    ).text.replace('/','-'),
                'comment': self.get_review_comment(review_element=element)
            } for element in main_review_container.find_elements_by_css_selector("div[class~='yotpo-review']")

        ]

        return reviews


    def generate_review_score(self, review_element):
        """
        generates a score to the review stars given by the
        class name of the stars
        :param review_element: selenium driver element
        :return: int
        """
        try:
            empty_stars = len(review_element.find_elements_by_css_selector("span[class~='yotpo-icon-empty-star']"))
            full_stars = len(review_element.find_elements_by_css_selector("span[class~='yotpo-icon-star']"))
            return full_stars-empty_stars if empty_stars < full_stars else 0
        except NoSuchElementException:
            return 0

    def get_review_comment(self, review_element):
        """
        parses the text element of the review
        so that the text is parsed accordingly.
        :param review_element: selenium driver element
        :return: str
        """
        review_container = review_element.find_element_by_css_selector("div[class~='yotpo-main']")
        review_title = review_container.find_element_by_css_selector("div[class~='content-title']")
        review_content = review_container.find_element_by_css_selector("div[class~='content-review']")
        return f"{review_title.text}: {review_content.text}"

    def get_items_from_main_page(self, driver: webdriver) -> list :
        """
        gathers all of the items from the main page, whether there's
        pagination or not.
        :param driver: Selenium Web driver
        :return: list
        """
        pages = self.get_pages_from_main_product_pagination(driver)
        return [item for page_url in pages for item in self.get_products_from_page(driver=driver
                                                                                   , page_url=page_url)]

    # modified
    def get_products_from_page(self, driver, page_url:str):
        """
        gets in the page and parses all of the links for
        the products in the given page.
        :param driver: web driver
        :param page_url: url to get into
        :return: list
        """
        driver.get(page_url)
        time.sleep(2)
        pages = driver.find_element_by_css_selector("div[class~='product__list--wrapper']")
        return [element.find_element_by_tag_name('a').get_attribute('href') for element in
                pages.find_element_by_class_name('product__listing').find_elements_by_class_name(
                    'product__list--item')
                ]

    # modified
    def get_pages_from_main_product_pagination(self, driver):
        """
        gets the links of all paginatied pages so that it becomes
        easier to access the data
        :param driver: web driver
        :return: list
        pagination items:
        main_div: div[class~='pages']
        previous: a[class~='previous']
        next: a[class~='next']
        """
        items_count_class = 'pagination-bar__results'
        lowest_count = 25
        obj_count = int(driver.find_element_by_class_name(
                    items_count_class).find_element_by_tag_name('span').text.split(
                        ' ')[0])
        pages = int((obj_count / lowest_count) + 1 if  obj_count % lowest_count > 0
                 else (obj_count / lowest_count))
        # pages = 1

        final_pages = [f"https://www.alkosto.com/electrodomesticos/grandes-electrodomesticos/"
                       f"refrigeracion/neveras/c/BI_A29_ALKOS?page={page}&pageSize=25&sort=relevance"
                       for page in range(1, pages+1)
                        ]

        return final_pages


    def force_purge(self):
        """
        forces the exit of the driver and web browser
        :return: None
        """
        os.system("pkill -9 -f selenium")
        os.system("pkill -9 -f firefox")


if __name__ == '__main__':
    handler = SeleniumScrapper()
    print(handler.scrape_items())