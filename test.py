import requests
from bs4 import BeautifulSoup


response = requests.get('https://www.upwork.com/nx/search/jobs/?contractor_tier=1,2&from_recent_search=true&payment_verified=1&proposals=0-4,5-9&q=scraping&sort=recency')

response.raise_for_status()


print(response.text)