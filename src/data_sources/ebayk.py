import bs4
import requests


# Everything:
SEARCH_URL = "https://www.ebay-kleinanzeigen.de/s-wohnung-mieten/berlin/anzeige:angebote/preis::1400/c203l3331+wohnung_mieten.qm_d:55%2C"
# No Exchange (may be excluding some legit places):
#SEARCH_URL = "https://www.ebay-kleinanzeigen.de/s-wohnung-mieten/berlin/anzeige:angebote/preis::1500/c203l3331+wohnung_mieten.qm_d:45%2C+wohnung_mieten.swap_s:nein"


class AdListing:
    """
    Class to represent an individual ebay-k listing.
    """

    def __init__(self, *args, **kwargs):
        if args and type(args[0]) is bs4.element.Tag:
            self.parse_from_tag(args[0])
        else:
            self.upload_time = kwargs.get("upload_time", 1234)
            self.location = kwargs.get("location", "12045 NK")
            self.area = kwargs.get("area", "55m^2")
            self.title = kwargs.get("title", "the title")
            self.description = kwargs.get(
                "description", "descriptions are normally longer"
            )
            self.price = kwargs.get("price", 1234)
            self.url = kwargs.get("url", "https://ebayk...")

    def __repr__(self):
        return f"{self.title} - {self.location} ({self.price}): {self.url}"

    def parse_from_tag(self, tag):
        """
        Given a bs4 tag, parse the listing details from it.
        """
        try:
            self.title = tag.find("a", class_="ellipsis").text
        except Exception as e:
            print(f"Failed to get title from {tag}")
            print("#" * 80)

        try:
            self.location = tag.find("div", class_="aditem-main--top--left").text
        except Exception as e:
            print(f"Failed to get location from {tag}")
            print("#" * 80)

        try:
            self.description = tag.find(
                "p", class_="aditem-main--middle--description"
            ).text
        except Exception as e:
            print(f"Failed to get description from {tag}")
            print("#" * 80)

        try:
            self.price = tag.find(
                "p", class_="aditem-main--middle--price-shipping--price"
            ).text.strip()
        except Exception as e:
            print(f"Failed to get price from {tag}")
            print("#" * 80)

        try:
            self.url = "https://www.ebay-kleinanzeigen.de" + tag.find("a")["href"]
        except Exception as e:
            print(f"Failed to get url from {tag}")
            print("#" * 80)

        try:
            self.upload_time = tag.find(
                "div", class_="aditem-main--top--right"
            ).text.strip()
        except Exception as e:
            print(f"Failed to get upload_time from {tag}")
            print("#" * 80)

        # TODO: Should just remove this?
        # if "top" in self.upload_time:
        #    self.upload_time = "TOP"


def fetch_page(url):
    """ """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "Host": "www.ebay-kleinanzeigen.de",
        "Accept": "*/*",
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        return None


def is_valid_listing(tag):
    """ """
    return tag.find("a") is not None


def parse_page(content):
    """ """
    soup = bs4.BeautifulSoup(content, "html.parser")

    ads = soup.find_all("li", class_="ad-listitem")
    #print(ads[0])
    #print("-" * 80)
    #print(ads[1])
    #print("-" * 80)

    return [AdListing(ad) for ad in ads if is_valid_listing(ad)]


def get_current_listings():
    """ """
    return parse_page(fetch_page(SEARCH_URL))


def main():
    resp = get_current_listings()
    print(len(resp))
    # print(parse_page(fetch_page(SEARCH_URL)))


if __name__ == "__main__":
    main()
