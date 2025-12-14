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
            items = soup.select("div.main-products-grid__results li product-card")
            if not items:
                scraper.signal = False
                return
    
            for item in items:
                try :
                    # Extract title
                    title = item.select_one('p.card__title a').text
                    
                    # # Extract link
                    link = "https://www.compumarts.com/" + item.select_one('p.card__title a').get('href')
        
                    
                    # # Extract price
                    price = item.select_one(".price__current .js-value").text

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
                except Exception as e:
                    logging.error(f"there was an error in getting the info as {e}")
                    continue
    
            logging.info(f"✅ Finished scraping compumarts page {page_number}")
    
        except Exception as e:
            logging.error(f"❌ compumarts scraper failed on page {page_number}: {e}")
            scraper.signal = False
            return
    
    # Run scraping function in threads
    scraper.run_threads(compumarts, product_name)
    return scraper.data






