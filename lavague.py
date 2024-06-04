import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

from lavague.core import WorldModel, ActionEngine
from lavague.core.agents import WebAgent
from lavague.drivers.selenium import SeleniumDriver
from lavague.contexts.openai import AzureOpenaiContext

# Configure logging
logging.basicConfig(level=logging.DEBUG)


class CustomSeleniumDriver(SeleniumDriver):
    def __init__(self, driver, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver = driver


def main():
    # Set up Chrome options
    chrome_options = Options()
    # Comment out headless option to see the browser activity
    # chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--no-sandbox")  # Add no-sandbox argument
    chrome_options.add_argument(
        "--disable-dev-shm-usage"
    )  # Add disable-dev-shm-usage argument

    # Set up the remote WebDriver to connect to the Selenium Docker container
    selenium_url = "http://51.8.84.12:4444/wd/hub"  # Replace with your VM's IP address

    try:
        driver = webdriver.Remote(command_executor=selenium_url, options=chrome_options)
        return driver

    except WebDriverException as e:
        logging.error(f"WebDriverException: {e}")
    except Exception as e:
        logging.error(f"Exception: {e}")


if __name__ == "__main__":
    driver = main()
    if not driver:
        raise RuntimeError("Failed to initialize WebDriver")

    context = AzureOpenaiContext()
    context.mm_llm = AzureOpenaiContext().mm_llm

    selenium_driver = CustomSeleniumDriver(driver=driver, headless=False)
    world_model = WorldModel.from_context(context)
    action_engine = ActionEngine.from_context(context, selenium_driver)
    agent = WebAgent(world_model, action_engine)

    try:
        agent.get("https://huggingface.co/docs")
        agent.run("Go on the quicktour of PEFT")
    finally:
        driver.quit()
