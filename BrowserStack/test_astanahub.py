import pytest
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os

load_dotenv()

# BrowserStack credentials
BROWSERSTACK_USERNAME = os.getenv('BROWSERSTACK_USERNAME')
BROWSERSTACK_ACCESS_KEY = os.getenv('BROWSERSTACK_ACCESS_KEY')

# Read test data from Excel
def get_test_data(sheet_name):
    workbook = openpyxl.load_workbook("task6/test_data.xlsx")
    sheet = workbook[sheet_name]
    data = [row[0] for row in sheet.iter_rows(min_row=2, values_only=True)]
    return data

# BrowserStack capabilities using RemoteOptions
@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.set_capability("browserName", "Chrome")
    options.set_capability("browserVersion", "latest")
    options.set_capability("bstack:options", {
        "os": "Windows",
        "osVersion": "10",
        "sessionName": "Astana Hub Tests"
    })
    
    driver = webdriver.Remote(
        command_executor=f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub",
        options=options
    )
    yield driver
    driver.quit()

# Test 1: Verify homepage title
def test_homepage_title(driver):
    driver.get("https://astanahub.com/")
    assert "astana_hub - Digital technopark" in driver.title, "Homepage title does not match!"

# Test 2: Verify main elements on homepage
def test_homepage_elements(driver):
    driver.get("https://astanahub.com/")
    
    # Check if logo exists
    logo = driver.find_element(By.CLASS_NAME, "header-logo")
    assert logo.is_displayed(), "Logo is missing!"

    # Check if search bar exists
    search_bar = driver.find_element(By.CLASS_NAME, "search-input")
    assert search_bar.is_displayed(), "Search bar is missing!"

# Test 3: Search functionality
@pytest.mark.parametrize("search_term", get_test_data("Search"))
def test_search(driver, search_term):
    driver.get("https://astanahub.com/")
    search_box = driver.find_element(By.CLASS_NAME, "search-input") 
    search_box.send_keys(search_term + Keys.RETURN)

    results = driver.find_elements(By.CLASS_NAME, "search-res-block")
    assert len(results) > 0, f"No results found for '{search_term}'!"
