import time
import csv
import requests
from PIL import Image
import pytesseract
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def solve_captcha(img):
    # Set the Tesseract path (adjust if needed)
    path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    pytesseract.pytesseract.tesseract_cmd = path_to_tesseract
    whitelist = '1234567890QWERTYUIOPASDFGHJKLZXCVBNM'
    custom_config = f'--oem 3 -c tessedit_char_whitelist={whitelist}'
    text = pytesseract.image_to_string(img, config=custom_config)
    return text.strip()

def get_student_result(driver, roll_no, semester="5", max_attempts=5):
    website = "https://www.jecjabalpur.ac.in/exam/programselect.aspx"
    driver.get(website)
    time.sleep(2)  # Allow the page to load
    
    try:
        # Select the program (using the radio button)
        driver.find_element("xpath", '//*[@id="radlstProgram_1"]').click()
        time.sleep(1)
        # Enter the roll number
        roll_input = driver.find_element("xpath", '//*[@id="txtrollno"]')
        roll_input.clear()
        roll_input.send_keys(roll_no)
        # Enter the semester
        sem_input = driver.find_element("xpath", '//*[@id="drpSemester"]')
        # sem_input.clear()
        sem_input.send_keys(semester)
    except NoSuchElementException as e:
        print(f"[{roll_no}] Error finding input fields: {e}")
        return None

    # Attempt to solve the CAPTCHA
    attempts = 0
    while attempts < max_attempts:
        attempts += 1
        try:
            # Locate and download the CAPTCHA image
            captcha_img_elem = driver.find_element("xpath", '//*[@id="pnlCaptcha"]/table/tbody/tr[1]/td/div/img')
            captcha_src = captcha_img_elem.get_attribute("src")
            response = requests.get(captcha_src, stream=True)
            img = Image.open(response.raw)
            
            captcha_text = solve_captcha(img)
            print(f"[{roll_no}] Attempt {attempts}: Captcha text guessed as '{captcha_text}'")
            
            # Enter the CAPTCHA
            captcha_input = driver.find_element("xpath", '//*[@id="TextBox1"]')
            captcha_input.clear()
            captcha_input.send_keys(captcha_text)
            time.sleep(2)
            
            # Click the 'View Result' button
            driver.find_element("xpath", '//*[@id="btnviewresult"]').click()
            time.sleep(2)
            
            # Check if an alert appears (indicating wrong captcha or missing enrollment)
            try:
                alert = driver.switch_to.alert
                alert_text = alert.text.strip()
                alert.accept()
                if alert_text == "Enrollment No. Not Found":
                    print(f"[{roll_no}] Enrollment not found.")
                    return {"Roll": roll_no, "Name": "Not Published", "Result": "", "SGPA": "", "CGPA": ""}
                else:
                    print(f"[{roll_no}] Incorrect captcha, trying again (attempt {attempts}).")
                    # Continue the loop to try solving captcha again
                    continue
            except NoAlertPresentException:
                # No alert – assume CAPTCHA is correct and results are displayed
                break
        except Exception as e:
            print(f"[{roll_no}] Exception during captcha process: {e}")
            continue

    if attempts >= max_attempts:
        print(f"[{roll_no}] Maximum captcha attempts reached.")
        return {"Roll": roll_no, "Name": "Captcha Failed", "Result": "", "SGPA": "", "CGPA": ""}

    # After a successful CAPTCHA solve, extract the result details
    try:
        time.sleep(2)  # Wait for the result page to load
        name = driver.find_element("xpath", '//*[@id="lblNameGrading"]').text
        result_status = driver.find_element("xpath", '//*[@id="lblResultNewGrading"]').text
        sgpa = driver.find_element("xpath", '//*[@id="lblSGPA"]').text
        cgpa = driver.find_element("xpath", '//*[@id="lblcgpa"]').text
        print(f"[{roll_no}] Retrieved result for {name}")
        return {"Roll": roll_no, "Name": name, "Result": result_status, "SGPA": sgpa, "CGPA": cgpa}
    except NoSuchElementException as e:
        print(f"[{roll_no}] Error extracting result details: {e}")
        return {"Roll": roll_no, "Name": "Error", "Result": "Error", "SGPA": "Error", "CGPA": "Error"}

# ----------------- Main Script -----------------

if __name__ == "__main__":
    # Setup Selenium WebDriver options
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.headless = False  # Set to True to run without opening a browser window
    service = Service()  # Specify the chromedriver path here if needed
    driver = webdriver.Chrome(service=service, options=options)
    
    # Prepare the CSV file for saving results
    csv_filename = "results.csv"
    fieldnames = ["Roll", "Name", "Result", "SGPA", "CGPA"]
    
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Generate roll numbers – update the range/prefix as per your institute's format
        # Example: roll numbers "0201AI221001" to "0201AI221100"
        roll_prefix = "0201AI2210"
        for i in range(1, 81):
            roll_no = roll_prefix + f"{i:02d}"  # Ensures two-digit formatting (e.g., "01", "02", ..., "100")
            result_data = get_student_result(driver, roll_no, semester="5", max_attempts=5)
            if result_data:
                writer.writerow(result_data)
            else:
                writer.writerow({"Roll": roll_no, "Name": "Error", "Result": "Error", "SGPA": "Error", "CGPA": "Error"})
            # Optional pause between requests to be polite to the server
            time.sleep(1)
    
    driver.quit()
    print("Result scraping completed. Data saved in", csv_filename)
