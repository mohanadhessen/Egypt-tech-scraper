import logging




def elnekhely(scraper,product_name, page_number):
    logging.info('🔍 scraping elnekhely...')
    
    try:
        # Construct the search URL with product name and current page number
        url = f"https://www.elnekhelytechnology.com/index.php?route=product/search&search={product_name}&page={page_number}"
        soup = scraper.fetch_page(url,10)
        if soup is None:
            scraper.signal = False
            raise Exception("fetch_page failed")
        
        items = soup.select(".main-products .product-layout")
        if not items:
            scraper.signal = False
            return


        for item in items:
            # title
            title_el = item.select_one(".name a")
            title = title_el.get_text(strip=True) if title_el else None

            # link
            link = title_el.get("href") if title_el else None

            # price
            price_el = item.select_one("span.price-normal, span.price-new")
            price = price_el.get_text(strip=True) if price_el else None
            labels = item.select_one('div.product-labels')
            in_stock = True
            if labels:
                spans =  item.select_one('div.product-labels').select('span')
                for span in spans:
                    if span.text.strip().lower() == "out of stock" or span.text.strip().lower() == "coming soon":
                        in_stock = False
                        break


            scraper.data.append({
                "title": title,
                "price": price,
                "link": link,
                "in_stock": in_stock,
                'store': 'elnekhely'
            })
        print(f"scrapering elnekhely page {page_number} ")
        
    except Exception as e:
        logging.error(f'❌ elnekhely scraper failed: {e}')
        scraper.signal = False

    


