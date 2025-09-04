from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
import logging


def build_driver(headless=True, user_data_dir=None):
    service = ChromeService(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    default_usser_data_dir = (
        Path.home() / ".cache" / "fck_aws_sso" / "user_data"
    )
    _user_data_dir = user_data_dir or default_usser_data_dir
    options.add_argument(f"user-data-dir={_user_data_dir}")
    if headless:
        options.add_argument("headless")
    return webdriver.Chrome(service=service, options=options)


def authorize_sso(url, code, headless=True, user_data_dir=None):
    driver = build_driver(headless, user_data_dir)
    url_with_code = f"{url}?user_code={code}"
    driver.get(url_with_code)
    logging.debug("Opening the page %s", url_with_code)

    try:
        logging.debug("Waiting for the page to load")
        submit_button = WebDriverWait(driver, 1000).until(
            EC.element_to_be_clickable((By.ID, "cli_verification_btn"))
        )
        logging.debug("Clicking on the verification button")
        submit_button.click()

        logging.debug("Waiting for the allow page to load")
        login_button = WebDriverWait(driver, 1000).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='allow-access-button']"))
        )
        
        logging.debug("Clicking on the allow button")
        login_button.click()

        logging.debug("Waiting for the confirmation page to load")

        xpath_expression = "//*[text()='You can close this window.' or text()='이 창을 닫을 수 있습니다.']"
        WebDriverWait(driver, 1000).until(
            EC.presence_of_element_located((By.XPATH, xpath_expression))
        )
        logging.debug("Done")

    except Exception as e:
        logging.error("An error occurred: %s", str(e))
    finally:
        driver.quit()
