import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


# Setup Logging (Equivalent to Log4j)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler("test_log.log")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


# TestNG-like setup: BeforeClass & AfterClass
@pytest.fixture(scope="class", autouse=True)
def setup_class(request):
    logger.info("Initializing WebDriver and opening browser")
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run tests in headless mode
    service = Service("chromedriver")  # Path to chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    request.cls.driver = driver
    yield
    logger.info("Closing browser")
    driver.quit()


# TestNG-like setup: BeforeMethod & AfterMethod
@pytest.fixture(autouse=True)
def setup_method():
    logger.info("Starting a new test case")
    yield
    logger.info("Test case execution completed")


# Capture Screenshot on Failure
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.failed:
        driver = item.cls.driver
        screenshot_path = f"screenshots/{item.name}.png"
        driver.save_screenshot(screenshot_path)
        logger.error(f"Test failed. Screenshot saved at: {screenshot_path}")


# Testing Astana Hub Homepage
@pytest.mark.usefixtures("setup_class")
class TestAstanaHub:
    
    def test_homepage_title(self):
        self.driver.get("https://astanahub.com/")
        title = self.driver.title
        logger.info(f"Page Title: {title}")
        assert "Astana Hub" in title, "Title does not match"
    
    def test_navigation_bar(self):
        self.driver.get("https://astanahub.com/")
        nav_bar = self.driver.find_element(By.CLASS_NAME, "navigation")
        assert nav_bar.is_displayed(), "Navigation bar is not displayed"


# Generate HTML Report
def pytest_configure(config):
    config.option.htmlpath = "test_report.html"
