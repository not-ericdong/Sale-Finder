import requests
from bs4 import BeautifulSoup as bs
import re
import sys


def find_website(url):
    # url = str(input("Enter the item you want price track. ")) #press space after input
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    session = requests.Session()
    page = session.get(url, headers=header)
    page.raise_for_status()
    soup = bs(page.content, "html5lib")
    print(soup.find("div", {"class": "product-price"}))
    # can add more websites
    WEBSITE_DATA = {
                    "solestop": soup.find("div", {"class": "prices"}),
                    "amazon": soup.find("span", {"id": "price_inside_buybox"}),
                    "ebay": soup.find("span", {"id": "prcIsum"}),
                    "nike": soup.find("div", {"class": "product-price"}),
                    "adidas": soup.find("span", {"class": "gl-price__value"})
                    }

    domain = re.findall(r".*\.(.*)\..*", url)
    try:
        domain_elem = WEBSITE_DATA[domain[0]]  # todo this is giving me none
        return domain_elem.get_text()
    except IndexError:
        pass
    except KeyError:
        print("This program does not work with this website yet.")
        sys.exit(1)
    except AttributeError:
        print("Something about this website changed.")
        sys.exit(1)


def get_price(price_str):
    try:
        price_txt = re.findall(r"\d+.\d+", price_str)
        return price_txt[0]
    except IndexError:
        pass
    except TypeError:
        print("No price found.")
        sys.exit(1)


def get_item_info(url):
    item_info = {"price": 0, "url": "", "sale": False}
    if url is None:
        item_info = None
    else:
        web_data = find_website(url)
        item_info["price"] = get_price(web_data)
        item_info["url"] = url
        item_info["sale"] = False

    return item_info
