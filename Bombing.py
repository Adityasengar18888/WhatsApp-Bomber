from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Configuration
PHONE_NUMBER = "+91**********"  # With country code
MESSAGE_TEXT = "...."  #MESSAGE TO SEND
CHROME_PROFILE_PATH = os.path.join(os.getcwd(), "WhatsAppSession")
MESSAGE_COUNT = 100 # Number of times to send the message
DELAY_BETWEEN_MESSAGES = 3 # Seconds between messages

def setup_driver():
    """Configure Chrome with maximum stability options"""
    options = webdriver.ChromeOptions()
    
    # Critical stability options
    options.add_argument(f"--user-data-dir={CHROME_PROFILE_PATH}")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Memory management
    options.add_argument("--memory-pressure-off")
    options.add_argument("--disable-backgrounding-occluded-windows")
    
    # Fix for Chrome crashes
    options.add_argument("--remote-debugging-port=9222")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    # Auto-install ChromeDriver
    service = Service(ChromeDriverManager().install())
    service.start_timeout = 30
    service.creationflags = 0x08000000  # CREATE_NO_WINDOW flag
    
    return webdriver.Chrome(service=service, options=options)

def whatsapp_login(driver):
    """Handle WhatsApp Web login with robust waiting"""
    driver.get("https://web.whatsapp.com")
    
    print("Please scan QR code within 45 seconds...")
    try:
        WebDriverWait(driver, 45).until(
            lambda d: d.find_elements(By.XPATH, '//div[@aria-label="Chat list"]') or
                     d.find_elements(By.XPATH, '//div[@aria-label="Scan me"]')
        )
        
        if driver.find_elements(By.XPATH, '//div[@aria-label="Scan me"]'):
            print("QR code not scanned in time")
            return False
            
        print("Login successful!")
        return True
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        return False

def send_message(driver, phone, message, attempt_count):
    """Send message with multiple fallback attempts"""
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            print(f"\nSending message {attempt_count}...")
            driver.get(f"https://web.whatsapp.com/send?phone={phone}")
            
            input_xpaths = [
                '//div[@contenteditable="true"][@data-tab="10"]',
                '//div[@contenteditable="true"][@data-tab="9"]',
                '//div[@role="textbox"]'
            ]
            
            input_box = None
            for xpath in input_xpaths:
                try:
                    input_box = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, xpath))
                    )
                    break  # Proper placement of break
                except:
                    continue
            
            if not input_box:
                raise Exception("Could not find message input box")
            
            input_box.clear()
            input_box.send_keys(f"{message} ({attempt_count})" + Keys.ENTER)
            time.sleep(2)
            
            print(f"Message {attempt_count} sent successfully!")
            return True
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            time.sleep(5)
    
    print(f"Failed after {max_attempts} attempts")
    return False

def main():
    # Create profile directory if it doesn't exist
    if not os.path.exists(CHROME_PROFILE_PATH):
        os.makedirs(CHROME_PROFILE_PATH)
    
    print("Initializing Chrome...")
    driver = None
    try:
        driver = setup_driver()
        driver.set_page_load_timeout(60)
        
        if whatsapp_login(driver):
            for i in range(1, MESSAGE_COUNT + 1):
                if not send_message(driver, PHONE_NUMBER, MESSAGE_TEXT, i):
                    print("Stopping due to repeated failures")
                    break
                
                if i < MESSAGE_COUNT:
                    print(f"Waiting {DELAY_BETWEEN_MESSAGES} seconds...")
                    time.sleep(DELAY_BETWEEN_MESSAGES)
            
            print("\nMessage sending completed!")
        else:
            print("WhatsApp login failed")
            
    except Exception as e:
        print(f"Fatal error: {str(e)}")
    finally:
        if driver:
            print("\nClosing browser...")
            driver.quit()
            print("Browser closed successfully.")

if __name__ == "__main__":
    main()
