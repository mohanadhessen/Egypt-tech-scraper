import requests
from bs4 import BeautifulSoup
import time
import random
from threading import Thread
import logging

# Configure logging at the start of the module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BaseScraper:
    def __init__(self):
        # Store scraped data
        self.data = []
        # Control flag for running threads
        self.signal = True

    def fetch_page(self, url, retries):
        """
        Fetch a web page and return BeautifulSoup object.
        Handles retries and common HTTP errors.
        Detects Cloudflare Turnstile pages.
        """
        for i in range(retries):
            try:
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

                # Detect Cloudflare Turnstile
                if soup.select_one("div.up-challenge-container"):
                    logging.error(f"Cloudflare Turnstile detected for URL: {url} (Attempt {i+1})")
                    break 
                
                return soup
            
            except requests.exceptions.HTTPError as e:
                status = e.response.status_code
                # Handle specific HTTP status codes
                match status:
                    case 404:
                        logging.error(f"Error 404: Page not found for URL: {url} (Attempt {i+1})")
                        break
                    case 500:
                        logging.error(f"Error 500: Server error for URL: {url} (Attempt {i+1})")
                        time.sleep(5)
                    case 403:
                        logging.error(f"Error 403: Forbidden access for URL: {url} (Attempt {i+1})")
                        break
                    case _:
                        logging.error(f"HTTP error {status} for URL: {url} (Attempt {i+1})")
                        time.sleep(2)
            
            except requests.exceptions.RequestException as e:
                # Catch network-related errors
                logging.warning(f"Network error on attempt {i+1}: {e}") 
                # If halfway through retries, wait longer
                if i == retries // 2:
                     time.sleep(60) 
                time.sleep(1)
            
            except Exception as e:
                # Catch-all for unexpected errors
                logging.error(f"Unknown error on attempt {i+1}: {e}")

    def run_threads(self, function, product_name, page_number=1):
        """
        Run a function in threads over multiple pages.
        Continues until self.signal is set to False.
        """
        while self.signal:
            threads = []
            # Launch 5 threads for consecutive pages
            for i in range(page_number, page_number + 5):
                threads.append(Thread(target=function, args=(product_name, i)))
            
            # Start all threads
            for t in threads:
                t.start()
            
            # Join threads with timeout to avoid blocking indefinitely
            for t in threads:
                t.join(timeout=30)

            # Move to next batch of pages
            page_number += 5
            # Random sleep to mimic human behavior and avoid rate limiting
            time.sleep(random.uniform(3, 5))