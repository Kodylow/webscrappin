import csv
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from driver_setup import setup_driver
from custom_wait import at_least_n_elements_found
from model import P2PDataRow

logging.basicConfig(level=logging.INFO)


def scrape_binance_p2p_website(website):
    driver = setup_driver()
    driver.get(website)

    wait = WebDriverWait(driver, 10)
    data = []

    logging.info("Starting Binance Scrape pages...")
    logging.info("Straping Buy pages...")
    scrape_pages(driver, wait, data, "Buy")
    logging.info("Buy pages complete.")

    try:
        sell_button = driver.find_element(
            By.CSS_SELECTOR, 'div.css-39cg0g div[data-bn-type="text"]'
        )
    except NoSuchElementException:
        logging.info("No Sell button found, skipping Sell pages.")
        return data

    sell_button.click()
    time.sleep(1)  # Wait for the page to load

    logging.info("Starting to scrape Sell pages...")
    scrape_pages(driver, wait, data, "Sell")
    logging.info("Scraping of Sell pages complete.")

    return data


def scrape_pages(driver, wait, data, page_type):
    while True:
        try:
            rows = wait.until(
                at_least_n_elements_found((By.CSS_SELECTOR, ".css-r9lvvx"), 1)
            )
        except:
            logging.info("No rows found on this page.")
            break
        for row in rows:
            extract_data(data, row, page_type)

        next_page_button = driver.find_element(By.CSS_SELECTOR, "button#next-page")
        if next_page_button.get_attribute("disabled"):
            logging.info("Next page button is disabled, we are on the last page.")
            break
        else:
            next_page_button.click()
            time.sleep(1)  # Wait for the next page to load


def extract_data(data, row, page_type):
    advertiser = row.find_element(By.CSS_SELECTOR, ".css-14xbj8l").text

    trade_partner_info = row.find_element(
        By.CSS_SELECTOR, ".css-1rxaqb6 a"
    ).get_attribute("href")
    try:
        row.find_element(
            By.CSS_SELECTOR,
            'img[src="https://bin.bnbstatic.com/static/images/c2c/authentication_icon.svg"]',
        )
        merchant_badge = True
    except NoSuchElementException:
        merchant_badge = False
    try:
        row.find_element(
            By.CSS_SELECTOR,
            'img[src="https://bin.bnbstatic.com/static/images/c2c/shield_badge.svg"]',
        )
        shield_badge = True
    except NoSuchElementException:
        shield_badge = False
    price = row.find_element(By.CSS_SELECTOR, ".css-onyc9z").text
    currency = row.find_element(By.CSS_SELECTOR, ".css-1cjl26j").text
    orders = row.find_element(By.CSS_SELECTOR, ".css-s3l2jm").text
    completion = row.find_elements(By.CSS_SELECTOR, ".css-s3l2jm")[1].text
    available = row.find_element(By.CSS_SELECTOR, ".css-vurnku").text
    limit = " - ".join(
        [
            elem.text.replace("\n", " ").replace("\r", "")
            for elem in row.find_elements(By.CSS_SELECTOR, ".css-aq7mev .css-4cffwv")
        ]
    )
    payment = [
        elem.text
        for elem in row.find_elements(By.CSS_SELECTOR, ".PaymentMethodItem__text")
    ]

    data_row = P2PDataRow(
        advertiser,
        page_type,
        trade_partner_info,
        merchant_badge,
        shield_badge,
        price,
        currency,
        orders,
        completion,
        available,
        limit,
        payment,
    )

    data.append(data_row)
