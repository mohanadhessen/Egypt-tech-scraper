from .scraper_base import BaseScraper
import logging


def elbadrgroupeg_scraper(product_name):
    scraper = BaseScraper()
    def elbadrgroupeg(product_name, page_number):
        """
        Scrape product data from Elbadr Group EG website for a given product name.
        Uses the provided BaseScraper instance.
        """
        logging.info(f"🔍 Scraping ElbadrGroupeG page {page_number} for '{product_name}'")
        
        try:
            # Build the URL for the current page
            url = f"https://elbadrgroupeg.store/index.php?route=product/search&search={product_name}&page={page_number}"
            
            # Fetch and parse the page
            soup = scraper.fetch_page(url, 10)
            if soup is None:
                scraper.signal = False
                return 
    
            # Select all product items
            items = soup.select(".main-products .product-layout")
            if not items:
                logging.info(f"No items found on page {page_number}")
                scraper.signal = False
                return
    
            for item in items:
                # Extract title
                title_el = item.select_one(".name a")
                title = title_el.get_text(strip=True) if title_el else None
    
                # Extract link
                link = title_el.get("href") if title_el else None
    
                # Extract price
                price_el = item.select_one("span.price-normal, span.price-new")
                price = price_el.get_text(strip=True) if price_el else None
    
                # Determine stock status
                in_stock = True
                labels = item.select_one('div.product-labels')
                if labels:
                    spans = labels.select('span')
                    for span in spans:
                        if span.text.strip().lower() in ["out of stock", "coming soon"]:
                            in_stock = False
                            break
    
                # Append product data
                scraper.data.append({
                    "title": title,
                    "price": price,
                    "link": link,
                    "in_stock": in_stock,
                    'store': 'elbadrgroupeg'
                })
    
            logging.info(f"✅ Finished scraping ElbadrGroupeG page {page_number}")
    
        except Exception as e:
            logging.error(f"❌ ElbadrGroupeG scraper failed on page {page_number}: {e}")
            scraper.signal = False
            return
    
    # Run scraping function in threads
    scraper.run_threads(elbadrgroupeg, product_name)
    return scraper.data







