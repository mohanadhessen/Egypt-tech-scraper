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
                scraper.signal = False
                return 
            
            # Select all product items
            items = soup.select(".main-products .product-layout")
            if not items:
                logging.info(f"No items found on page {page_number}")
                scraper.signal = False
                return

            for item in items:
                try :
                    title = item.select_one('div.name a').text
                    link = item.select_one('div.name a').get("href")
                    price = None
                    
                    price_spans = item.find('div', class_='price').find_all('span')
                    for span in price_spans:
                        span_class = span.get('class')[0]
                        if span_class in ['price-normal', 'price-new']:
                            price = span.text
                    print(price)
    
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
                except Exception as e:
                    logging.error(f"there was an error in getting the info as {e}")

            logging.info(f"✅ Finished scraping elnekhely page {page_number}")
    
        except Exception as e:
            logging.error(f"❌ elnekhely scraper failed on page {page_number}: {e}")
            scraper.signal = False
            return
    
    # Run scraping function in threads
    scraper.run_threads(elnekhely, product_name)
    return scraper.data







