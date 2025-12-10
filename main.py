from db_product_updater import get_most_searched , add_to_database
from scraping_modules.elnekhely import elnekhely
from scraping_modules.elbadrgroupeg import elbadrgroupeg
from scraping_modules.compumarts import compumarts
from scraping_modules.sigma import sigma
from scraping_modules.scraper_base import BaseScraper
from data_formater import formater
import logging
logging.basicConfig(level=logging.INFO)


sigma_scraper = BaseScraper()
elnekhely_scraper = BaseScraper()
compumarts_scraper = BaseScraper()
elbadrgroupeg_scraper = BaseScraper()

def merging_data(product):
    sigma_scraper.run_threads(product)
    elnekhely_scraper.run_threads(product)
    compumarts_scraper.run_threads(product)
    elbadrgroupeg_scraper.run_threads(product)
    return sigma_scraper.data + elnekhely_scraper.data + compumarts_scraper.data + elbadrgroupeg_scraper.data


def schedule():
    try :   
        most_searched = get_most_searched()
        for product in most_searched:
            logging.info(f"product name currently begin scraped {product['product_name']}")
            add_to_database(merging_data(product['product_name']))
        logging.info('✅ finished scraping all product')
    
    except Exception as e:
        logging.error(f'thier wasa an error as {e}')
        


if __name__ == "__main__":
    schedule()