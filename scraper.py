import requests
from bs4 import BeautifulSoup
import csv

def scrape_books():
    # 1. Define the target URL and User-Agent (to look like a real browser)
    url = 'http://books.toscrape.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print(f"Connecting to {url}...")
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return

    # 2. Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 3. Find all book containers on the page
    books = soup.find_all('article', class_='product_pod')
    scraped_data = []

    print(f"Found {len(books)} books. Extracting data...")

    # 4. Loop through each book and extract specific details
    for book in books:
        # Extract title
        title = book.h3.a['title']
        
        # Extract price
        price = book.find('p', class_='price_color').text
        
        # Extract stock availability and strip extra whitespace
        stock = book.find('p', class_='instock availability').text.strip()
        
        scraped_data.append([title, price, stock])

    # 5. Save the extracted data to a CSV file
    filename = 'books_data.csv'
    with open(filename, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Price', 'Availability']) # Write headers
        writer.writerows(scraped_data) # Write data rows

    print(f"Success! Data successfully saved to {filename}")

if __name__ == '__main__':
    scrape_books()