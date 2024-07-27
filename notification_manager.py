import os
from twilio.rest import Client
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# This is responsible for sendingout a twilio message to whatsApp about the cheapest flight found or if not flights that match the criteria are found
class NotificationManager:
    def __init__(self):
        self.twilio_auth_token = os.getenv("twilio_auth_token")
        self.twilio_account_SID = os.getenv("twilio_account_SID")

    def send_message(self, city, lowestPrice, departureDate, returnDate):
        client = Client(self.twilio_account_SID, self.twilio_auth_token)
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=f'Low Price Alert! There is a flight to {city} for ${lowestPrice}, leaving Sydney {departureDate} and returning {returnDate}',
            to='whatsapp:+61490064563'
        )

    def no_flights_message(self, city):
        client = Client(self.twilio_account_SID, self.twilio_auth_token)
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=f"Sorry we found no flight's to {city} matching your criteria ",
            to='whatsapp:+61490064563'
        )