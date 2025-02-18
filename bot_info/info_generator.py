import requests

def gen_info():
    # get new fake profile from API
    api_res = requests.get("https://randomuser.me/api/")
    res_json = api_res.json()

    # query each information
    profile = res_json["results"][0]
    gender = profile["gender"]
    if gender == "female":
        gender = 1
    else:
        gender = 2

    first_name = profile["name"]["first"]
    surname = profile["name"]["last"]

    birthdate = profile["dob"]["date"]
    birthdate = birthdate.split("T")[0]
    year_month_day = birthdate.split("-")

    year = year_month_day[0]
    month = year_month_day[1]
    day = year_month_day[2]

    return gender, first_name, surname, year, month, day

