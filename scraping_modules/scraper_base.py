import requests
from bs4 import BeautifulSoup
import time
import random
from threading import Thread
import logging


class BaseScraper:
    def __init__(self):
        self.data = []
        self.signal = True

    
    def fetch_page(self, url, retries):
        for i in range(retries):
            try:
                logging.info(f"Attempt {i+1} of {retries} for URL: {url}")
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                logging.info(f"Successfully fetched page for URL: {url}")
                soup = BeautifulSoup(response.text, 'html.parser')

                if soup.select_one("div.up-challenge-container"):
                    logging.error(f"Cloudflare Turnstile detected for URL: {url} (Attempt {i+1})")
                    break 
                return soup
            
            except requests.exceptions.HTTPError as e:
                status = e.response.status_code
                if status == 404:
                    logging.error(f"Error 404: Page not found for URL: {url} (Attempt {i+1})")
                    break
                elif status == 500:
                    logging.error(f"Error 500: Server error for URL: {url} (Attempt {i+1})")
                    time.sleep(5)
                elif status == 403:
                    logging.error(f"Error 403: Forbidden access for URL: {url} (Attempt {i+1})")
                    break
                else:
                    logging.error(f"HTTP error {status} for URL: {url} (Attempt {i+1})")
                    time.sleep(2)
            
            except requests.exceptions.RequestException as e:
                logging.warning(f"Network error on attempt {i+1}: {e}")
                if i == retries // 2:
                    time.sleep(60)
                time.sleep(1)
            
            except Exception as e:
                logging.error(f"Unknown error on attempt {i+1}: {e}")
    
    

    def run_threads(self,function,product_name,page_number = 1):
        while self.signal:
            threads = []
            for i in range(page_number,page_number+5):
                threads.append(Thread(target=function,args=(product_name,i)))
            for t in threads:
                t.start()
            for t in threads:
                t.join(timeout=30)

            page_number+=5
            time.sleep(random.uniform(3,5))




