import json
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from driver_setup import setup_driver
from custom_wait import at_least_n_elements_found
from config import website
from model import P2PDataRow


def scrape_website():
    driver = setup_driver()
    driver.get(website)
    driver.set_window_size(400, 800)
    wait = WebDriverWait(driver, 30)
    data = []

    while True:
        rows = wait.until(
            at_least_n_elements_found((By.CSS_SELECTOR, ".css-r9lvvx"), 1)
        )
        for row in rows:
            extract_data(data, row)

        # Print the scraped data
        for item in data:
            print(json.dumps(item, indent=2))

        next_page_button = driver.find_element(By.CSS_SELECTOR, "button#next-page")
        if next_page_button.get_attribute("disabled"):
            # The "Next page" button is disabled, we're on the last page
            break
        else:
            print("Clicking the next page button")
            next_page_button.click()
            time.sleep(1)  # Wait for the next page to load
            print("Current data length:", len(data))


def extract_data(data, row):
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
            elem.text
            for elem in row.find_elements(By.CSS_SELECTOR, ".css-aq7mev .css-4cffwv")
        ]
    )
    payment = [
        elem.text
        for elem in row.find_elements(By.CSS_SELECTOR, ".PaymentMethodItem__text")
    ]

    data_row = P2PDataRow(
        advertiser,
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
