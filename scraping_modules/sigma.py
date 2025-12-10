import logging




def sigma(scraper,product_name, page_number):
    try:
        url = f"https://www.sigma-computer.com/en/search?q={product_name}&pageSize=50&page={page_number}"
        
        soup = scraper.fetch_page(url,10)

        items = soup.select('div.px-2.md\\:px-4.py-1.md\\:py-2')
        if not items:
            print(f"there was no items in page : {page_number}")
            scraper.signal = False
            raise
        
        for item in items:
            price_el = item.select_one("p.font-bold.text-\\[\\#026EB3\\]")
            price = price_el.get_text(strip=True) if price_el else None
        

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
        
            in_stock = True
            badges_container = item.select_one("div#badges-container")
            if badges_container and "out of stock" in badges_container.get_text(strip=True).lower():
                in_stock = False
        
            scraper.data.append({
                "title": title,
                "price": price,
                "link": link,
                "in_stock": in_stock,
                'store': 'sigma'
            })
        logging.info(f"scraping sigma current page {page_number}")
        
    except Exception as e:
        print(e) 
        scraper.signal = False




