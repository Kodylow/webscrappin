from model import P2PDataRow
from typing import List
from driver_setup import setup_driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from parsers import parse_header, parse_feedback, parse_stats
from model import UnifiedDataRow, fieldnames
import csv
import logging


def scrape_advertiser_pages(data: List[P2PDataRow]):
    driver = setup_driver()
    wait = WebDriverWait(driver, 3)

    for row in data:
        url = row.trade_partner_info
        driver.get(url)
        logging.info(f"Scraping {url}...")
        try:
            unified_data = parseAdvertiserRow(row, wait)
        except Exception as e:
            logging.error(f"Error parsing {url}: {e}")
            continue

        with open("data.csv", "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(unified_data.to_dict())

    driver.quit()


def parseAdvertiserRow(row: P2PDataRow, wait):
    if row.merchant_badge:
        return parseVerifiedMerchant(row, wait)
    else:
        return parseVerifiedUser(row, wait)


def parseVerifiedUser(row: P2PDataRow, wait):
    container = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "css-lvif0s"))
    )
    header_text = container.find_element(By.CLASS_NAME, "css-4cffwv").text.split("\n")
    feedback_text = container.find_element(By.CLASS_NAME, "css-ooxez").text.split("\n")
    stats_text = container.find_element(By.CLASS_NAME, "css-1tngqys").text.split("\n")

    return parseUnifiedDataRow(header_text, feedback_text, stats_text, row)


def parseVerifiedMerchant(row: P2PDataRow, wait):
    container = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "css-427vec"))
    )
    header_text = container.find_element(By.CLASS_NAME, "css-4cffwv").text.split("\n")
    feedback_text = container.find_element(By.CLASS_NAME, "css-xac401").text.split("\n")
    stats_text = container.find_element(By.CLASS_NAME, "css-1tngqys").text.split("\n")

    return parseUnifiedDataRow(header_text, feedback_text, stats_text, row)


def parseUnifiedDataRow(header_text, feedback_text, stats_text, row):
    header = parse_header(header_text)
    feedback = parse_feedback(feedback_text)
    stats = parse_stats(stats_text)

    unified_data = UnifiedDataRow(
        row.advertiser,
        row.page_type,
        row.trade_partner_info,
        row.merchant_badge,
        row.shield_badge,
        row.price,
        row.currency,
        row.orders,
        row.completion,
        row.available,
        row.limit,
        row.payment,
        header.name,
        header.last_seen,
        header.joined_on,
        feedback.positive_feedback,
        feedback.total_feedback,
        feedback.positive,
        feedback.negative,
        stats.all_trades,
        stats.buy_sell_ratio,
        stats.buy,
        stats.sell,
        stats._30d_trades,
        stats._30d_completion_rate,
        stats.avg_release_time,
        stats.avg_pay_time,
    )

    return unified_data
