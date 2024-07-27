import os
import requests
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# this is responsible for getting the token, flights and IATA codes from the Amadeus API
class FlightSearch:
    def __init__(self):
        self.api_key = os.getenv('FLIGHT_API_KEY')
        self.api_secret = os.getenv('FLIGHT_API_SECRET')
        self.token = self.get_new_token()

    def get_new_token(self):
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'grant_type': 'client_credentials',
            'client_id': self.api_key,
            'client_secret': self.api_secret
        }
        TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"
        response = requests.post(url=TOKEN_ENDPOINT, headers=header, data=body)
        self.access_token = response.json()['access_token']
        self.HEADER = {
            "Authorization": f"Bearer {self.access_token}"
        }

    def get_city(self, cities):
        IATA_url = f"https://test.api.amadeus.com/v1/reference-data/locations/cities?keyword={cities}&max=10"
        response = requests.get(url=IATA_url, headers=self.HEADER)
        flight_data = response.json()
        self.IATA_codes = flight_data["data"][0]["iataCode"]
        return self.IATA_codes

    def get_flights(self, city, lowestPrice, departSYD, returnHome):
        flight_deal_url = f'https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode=SYD&destinationLocationCode={city}&departureDate={departSYD}&returnDate={returnHome}&adults=1&travelClass=ECONOMY&nonStop=false&currencyCode=AUD&maxPrice={lowestPrice}&max=250'
        response = requests.get(url=flight_deal_url, headers=self.HEADER)
        flight_deals = response.json()
        return flight_deals


