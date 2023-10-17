import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape product listings from Amazon
def scrape_product_listings(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    product_data = []
    for page in range(1, 21):  # Scraping 20 pages
        page_url = f"{url}&page={page}"
        response = requests.get(page_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        products = soup.find_all('div', {'data-component-type': 's-search-result'})
        for product in products:
            product_url = 'https://www.amazon.in' + product.find('a', {'class': 'a-link-normal'})['href']
            product_name = product.find('span', {'class': 'a-text-normal'}).text
            product_price_element = product.find('span', {'class': 'a-price-whole'})
            product_price = product_price_element.text if product_price_element else 'N/A'
            rating = product.find('span', {'class': 'a-icon-alt'})
            num_reviews = product.find('span', {'class': 'a-size-base', 'aria-label': True})

            rating = rating.text if rating else 'N/A'
            num_reviews = num_reviews.text if num_reviews else 'N/A'

            product_data.append([product_url, product_name, product_price, rating, num_reviews])

    return product_data

# URL to scrape
amazon_url = "https://www.amazon.in/s?k=bags&crid=2M096C6104MLT&qid=1653308124&sprefix=ba,aps%2C283&ref=sr_pg"

# Scrape product listings
product_listings = scrape_product_listings(amazon_url)

# Convert data to DataFrame
columns = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews']
product_df = pd.DataFrame(product_listings, columns=columns)

# Save the product listings to a CSV file
product_df.to_csv('product_listings.csv', index=False)




# Function to scrape product details from individual product pages
def scrape_product_details(url, headers):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    description = soup.find('div', {'id': 'productDescription'})
    asin = soup.find('th', text='ASIN').find_next('td').text.strip()
    manufacturer = soup.find('th', text='Manufacturer').find_next('td').text.strip()

    product_description = description.text.strip() if description else 'N/A'

    return asin, product_description, manufacturer

# Example usage in a loop
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Example list of product URLs
product_urls = ['https://example.com/product1', 'https://example.com/product2', ...]

product_details = []

for url in product_urls:
    asin, description, manufacturer = scrape_product_details(url, headers)
    product_details.append([url, description, asin, manufacturer])

# Now you can use product_details list as needed.


# Convert data to DataFrame
columns = ['Product URL', 'Description', 'ASIN', 'Manufacturer']
product_details_df = pd.DataFrame(product_details, columns=columns)

# Save the product details to a CSV file
product_details_df.to_csv('product_details.csv', index=False)
