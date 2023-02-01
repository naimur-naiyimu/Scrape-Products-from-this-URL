import csv
import requests
from bs4 import BeautifulSoup

HEADERS = ({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0',
    'Accept-Language': 'en-US, en;q=0.5'})

def scrape_amazon_products ( pages = 20 ):
    # create an empty list to store the scraped products
    products = []

    # loop through the desired number of pages
    for i in range (1, pages + 1):
        # make a GET request to the URL with the current page number
        response = requests.get (
            f"https://www.amazon.in/s?k=bags&page={i}&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1",headers = HEADERS)

        # parse the HTML content of the response
        soup = BeautifulSoup (response.content, "html.parser")

        # find all the products on the current page
        product_elements = soup.find_all ("div", class_ = "s-result-item")

        # loop through the product elements
        for product_element in product_elements:
            # extract the product URL, name, price, rating, and number of reviews

            product_url_element = product_element.find ("a", class_ = "a-link-normal")
            product_url = product_url_element ["href"] if product_url_element else ""

            product_name_element = product_element.find ("span", class_ = "a-size-medium a-color-base a-text-normal")
            product_name = product_name_element.text if product_name_element else ""

            product_price_element = product_element.find ("span", class_ = "a-offscreen")
            product_price = product_price_element.text if product_price_element else ""

            product_rating_element = product_element.find ("span", class_ = "a-icon-alt")
            product_rating = product_rating_element.text if product_rating_element else ""

            product_reviews_element = product_element.find ("div", class_ = "a-section a-text-normal")
            product_reviews = product_reviews_element.text if product_reviews_element else ""

            product = {"url": product_url.strip () if product_url else "",
                "name": product_name.strip () if product_name else "",
                "price": product_price.strip () if product_price else "",
                "rating": product_rating.strip () if product_rating else "",
                "reviews": product_reviews.strip () if product_reviews else "", }

            if product ["url"].strip () and product ["name"].strip () and product ["price"].strip ():
                products.append (product)

    return products
def scrape_product_details(product_url):
    # response = requests.get(product_url,headers = HEADERS)
    try:
        response = requests.get(product_url,headers = HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")

        description = soup.find("div", {"id": "productDescription"}).text.strip() if soup.find("div", {"id": "productDescription"}) else ""
        asin = soup.find("td", {"class": "a-size-medium a-color-secondary"}).text.strip() if soup.find("td", {"class": "a-size-medium a-color-secondary"}) else ""
        manufacturer = soup.find("a", {"id": "bylineInfo"}).text.strip() if soup.find("a", {"id": "bylineInfo"}) else ""

        return {
            "description": description,
            "asin": asin,
            "manufacturer": manufacturer,
        }
    except requests.exceptions.MissingSchema as e:
        # log the error or print it to the console
        print(f"Error: {e}")
        # continue  # continue with the next product URL
    
    return {}
    

def save_to_csv(products):
    with open("products.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["url", "name", "price", "rating", "reviews", "description", "asin", "manufacturer"])
        writer.writeheader()
        for product in products:
            product_details = scrape_product_details(product["url"])
            product.update(product_details)
            writer.writerow(product)

products = scrape_amazon_products(20)
save_to_csv(products)
