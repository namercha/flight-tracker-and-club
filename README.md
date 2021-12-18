## Flight Tracker

This program is to use a combination of multiple APIs to find a good flight deal. 

### Part 1
There is a Google sheet that has the location of the places you want to visit and a price cutoff (which is the historical low price). That data will be fed into a flight search API every day.
When a price is found that matches the lowest price and destinations, an SMS will be sent with the deal details.

#### Searching for Flights
The next step is to search for the flight prices from New York (JFK) to all the destinations in the Google Sheet. In this project, we're looking only for direct flights, that leave anytime between tomorrow and in 6 months (6x30days) time. We're also looking for round trips that return between 7 and 28 days in length. The currency of the price we get back should be in UDS.

### APIs Required
Google Sheet Data Management - https://sheety.co/

Kiwi Partners Flight Search API (Free Signup, Requires Credit Card Details) - https://partners.kiwi.com/

Tequila Flight Search API Documentation - https://tequila.kiwi.com/portal/docs/tequila_api

Twilio SMS API - https://www.twilio.com/docs/sms

