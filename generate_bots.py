from Nomes import NameGenerator

import sys
from selenium import webdriver

print("$$$..............EXECUTING.............$$$ \n")
number_bots = 0
CREATE_GOOGLE_ACCOUNT_URL = "https://accounts.google.com/lifecycle/steps/signup/name?ddm=0&dsh=S941546135:1721948925508654&flowEntry=SignUp&flowName=GlifWebSignIn&TL=ALoj5Ao_p9rim082m1ADtR6Uc3LUObMFfIrnUDn6As2pFWJPEkNIqZJD3u6Ov5n2"

# Validate user inputs
if len(sys.argv) == 2 and sys.argv[1].isdigit():
    number_bots = sys.argv[1]
else:
    print("!!! USAGE: python generate_bots.py <number of bots> !!!")
    number_bots = int(input("ENTER NUMBER OF BOTS: "))

print("\n$$$............GENERATING " + str(number_bots) + " GOOGLE ACCOUNTS...........$$$")

browser = webdriver.Chrome()
browser.get(CREATE_GOOGLE_ACCOUNT_URL)

for i in range(number_bots):
    nome_propio, apelido = NameGenerator.genName()
    browser.select_form("firstName")
    browser.form["firstName"] = nome_propio
    browser.form["lastName"] = apelido
    browser.submit()