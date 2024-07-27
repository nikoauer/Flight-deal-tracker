import os
from pprint import pprint
from dotenv import find_dotenv, load_dotenv
from notification_manager import NotificationManager
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flight_search import FlightSearch
from flight_data import FlightData

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

def main():
    credentials = None
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(credentials.to_json())

    try:
        service = build("sheets", "v4", credentials=credentials)
        sheets = service.spreadsheets()
        for row in range(2,11):
            iataResults = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=f"prices!B{row}").execute().get("values")
            cityResults = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=f"prices!A{row}").execute().get("values")
            priceResults = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=f"prices!C{row}").execute().get("values")
            departureResults = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=f"prices!D{row}").execute().get("values")
            print(departureResults)
            returnResults = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=f"prices!E{row}").execute().get("values")
            flight_search = FlightSearch()
            if iataResults == None:
                iata_code = flight_search.get_city(cityResults[0][0])
                sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"prices!B{row}", valueInputOption="USER_ENTERED", body={"values": [[f"{iata_code}"]]}).execute()
            else:
                flight_deals = flight_search.get_flights(iataResults[0][0], priceResults[0][0],
                                                         departureResults[0][0], returnResults[0][0])
                if not flight_deals['data']:
                    notification_manager = NotificationManager()
                    no_flights_message = notification_manager.no_flights_message(cityResults[0][0])
                else:
                    flight_data = FlightData()
                    lowest_price = flight_data.find_lowest_price(flight_deals)
                    notification_manager = NotificationManager()
                    send_message = notification_manager.send_message(cityResults[0][0], lowest_price, departureResults[0][0], returnResults[0][0])

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == '__main__':
    main()
