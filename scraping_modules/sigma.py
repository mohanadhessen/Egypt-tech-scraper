import requests
from bs4 import BeautifulSoup
import logging
import time
import random

def sigma_scraper(product_name):
    logging.info('scraping sigma...')
    data = []
    page_number = 1

    while True:
        try:
            url = f"https://www.sigma-computer.com/en/search?q={product_name}&page={page_number}&pageSize=50"
            r = requests.get(url, timeout=40)
            soup = BeautifulSoup(r.text, "html.parser")

            # new product blocks
            items = soup.select('div.px-2.md\\:px-4.py-1.md\\:py-2')
            if not items:      # no more pages
                break

            for item in items:
                try:
                    # price
                    price_el = item.select_one("p.font-bold.text-\\[\\#026EB3\\]")
                    price = price_el.get_text(strip=True) if price_el else None

                    # title
                    title_el = item.select_one(
                        "a.chakra-tooltip__trigger.line-clamp-2.w-fit.font-semibold.dark\\:text-sigma-blue-50.text-sm.md\\:text-base"
                    )
                    title = title_el.get_text(strip=True) if title_el else None

                    # link
                    link = None
                    if title_el:
                        href = title_el.get("href")
                        if href:
                            link = "https://www.sigma-computer.com/" + href

                    # stock
                    in_stock = True
                    badges_container = item.select_one("div#badges-container")
                    if badges_container and "out of stock" in badges_container.get_text(strip=True).lower():
                        in_stock = False

                    data.append({
                        "title": title,
                        "price": price,
                        "link": link,
                        "in_stock": in_stock,
                        "store": "sigma"
                    })

                except Exception as e:
                    logging.warning(f"failed parsing product on page {page_number}: {e}")

            print(f"finished scraping page {page_number}")
            page_number += 1
            time.sleep(random.uniform(1, 3))

        except Exception as e:
            logging.error(f"sigma scraper failed: {e}")
            break

    logging.info('finished scraping sigma')
    return data
