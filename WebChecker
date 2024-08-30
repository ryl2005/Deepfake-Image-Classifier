!pip install selenium
!pip install webdriver_manager
!pip install cloudscraper
!pip install requests beautifulsoup4 lxml requests-cache
import cloudscraper
from bs4 import BeautifulSoup
from itertools import cycle
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests_cache
import signal
import time

def CheckWebsite(input):
  list_image = []
  class TimeoutException(Exception):
    pass
  def timeout_handler(signum, frame):
    raise TimeoutException("timed out")
  signal.signal(signal.SIGALRM, timeout_handler)
  def scrape_with_cloudscraper(url):
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url, timeout=15)
    return response
  def scrape_with_selenium(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(15)
    driver.get(url)
    page_source = driver.page_source
    driver.quit()
    return page_source
  def scrape_with_proxies(url, proxies, user_agents):
    proxy_pool = cycle(proxies)
    user_agent_pool = cycle(user_agents)
    headers = {
        "User-Agent": next(user_agent_pool)
    }
    proxy = {
        "http": next(proxy_pool),
        "https": next(proxy_pool)
    }
    response = requests.get(url, headers=headers, proxies=proxy, timeout=15)
    return response
  def parse_webpage(content):
    soup = BeautifulSoup(content, "lxml")
    for image in soup.find_all('img'):
        list_image.append(image.get('src'))
  if __name__ == "__main__":
    requests_cache.install_cache('webpage_cache', backend='sqlite', expire_after=1800)
    url = input
    proxies = [
        "http://181.48.155.78:8003",
        "http://88.150.15.30:8080",
        "http://103.246.79.10:1111",
        "http://117.55.202.206:3128",
        "https://180.191.255.147:8081",
        "https://134.35.249.32:8080",
        "http://181.94.244.22:8080"
    ]
    user_agents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_15) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5392.175 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.4.263.6 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5367.208 Safari/537.36',
        'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5387.128 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.361675786808',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.361675786817',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.361675786823',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.361675786837',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.5.197.2 Safari/537.36'
    ]
    signal.alarm(120)
    try:
        start_time = time.time()
        response = scrape_with_cloudscraper(url)
        if response.status_code == 200:
            parse_webpage(response.content)
        else:
            print(f"Cloudscraper failed with status code {response.status_code}")
        elapsed_time = time.time() - start_time
        if elapsed_time >= 120:
            raise TimeoutException("timed out")
        page_source = scrape_with_selenium(url)
        parse_webpage(page_source)
        elapsed_time = time.time() - start_time
        if elapsed_time >= 120:
            raise TimeoutException("timed out")
        response = scrape_with_proxies(url, proxies, user_agents)
        if response.status_code == 200:
            parse_webpage(response.content)
        else:
            print(f"Proxies and rotating user agents failed with status code {response.status_code}")
    except TimeoutException as te:
        print(te)
        return list_image
    except Exception as e:
        print(f"An error occurred: {e}")
        return list_image
    finally:
        signal.alarm(0)
        return list_image

text = (CheckWebsite(str(input("Enter a url:"))))
image_list = []
for i in text:
  if i[0:4] == "http":
    image_list.append(i)
