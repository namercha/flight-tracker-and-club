import requests
import os
from dotenv import load_dotenv
load_dotenv()

# 1. Go to the link for the starting Google Sheet and make your own copy of it.
# Then create a new project on Sheety to work with your copy of the Google sheet.
SHEETY_PRICES_ENDPOINT = os.environ["SHEETY_PRICES_ENDPOINT"]
SHEETY_BEARER_TOKEN = os.environ["SHEETY_BEARER_TOKEN"]
SHEETY_USERS_ENDPOINT = os.environ["SHEETY_USERS_ENDPOINT"]


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        # 2. Now use the Sheety API to GET all the data in that sheet and print it out.
        sheety_auth = {
            "Authorization": f"Bearer {SHEETY_BEARER_TOKEN}"
        }
        response = requests.get(url=SHEETY_PRICES_ENDPOINT, headers=sheety_auth)
        results = response.json()
        self.destination_data = results['prices']
        return self.destination_data

    # 6. In the DataManager Class make a PUT request and use the row id  from sheet_data to update the Google Sheet
    # with the IATA codes. (Do this using code). HINT: Remember to check the checkbox to allow PUT requests in Sheety.
    def put_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            sheety_auth = {
                "Authorization": f"Bearer {SHEETY_BEARER_TOKEN}"
            }
            response = requests.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                json=new_data,
                headers=sheety_auth
            )
            print(response.text)

    # 7. Ask the user for their first name, last name and email. Make sure to get them to type their email twice for
    # validation. If the two emails match, then tell them that they're in the club. e.g.
    def get_user_input(self):
        print("Welcome to Nabil's Flight Club."
              "\nWe find the best flight deals and email you.")

        first_name = input("What is your first name?\n")
        last_name = input("What is your last name?\n")
        email_first_entry = input("What is your email address?\n")
        email_second_entry = input("Please en-enter your email again.\n")

        if email_first_entry == email_second_entry:
            print("The emails match. Adding you to the Flight Club.")
            user_info = {
                "user": {
                    "firstName": first_name,
                    "lastName": last_name,
                    "email": email_second_entry
                }
            }
            sheety_auth = {
                "Authorization": f"Bearer {SHEETY_BEARER_TOKEN}"
            }
            response = requests.post(
                url=f"{SHEETY_USERS_ENDPOINT}",
                json=user_info,
                headers=sheety_auth
            )
            print(response.text)

        else:
            print("The emails don't match. Cannot sign you up, Sorry.")



