!pip install cloudscraper fake-useragent retrying

import os
from urllib.parse import urljoin, urlparse
import cloudscraper
from bs4 import BeautifulSoup
from retrying import retry
from fake_useragent import UserAgent

BASE_URL = str(input("Enter a url:"))
IMAGES_DIR = "downloaded_images"

if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

ua = UserAgent()
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'windows',
        'mobile': False
    }
)

@retry(stop_max_attempt_number=5, wait_fixed=2000)
def fetch_url(url):
    headers = {
        'User-Agent': ua.random
    }
    response = scraper.get(url, headers=headers, timeout=15)
    response.raise_for_status()  
    return response

def is_absolute(url):
    return bool(urlparse(url).netloc)

def download_image(img_url, folder):
    filename = os.path.join(folder, os.path.basename(urlparse(img_url).path))
    try:
        img_data = fetch_url(img_url).content
        with open(filename, 'wb') as img_file:
            img_file.write(img_data)
        print(f"Downloaded {img_url} to {filename}")
    except Exception as e:
        print(f"Failed to download {img_url}: {e}")

def scrape_images_from_url(url):
    try:
        html_content = fetch_url(url).text
        soup = BeautifulSoup(html_content, 'lxml')
        
        img_tags = soup.find_all('img')
        
        for img in img_tags:
            img_url = img.get('src')
            if img_url:
                img_url = urljoin(BASE_URL, img_url) if not is_absolute(img_url) else img_url
                download_image(img_url, IMAGES_DIR)
                
    except Exception as e:
        print(f"Error scraping {url}: {e}")

def main():
    scrape_images_from_url(BASE_URL)

if __name__ == "__main__":
    main()

def clear_downloaded_images(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

#Use this to clear
if str(input("Would you like to clear data?(yes or no)")) == "yes":
  clear_downloaded_images(IMAGES_DIR)
