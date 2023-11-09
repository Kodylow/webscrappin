from binance_p2p_scraper import scrape_binance_p2p_website
from advertiser_scraper import scrape_advertiser_pages
from config import website, fiats
from model import fieldnames
import logging
import csv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)

if __name__ == "__main__":
    with open("data.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    total_fiats = len(fiats)
    for index, fiat in enumerate(fiats):
        logging.info(f"Scraping {website + fiat}... ({index+1}/{total_fiats})")
        data = scrape_binance_p2p_website(website + fiat)
        scrape_advertiser_pages(data)
