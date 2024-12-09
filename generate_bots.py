from nomes import name_generator

import sys
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

CREATE_GOOGLE_ACCOUNT_URL = "https://accounts.google.com/signup/v2/createaccount?flowName=GlifWebSignIn&flowEntry=SignUp"

def main():
    print("\n$$$..............EXECUTING.............$$$")
    number_bots = 0
    # Validate user inputs
    if len(sys.argv) == 2 and sys.argv[1].isdigit():
        number_bots = sys.argv[1]
    else:
        print("!!! USAGE: python generate_bots.py <number of bots> !!!")
        number_bots = int(input("ENTER NUMBER OF BOTS: "))

    print("\n$$$............GENERATING " + str(number_bots) + " GOOGLE ACCOUNTS...........$$$")

    user_agent = generate_random_useragent()
    browser = setup_webdriver(user_agent)
    browser.get(CREATE_GOOGLE_ACCOUNT_URL)
    print("\n$$$...........CONNECTED TO GOOGLE SERVICE...........$$$")

    fill_forms()


# Get random user agent from db dump
def generate_random_useragent():
    db = open("useragent_db.txt")
    line = next(db)
    for num, aline in enumerate(db, 2):
        if random.randrange(num):
            continue
        line = aline
    return line


# Create Firefox webdriver with random user agent
def setup_webdriver(user_agent):
    options = Options()
    firefox_profile = FirefoxProfile()
    firefox_profile.set_preference("general.useragent.override", user_agent)
    options.profile = firefox_profile

    return webdriver.Firefox(options = options)





def fill_forms():



# Connect to google account creation page
wait = WebDriverWait(browser, 20)
wait.until(EC.element_to_be_clickable((By.NAME, "firstName")))  # sync


gender = random.randint(1, 2)
first_name, surname = name_generator.genName(gender)
# name form
print("\n$$$...........FILLING ACCOUNT NAME...........$$$")
browser.find_element(By.NAME, "firstName").clear()
browser.find_element(By.NAME, "firstName").send_keys(first_name)
browser.find_element(By.NAME, "lastName").clear()
browser.find_element(By.NAME, "lastName").send_keys(surname)
# submit the form
browser.find_element(By.ID, "collectNameNext").click()
print("\n$$$...........DONE...........$$$")

wait.until(EC.element_to_be_clickable((By.ID, "day")))  # sync

# birthday and gender forms
print("\n$$$...........FILLING ACCOUNT BIRTHDAY AND AGE...........$$$")
browser.find_element(By.ID, "day").send_keys(str(random.randint(1, 28)))
month = Select(browser.find_element(By.ID, 'month'))
month.select_by_index(random.randint(1, 12))
# calculate the birth year of a 20 to 40 years old person
actual_year = datetime.now().year
birth_year = random.randint(actual_year - 40, actual_year - 20)
browser.find_element(By.ID, "year").send_keys(str(birth_year))

# gender
gender_select = Select(browser.find_element(By.ID, "gender"))
gender_select.select_by_index(gender)
browser.find_element(By.ID, "birthdaygenderNext").click()
print("\n$$$...........DONE...........$$$")

wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Create a Gmail address')]")))  # sync

# create new email address
print("\n$$$...........CREATING NEW EMAIL ADDRESS...........$$$")
# the elements on this page have their ids either dynamically generated or are not set. Used xpath instead
browser.find_element(By.XPATH, "//*[contains(text(),'Create a Gmail address')]").click()
browser.find_element(By.XPATH, "//*[contains(text(),'Next')]").click()
# submit new email address
wait.until(EC.element_to_be_clickable((By.NAME, "Username")))  # sync
# must be guaranteed to be unique
browser.find_element(By.NAME, "Username").send_keys(first_name + surname)

print("\n$$$...........DONE...........$$$")
