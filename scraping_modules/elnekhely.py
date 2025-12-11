from .scraper_base import BaseScraper
import logging



def elnekhely_scraper(product_name):
    """
    Scrape product data from Elnekhely Technology website for a given product name.
    Uses BaseScraper and runs multiple pages concurrently.
    """
    scraper = BaseScraper()

    def elnekhely(product_name, page_number):
        logging.info(f"🔍 Scraping Elnekhely page {page_number} for '{product_name}'")
        
        try:
            # Build the URL for the current page
            url = f"https://www.elnekhelytechnology.com/index.php?route=product/search&search={product_name}&page={page_number}"
            
            # Fetch and parse the page
            soup = scraper.fetch_page(url, 10)
            if soup is None:
                logging.warning(f"Failed to fetch page {page_number} for '{product_name}'")
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
                    'store': 'elnekhely'
                })

            logging.info(f"Scraped Elnekhely page {page_number} successfully")
            
        except Exception as e:
            logging.error(f"❌ Elnekhely scraper failed on page {page_number}: {e}")
            scraper.signal = False

    # Run scraping function in threads
    scraper.run_threads(elnekhely, product_name)
    return scraper.data


