from api_client import APIClient
from models import Flight, Hotel
from datetime import datetime

class TripPlanner:
    def __init__(self):
        self.client = APIClient()

    def plan_trip(self, vacation_type, start_date, end_date, budget):
        month = datetime.strptime(start_date, "%Y-%m-%d").strftime('%B')
        try:
            destinations = self.client.suggest_destinations(vacation_type, month)
            print(destinations)
            for destination in destinations:
                try:
                    flight = self.client.fetch_flights("Tel Aviv", destination, start_date, end_date)
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

# Test the TripPlanner
if __name__ == "__main__":
    keys = {
        "openai_api_key": "sk-proj-qhejt5MEC6gIQsXrrXUqT3BlbkFJXscAWR9AGMkzSnhapvP7",
        "serpapi_key": "5292a242909f3c34886aaa8b25982b4477e759672e4e3542417c23589d6922b9"
    }
    trip_planner = TripPlanner(keys["openai_api_key"], keys["serpapi_key"])
    trip_planner.plan_trip("beach", "2024-06-01", "2024-06-15", 3000)