import requests
import os

# 1. Go to the link for the starting Google Sheet and make your own copy of it.
# Then create a new project on Sheety to work with your copy of the Google sheet.
SHEETY_PRICES_ENDPOINT = os.environ["SHEETY_PRICES_ENDPOINT"]
SHEETY_BEARER_TOKEN = os.environ["SHEETY_BEARER_TOKEN"]


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
