import mysql.connector
import logging
import os
from dotenv import find_dotenv, load_dotenv

# Load environment variables (works both locally and in GitHub Actions)
dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)

def add_to_database(data):
    logging.info('💾 adding to database...')
    try:
        # Connect to MySQL database
        db = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT', 3306)),  # Default MySQL port
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            database=os.getenv('DB_NAME'),
            ssl_disabled=False,
            autocommit=True  # Auto-commit transactions
        )
        mycursor = db.cursor(dictionary=True)

        for product in data:
            title = product['title']
            price = product['price']
            link = product['link']
            in_stock = product['in_stock']
            store = product['store']

            try:
                # Insert new product
                query = 'INSERT INTO products_info (title, price, link, in_stock, store) VALUES (%s, %s, %s, %s, %s)'
                mycursor.execute(query, (title, price, link, in_stock, store))

            except mysql.connector.Error as e:
                if e.errno == 1062:
                    # Duplicate: check if price or stock changed
                    mycursor.execute('SELECT id, price, in_stock FROM products_info WHERE link = %s', (link,))
                    result = mycursor.fetchone()
                    if result:  # Check if result exists
                        product_id = result['id']
                        old_price = result['price']
                        old_in_stock = result['in_stock']
                        new_price = price
                        new_in_stock = in_stock

                        # Update price if changed
                        if old_price != new_price:
                            mycursor.execute(
                                'INSERT INTO price_history (product_id, old_price, new_price) VALUES (%s, %s, %s)',
                                (product_id, old_price, new_price)
                            )
                            mycursor.execute('UPDATE products_info SET price = %s WHERE id = %s', (new_price, product_id))

                        # Update stock if changed
                        if old_in_stock != new_in_stock:
                            mycursor.execute('UPDATE products_info SET in_stock = %s WHERE id = %s', (new_in_stock, product_id))
                else:
                    logging.error(f'Database error: {e}')

        db.close()
        logging.info('✅ finished adding to database')

    except Exception as e:
        logging.error(f'Error connecting to the database: {e}')
        raise  # Re-raise to fail the GitHub Action if DB connection fails


def get_most_searched():
    logging.info('🔍 searching from database...')
    try:
        db = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT', 3306)),  
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            database=os.getenv('DB_NAME'),
            ssl_disabled=False
        )
        mycursor = db.cursor(dictionary=True)
        query = "SELECT token, total_count FROM tokens ORDER BY total_count DESC LIMIT 10"
        mycursor.execute(query)
        results = mycursor.fetchall()
        db.close()
        logging.info('✅ Finished querying database')
        return results

    except Exception as e:
        logging.error(f'Error connecting to the database: {e}')
        raise  # Re-raise to fail the GitHub Action if DB connection fails




