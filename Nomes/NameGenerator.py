import random


def genName():
    firstname_list = open("Nomes/FirstNames.txt", "r").readlines()
    surname_list = open("Nomes/Surnames.txt", "r").readlines()

    first_name = random.choice(firstname_list).strip()
    surname = random.choice(surname_list).strip()

    return first_name, surname
