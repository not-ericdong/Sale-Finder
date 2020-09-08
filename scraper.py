import requests
from bs4 import BeautifulSoup as bs
import re
import sys
# import main

# url = main.url
url = str(input("Enter the item you want price track. ")) #press space after input
#url = "https://www.amazon.ca/dp/B07YWJZXCX?ref_=Oct_DLandingS_D_b372500d_NA"
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/84.0.4147.135 Safari/537.36"}
session = requests.Session()
page = session.get(url, headers=header)
page.raise_for_status()

soup = bs(page.content, "html5lib")

WEBSITE_DATA = {
                "solestop": soup.find("div", {"class": "prices"}),
                "amazon": soup.find("span", {"id": "price_inside_buybox"}),
                "havenshop": soup.find("div", {"class": "price"}),
                "nike": soup.find("div", {"class": "price"})
                }
WEBSITE_DATA2 = {
                "havenshop": soup.find("span", {"class": "highlight"}),
                }


def get_price(price_str):
    try:
        price_txt = re.findall(r"\d+.\d+", price_str)
        return price_txt[0]
    except IndexError:
        raise IndexError
    except TypeError:
        print("No price found.")


def find_website(url):
    domain = re.findall(r".*\.(.*)\..*", url)
    try:
        domain_elem = WEBSITE_DATA[domain[0]]
        return domain_elem.get_text()
    except IndexError:
        pass
    except KeyError:
        print("This program does not work with this website yet.")
        sys.exit(1)
    except AttributeError:
        print("Something about this website changed.")


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


data = get_item_info(url)
# print(find_website(url))
# print(data)
