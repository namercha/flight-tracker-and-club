# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the
# program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from datetime import datetime, timedelta
from pprint import pprint
from dotenv import load_dotenv
load_dotenv()

ORIGIN_CITY_IATA = "JFK"

data_manager = DataManager()
# 4. Pass everything stored in the "prices" key back to the main.py file and store it in a variable called sheet_data,
# so that you can print the sheet_data from main.py
sheet_data = data_manager.get_destination_data()
# pprint(sheet_data)
flight_search = FlightSearch()

notification_manager = NotificationManager()

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

tomorrows_date = datetime.now() + timedelta(days=1)
six_months_from_today = datetime.now() + timedelta(days=(30 * 6))

data_manager.get_user_input()

for item in sheet_data:
    flight = flight_search.check_flights(
        origin_city_code=ORIGIN_CITY_IATA,
        destination_city_code=item["iataCode"],
        from_date=tomorrows_date,
        to_date=six_months_from_today
    )
    # The final in part 1 step is to check if any of the flights found are cheaper than the Lowest Price listed in the
    # Google Sheet. If so, then we should use the Twilio API to send an SMS with enough information to book the flight.
    # You should use the NotificationManager for this job.
    if flight is not None:
        if flight.price < item["lowestPrice"]:
            message_body = f"Low price alert! "\
                           f"Only ${flight.price} "\
                           f"to fly from {flight.origin_city}-{flight.origin_airport} "\
                           f"to {flight.destination_city}-{flight.destination_airport}, "\
                           f"from {flight.out_date} "\
                           f"to {flight.return_date}."

            notification_manager.send_text_message(message=message_body)
            users = data_manager.get_customer_emails()
            email_list = [item["email"] for item in users]
            names = [item["firstName"] for item in users]

            if flight.layovers > 0:
                message_body += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."
                print(message_body)

            # Not a simple way to generate this link. link = f"https://www.google.com/travel/flights?hl=en#flt={
            # flight.origin_airport}.{flight.destination_airport}.{flight.out_date}*{flight.destination_airport}.{
            # flight.origin_airport}.{flight.return_date}"

            notification_manager.send_email(email_list, message_body)
