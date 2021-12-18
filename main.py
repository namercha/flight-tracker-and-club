# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the
# program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from pprint import pprint

data_manager = DataManager()
# 4. Pass everything stored in the "prices" key back to the main.py file and store it in a variable called sheet_data,
# so that you can print the sheet_data from main.py
sheet_data = data_manager.get_destination_data()
# pprint(sheet_data)

# 5. In main.py check if sheet_data contains any values for the "iataCode" key.
# If not, then the IATA Codes column is empty in the Google Sheet.
# In this case, pass each city name in sheet_data one-by-one to the FlightSearch class.
# For now, the FlightSearch class can respond with "TESTING" instead of a real IATA code.
# You should use the response from the FlightSearch class to update the sheet_data dictionary.
if sheet_data[0]["iataCode"] == "":
    flight_search = FlightSearch()
    for item in sheet_data:
        item["iataCode"] = flight_search.get_destination_code(item["city"])
    
    pprint(sheet_data)

    data_manager.destination_data = sheet_data
    data_manager.put_destination_codes()
