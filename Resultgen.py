#Importing All selenium libraries to get driver working
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

#Importing For Recaptcha & Extras
import urllib.request
from PIL import Image
from pytesseract import pytesseract
import time

#Paths and website for webdriver and Website JEC
path = "C:/Users/Anubhav Choubey/Documents/Lets CODE/Python_Extra/Automation/chromedriver/chromedriver.exe"
website = "https://www.jecjabalpur.ac.in/exam/programselect.aspx"
sem = '2'
retrived = False

#Driver Declaration And Options if need to use
options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.headless = False
# options.headless = True
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service, options=options)

#Gets us to the website
# driver.get(website)

#To solve recaptcha in the website (low accuracy)
def recapt(url):
    urllib.request.urlretrieve(url, "c.jpg")
    path_to_tesseract = "C:/Program Files/Tesseract-OCR/tesseract.exe"
    image_path = "C:/Users/Anubhav Choubey/Documents/Lets CODE/Python_Extra/Automation/c.jpg"
    img = Image.open(image_path)
    
    pytesseract.tesseract_cmd = path_to_tesseract
    text = pytesseract.image_to_string(img)
    text =  text[:-1].upper().replace(" ","")
    text = text.replace("\n","")
    return text[:5]

#Complete function to generate the Result of one roll no.
def genResult(roll):
    driver.get(website)
    driver.find_element(by='xpath', value='//*[@id="radlstProgram_1"]').click()
    driver.find_element(by='xpath', value='//*[@id="drpSemester"]').send_keys(sem)

    driver.find_element(by='xpath', value='//*[@id="txtrollno"]').send_keys(roll)
    src = driver.find_element(by='xpath', value='//*[@id="pnlCaptcha"]/table/tbody/tr[1]/td/div/img').get_attribute('src')
    recpt = recapt(src)
    print(recpt)
    time.sleep(1.5)
    driver.find_element(by='xpath', value='//*[@id="TextBox1"]').send_keys(recpt)
    time.sleep(1.5)
    driver.find_element(by='xpath', value='//*[@id="btnviewresult"]').click()

#Retrives Data Of result from website
def retr(roll,retrived):
    try:
        name = driver.find_element(by='xpath', value='//*[@id="lblNameGrading"]').text
        res = driver.find_element(by='xpath', value='//*[@id="lblResultNewGrading"]').text
        sgpa = driver.find_element(by='xpath', value='//*[@id="lblSGPA"]').text
        cgpa = driver.find_element(by='xpath', value='//*[@id="lblcgpa"]').text

        with open('Results.txt', 'a') as saver:
            saver.write(f'{roll},{name},{res},{sgpa},{cgpa}\n')
        saver.close()
        print("Retrived ",name)
        retrived = True
    except:
        print("Problem Occured")
        retrived = False
    return retrived

def comp(roll, retrived):
    genResult(roll)
    ret = retr(roll, retrived)
    if not ret:
        time.sleep(1)
        comp(roll,ret)


rolln = '0201AI2210'
for i in range(61,79):
    rollno = rolln + str(i)
    try:
        comp(rollno, retrived)
    except:
        print("Kuch toh Gadbad h daya!")
        comp(rollno, retrived)
print("kand kr diya")