from api_client import APIClient
from models import Flight, Hotel
from datetime import datetime

class TripPlanner:
    def __init__(self, openai_api_key, serpapi_key):
        self.client = APIClient(openai_api_key, serpapi_key)

    def plan_trip(self, vacation_type, start_date, end_date, budget):
        month = datetime.strptime(start_date, "%Y-%m-%d").strftime('%B')
        print(f"Vacation type: {vacation_type}, Month: {month}, Start date: {start_date}, End date: {end_date}, Budget: {budget}")
        try:
            destinations = self.client.suggest_destinations(vacation_type, month)
            trip_options = []
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
                    
                    total_price = flight.price + hotel.price
                    trip_options.append((destination, flight, hotel, total_price))
                except Exception as e:
                    print(f"Error planning trip to {destination}: {e}")
                    continue

            if not trip_options:
                print("No suitable trip options found within the budget.")
                return

            self.show_trip_options(trip_options)
            chosen_trip = self.choose_trip_option(trip_options)
            if chosen_trip:
                destination, flight, hotel, total_price = chosen_trip
                print(f"Chosen trip: Destination: {destination}, Flight: {flight}, Hotel: {hotel}, Total price: {total_price}")
                daily_plan = self.client.create_daily_plan(destination, vacation_type, start_date, end_date, month)
                print(f"\nDaily plan for your trip to {destination}:\n{daily_plan}")
        except Exception as e:
            print(f"Error suggesting destinations: {e}")

    def show_trip_options(self, trip_options):
        print("\nTrip options found:")
        for idx, (destination, flight, hotel, total_price) in enumerate(trip_options, 1):
            print(f"{idx}. Destination: {destination}")
            print(f"   Flight: {flight.airline} at ${flight.price}")
            print(f"   Hotel: {hotel.name} at ${hotel.price} per night")
            print(f"   Total Price: ${total_price}")

    def choose_trip_option(self, trip_options):
        choice = int(input("\nChoose a trip option (1-5): "))
        if 1 <= choice <= len(trip_options):
            print(f"Chosen option: {choice}")
            return trip_options[choice - 1]
        else:
            print("Invalid choice.")
            return None
