import logging  
from selenium import webdriver  
from selenium.webdriver.common.by import By  
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities  
from selenium.common.exceptions import WebDriverException 

from lavague.core import  WorldModel, ActionEngine
from lavague.core.agents import WebAgent
from lavague.drivers.selenium import SeleniumDriver
  
# Configure logging  
logging.basicConfig(level=logging.DEBUG)  
  
def main():  
    # Set up Chrome options  
    chrome_options = Options()  
    chrome_options.add_argument("--headless")  # Run in headless mode  
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration  
    chrome_options.add_argument("--no-sandbox")  # Add no-sandbox argument  
    chrome_options.add_argument("--disable-dev-shm-usage")  # Add disable-dev-shm-usage argument  
  

  
    # Set up the remote WebDriver  
    browserless_url = "http://localhost:3000/webdriver"  
  
    try:  
        driver = webdriver.Remote(  
            command_executor=browserless_url,
            options=chrome_options
        )  
        return driver
  
    except WebDriverException as e:  
        logging.error(f"WebDriverException: {e}")  
    except Exception as e:  
        logging.error(f"Exception: {e}")  
    finally:  
        if 'driver' in locals():  
            driver.quit()  
  
if __name__ == "__main__":  
    driver = main()  #None

    selenium_driver = SeleniumDriver(headless=False)
    world_model = WorldModel()
    action_engine = ActionEngine(driver)
    agent = WebAgent(world_model, action_engine)
    agent.get("https://huggingface.co/docs")
    agent.run("Go on the quicktour of PEFT")