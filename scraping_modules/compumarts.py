import logging





def compumarts(scraper,product_name, page_number):
    logging.info('scraping compumarts...')

    try:
        url = f"https://www.compumarts.com/search?options[prefix]=last&page={page_number}&q={product_name}"

        soup = scraper.fetch_page(url, 10)
        if soup is None:
            scraper.signal = False
            raise Exception("fetch_page failed")

        items = soup.select("div.main-products-grid__results li")
        if not items:
            scraper.signal = False
            return

        for item in items:

            # title
            title_el = item.select_one(".card__title a")
            title = title_el.get_text(strip=True) if title_el else None

            # link
            link = "https://www.compumarts.com/" + title_el.get("href") if title_el else None

            # price
            price_el = item.select_one(".price__current .js-value")
            price = price_el.get_text(strip=True) if price_el else None

            # Default to in stock unless "Sold out" is found
            in_stock = True
            label_container = item.select_one("span.product-label--sold-out")
            if label_container:
                in_stock = False


            scraper.data.append({
                "title": title,
                "price": price,
                "link": link,
                "in_stock": in_stock,
                "store": "compumarts"
            })

        print(f'finished scraping this page {page_number}')

    except Exception as e:
        logging.error(f'compumarts scraper failed: {e}')
        scraper.signal = False




