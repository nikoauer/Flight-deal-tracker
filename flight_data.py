# This is responsible for finding the lowest price in the flights from the Amadeus API

class FlightData:
    def __init__(self):
        self.list_of_prices = []

    def find_lowest_price(self, flight_deals):
        x = len(flight_deals['data'])
        for price in range(0, x):
            flight_price = int(float(flight_deals['data'][price]['price']['grandTotal']))
            self.list_of_prices.append(flight_price)
        return(min(self.list_of_prices))
