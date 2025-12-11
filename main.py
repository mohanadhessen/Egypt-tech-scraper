from db_product_updater import get_most_searched , add_to_database
from scraping_modules.sigma import sigma_scraper
from scraping_modules.elnekhely import elnekhely_scraper
from scraping_modules.compumarts import compumarts_scraper
from scraping_modules.elbadrgroupeg import elbadrgroupeg_scraper
from data_formater import formater
import logging


logging.basicConfig(level=logging.INFO)



def merging_data(product_name):
    """
    Run all scrapers for a product and merge results into a single list.
    """
    return (
        sigma_scraper(product_name) +
        elnekhely_scraper(product_name) +
        compumarts_scraper(product_name) +
        elbadrgroupeg_scraper(product_name)
    )


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




