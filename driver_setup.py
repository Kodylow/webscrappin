from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from config import path


def setup_driver():
    service = Service(executable_path=path)
    options = ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    return driver
