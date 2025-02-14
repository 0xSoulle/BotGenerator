import threading

from bot_info import info_generator

import sys
import random
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
        number_bots = int(sys.argv[1])
    else:
        print("!!! USAGE: python generate_bots.py <number of bots> !!!")
        number_bots = int(input("ENTER NUMBER OF BOTS: "))


    print("\n$$$............GENERATING " + str(number_bots) + " GOOGLE ACCOUNTS...........$$$")

    for bot in range(number_bots):
        tid = threading.Thread(target=bot_thread)
        tid.start()




def bot_thread():
    print("\n$$$...........STARTING BROWSER...........$$$")

    # Get a user agent from db
    user_agent = generate_random_useragent()

    # setup selenium driver with the user agent aaaaaaaaa
    browser = setup_webdriver(user_agent)

    # Connect to google account creation page
    try:
        browser.get(CREATE_GOOGLE_ACCOUNT_URL)
        print("\n$$$...........CONNECTED TO GOOGLE SERVICE...........$$$")

        fill_forms(browser)

        print("\n$$$...........FINNISHED CREATING BOT...........$$$")
    finally:
        # close the browser
        browser.quit()



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
    # run browser headless mode
    options = Options()
    #options.add_argument("--headless")

    return webdriver.Firefox(options)


def fill_forms(browser):

    # define characteristics for bot account
    gender,first_name, surname,year, month, day = info_generator.gen_info()
    # calculate the birth year of a 20 to 40 years old person

    wait = WebDriverWait(browser, 10)

    print("\n$$$...........FILLING ACCOUNT NAME...........$$$")
    # name form
    first_name_entry = wait.until(EC.element_to_be_clickable((By.NAME, "firstName")))  # sync
    first_name_entry.clear()
    first_name_entry.send_keys(first_name)
    browser.find_element(By.NAME, "lastName").clear()
    browser.find_element(By.NAME, "lastName").send_keys(surname)

    # submit the form
    browser.find_element(By.ID, "collectNameNext").click()
    print("\n$$$...........DONE...........$$$")


    # birthday and gender forms
    print("\n$$$...........FILLING ACCOUNT BIRTHDAY AND AGE...........$$$")
    brithday = wait.until(EC.element_to_be_clickable((By.ID, "day")))  # sync
    brithday.send_keys(day)
    month_element = wait.until(EC.element_to_be_clickable(browser.find_element(By.ID, "month")))
    month = Select(month_element)
    month.select_by_index(random.randint(1, 12))

    browser.find_element(By.ID, "year").send_keys(year)

    # gender
    gender_select = Select(browser.find_element(By.ID, "gender"))
    gender_select.select_by_index(gender)
    browser.find_element(By.ID, "birthdaygenderNext").click()
    print("\n$$$...........DONE...........$$$")

    # create new email address
    print("\n$$$...........CREATING NEW EMAIL ADDRESS...........$$$")

    create_gmail_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Create a Gmail address')]")))  # sync

    # the elements on this page have their ids either dynamically generated or are not set. Used xpath instead
    create_gmail_option.click()
    browser.find_element(By.XPATH, "//*[contains(text(),'Next')]").click()

    # check for Gmail suggestions
    html_content = browser.page_source

    if "Choose your Gmail address" in html_content:
        # click second option (looks natural more often)
        email_suggestions = browser.find_elements(By.XPATH, "//*[contains(text(),'.*@gmail.com')]")
        email_suggestions[1].click()
        email_suggestions[1].text()
        # submit
        browser.find_element(By.XPATH, "//*[contains(text(),'Next')]").click()
    else:
        # submit an email address
        wait.until(EC.element_to_be_clickable((By.NAME, "Username")))  # sync

        # must be guaranteed to be unique
        magic = chr(random.randrange(65, 90))
        base = first_name + "." + surname
        address = magic + year[:2] + "." + base + "." + year[2:] + magic

        browser.find_element(By.NAME, "Username").send_keys(address)

    print("\n$$$...........DONE...........$$$")



if __name__ == "__main__":
    main()

