from .scraper_base import BaseScraper
import logging

def sigma_scraper(product_name):
    scraper = BaseScraper()

    def sigma(product_name, page_number):
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
                logging.info(f"No items found on page {page_number}")
                scraper.signal = False
                return

            for item in items:
                # Extract price
                price_el = item.select_one("p.font-bold.text-\\[\\#026EB3\\]")
                price = price_el.get_text(strip=True) if price_el else None

                # Extract title
                title_el = item.select_one(
                    "a.chakra-tooltip__trigger.line-clamp-2.w-fit.font-semibold.dark\\:text-sigma-blue-50.text-sm.md\\:text-base"
                )
                title = title_el.get_text(strip=True) if title_el else None

                # Extract product link
                link = None
                if title_el:
                    href = title_el.get("href")
                    if href:
                        link = "https://www.sigma-computer.com/" + href

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

            logging.info(f"Scraped Sigma page {page_number} for '{product_name}'")

        except Exception as e:
            logging.error(f"Error scraping page {page_number} for '{product_name}': {e}")
            scraper.signal = False

    # Run scraping function in threads
    scraper.run_threads(sigma, product_name)
    
    return scraper.data