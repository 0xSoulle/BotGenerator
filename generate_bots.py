from nomes import name_generator

import sys
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


print("$$$..............EXECUTING.............$$$ \n")
number_bots = 0
CREATE_GOOGLE_ACCOUNT_URL = "https://accounts.google.com/signup/v2/createaccount?flowName=GlifWebSignIn&flowEntry=SignUp"

# Validate user inputs
if len(sys.argv) == 2 and sys.argv[1].isdigit():
    number_bots = sys.argv[1]
else:
    print("!!! USAGE: python generate_bots.py <number of bots> !!!")
    number_bots = int(input("ENTER NUMBER OF BOTS: "))

print("\n$$$............GENERATING " + str(number_bots) + " GOOGLE ACCOUNTS...........$$$")

# Connect to google account creation page
browser = webdriver.Firefox()
browser.get(CREATE_GOOGLE_ACCOUNT_URL)
wait = WebDriverWait(browser, 20)
wait.until(EC.element_to_be_clickable((By.NAME, "firstName")))  # sync

gender = random.randint(1, 2)
first_name, surname = name_generator.genName(gender)
# name form
browser.find_element(By.NAME, "firstName").clear()
browser.find_element(By.NAME, "firstName").send_keys(first_name)
browser.find_element(By.NAME, "lastName").clear()
browser.find_element(By.NAME, "lastName").send_keys(surname)
# submit the form
browser.find_element(By.ID, "collectNameNext").click()


wait.until(EC.element_to_be_clickable((By.ID, "day")))  # sync

# birthday and gender forms
browser.find_element(By.ID, "day").send_keys(str(random.randint(1, 28)))
month = Select(browser.find_element(By.ID, 'month'))
month.select_by_index(random.randint(1, 12))
# calculate the birthyear of a 20 to 40 years old person
actual_year = datetime.now().year
birthyear = random.randint(actual_year - 40, actual_year - 20)
browser.find_element(By.ID, "year").send_keys(str(birthyear))

# gender
gender_select = Select(browser.find_element(By.ID, "gender"))
gender_select.select_by_index(gender)
browser.find_element(By.ID, "birthdaygenderNext").click()

# create new email adress
browser.find_element(By.ID, "selectionc7").click()
browser.find_element(By.ID, "").click()
browser.find_element(By.NAME, "username").send_keys(first_name + surname)

    