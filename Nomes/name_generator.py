import random


def genName(gender):
    firstname_list = []
    if gender == 1:
        firstname_list = open("nomes/FirstNames_f.txt", "r").readlines()
    elif gender == 2:
        firstname_list = open("nomes/FirstNames_m.txt", "r").readlines()

    surname_list = open("nomes/Surnames.txt", "r").readlines()

    first_name = random.choice(firstname_list).strip()
    surname = random.choice(surname_list).strip()

    return first_name, surname
