from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random


def delay(a=1.5, b=3.0):
    time.sleep(random.uniform(a, b))


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 20)

try:
    print("[INFO] Test Started")

    driver.get("https://authorized-partner.vercel.app/")
    driver.maximize_window()

    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    delay()

    print("[INFO] Page Loaded:", driver.title)

    buttons = driver.find_elements(By.TAG_NAME, "button")

    clicked = False
    for btn in buttons:
        try:
            text = btn.text.lower().strip()
            if "sign" in text or "register" in text or "get started" in text:
                driver.execute_script("arguments[0].click();", btn)
                clicked = True
                print("[STEP] Signup button clicked")
                break
        except:
            continue

    if not clicked:
        print("[WARNING] Signup button not found")

    delay(3, 5)

    wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "input")))
    inputs = driver.find_elements(By.TAG_NAME, "input")

    print("[STEP] Inputs Found:", len(inputs))

    for inp in inputs:
        try:
            t = inp.get_attribute("type")

            if t == "text":
                inp.send_keys("Manish")
            elif t == "email":
                inp.send_keys("test@gmail.com")
            elif t == "password":
                inp.send_keys("12345678")

            delay(0.5, 1.2)

        except:
            continue

    print("[ACTION] Form Filled Successfully")

    submitted = False

    buttons = driver.find_elements(By.TAG_NAME, "button")
    for btn in buttons:
        try:
            if btn.is_displayed() and btn.is_enabled():
                driver.execute_script("arguments[0].click();", btn)
                submitted = True
                print("[ACTION] Form Submitted")
                break
        except:
            continue

    if not submitted:
        print("[ERROR] Submit button not found")

    delay(3, 5)

    final_url = driver.current_url
    print("[VERIFY] Final URL:", final_url)

    if "step=setup" in final_url or "register" in final_url:
        print("[RESULT] TEST PASSED")
    else:
        print("[RESULT] TEST FAILED")

    driver.save_screenshot("test_result.png")
    print("[INFO] Screenshot saved")

    print("[INFO] Test Completed")

except Exception as e:
    print("[ERROR] Test Failed:", str(e))
    driver.save_screenshot("error.png")

finally:
    driver.quit()