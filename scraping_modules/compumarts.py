from .scraper_base import BaseScraper
import logging



def compumarts_scraper(product_name):
    scraper = BaseScraper()
    def compumarts(product_name, page_number):
        """
        Scrape product data from Compumarts website for a given product name.
        Uses the provided BaseScraper instance.
        """
        logging.info(f"🔍 Scraping Compumarts page {page_number} for '{product_name}'")
    
        try:
            # Build the URL for the current page
            url = f"https://www.compumarts.com/search?options[prefix]=last&page={page_number}&q={product_name}"
    
            # Fetch and parse the page
            soup = scraper.fetch_page(url, 10)
            if soup is None:
                scraper.signal = False
                raise Exception("fetch_page failed")
    
            # Select all product items
            items = soup.select("div.main-products-grid__results li")
            if not items:
                logging.info(f"No items found on page {page_number}")
                scraper.signal = False
                return
    
            for item in items:
                # Extract title
                title_el = item.select_one(".card__title a")
                title = title_el.get_text(strip=True) if title_el else None
    
                # Extract link
                link = "https://www.compumarts.com/" + title_el.get("href") if title_el else None
    
                # Extract price
                price_el = item.select_one(".price__current .js-value")
                price = price_el.get_text(strip=True) if price_el else None
    
                # Determine stock status
                in_stock = True
                label_container = item.select_one("span.product-label--sold-out")
                if label_container:
                    in_stock = False
    
                # Append product data
                scraper.data.append({
                    "title": title,
                    "price": price,
                    "link": link,
                    "in_stock": in_stock,
                    "store": "compumarts"
                })
    
            logging.info(f"✅ Finished scraping Compumarts page {page_number}")
    
        except Exception as e:
            logging.error(f"❌ Compumarts scraper failed on page {page_number}: {e}")
            scraper.signal = False

    # Run scraping function in threads
    scraper.run_threads(compumarts, product_name)
    
    return scraper.data



