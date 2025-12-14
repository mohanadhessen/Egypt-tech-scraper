from .scraper_base import BaseScraper
import logging


def sigma_scraper(product_name):
    scraper = BaseScraper()

    def sigma(product_name, page_number):
        logging.info(f"🔍 Scraping sigma page {page_number} for '{product_name}'")
        try:
            # Build the URL for the current page
            url = f"https://www.sigma-computer.com/en/search?q={product_name}&pageSize=50&page={page_number}"
            
            # Fetch and parse the page
            soup = scraper.fetch_page(url, 10)
            if not soup:
                logging.warning(f"Failed to fetch page {page_number} for product '{product_name}'")
                scraper.signal = False
                return

            # Select all product items
            items = soup.select('div.px-2.md\\:px-4.py-1.md\\:py-2')
            if not items:
                scraper.signal = False
                return

            for item in items:
                try :
                    info = item.select_one("a.chakra-tooltip__trigger.line-clamp-2.w-fit.font-semibold.dark\\:text-sigma-blue-50.text-sm.md\\:text-base")
                    title = info.text
                    link = "https://www.sigma-computer.com/" + info.get('href')
                    price = item.select_one("p.font-bold.text-sigma-blue-600").text
                    
                    # Determine stock status
                    in_stock = True
                    badges_container = item.select_one("div#badges-container")
                    if badges_container and "out of stock" in badges_container.get_text(strip=True).lower():
                        in_stock = False
    
                    # Append product data
                    scraper.data.append({
                        "title": title,
                        "price": price,
                        "link": link,
                        "in_stock": in_stock,
                        'store': 'sigma'
                    })
                except Exception as e:
                    logging.error(f"there was an error in getting the info as {e}")
                    continue
                
            logging.info(f"✅ Finished scraping sigma page {page_number}")
    
        except Exception as e:
            logging.error(f"❌ sigma scraper failed on page {page_number}: {e}")
            scraper.signal = False
            return
    
    # Run scraping function in threads
    scraper.run_threads(sigma, product_name)
    return scraper.data


