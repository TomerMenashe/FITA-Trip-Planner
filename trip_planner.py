from api_client import APIClient
from models import Flight, Hotel
from datetime import datetime

class TripPlanner:
    def __init__(self, openai_api_key, serpapi_key):
        self.client = APIClient(openai_api_key, serpapi_key)

    def plan_trip(self, vacation_type, start_date, end_date, budget):
        month = datetime.strptime(start_date, "%Y-%m-%d").strftime('%B')
        try:
            destinations = self.client.suggest_destinations(vacation_type, month)
            for destination in destinations:
                try:
                    flight = self.client.fetch_flights(destination, start_date, end_date)
                    if not flight:
                        print(f"No flight found for destination: {destination}")
                        continue
                    
                    remaining_budget = budget - flight.price
                    hotel = self.client.fetch_hotel(destination, start_date, end_date, remaining_budget)
                    if not hotel:
                        print(f"No hotel found within budget for destination: {destination}")
                        continue
                    
                    print(f"Destination: {destination}, Flight: {flight.airline} at ${flight.price}, Hotel: {hotel.name} at ${hotel.price}")
                except Exception as e:
                    print(f"Error planning trip to {destination}: {e}")
        except Exception as e:
            print(f"Error suggesting destinations: {e}")
