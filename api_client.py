import requests
from models import Flight, Hotel
import pandas as pd
import re

class APIClient:
    def __init__(self, openai_api_key, serpapi_key):
        self.openai_api_key = openai_api_key
        self.serpapi_key = serpapi_key
        self.google_flights_base_url = "https://serpapi.com/search?engine=google_flights"
        self.google_hotels_base_url = "https://serpapi.com/search?engine=google_hotels"

    def suggest_destinations(self, vacation_type, month):
        headers = {
            'Authorization': f'Bearer {self.openai_api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "model": "gpt-4",
            "messages": [
                {
                    "role": "system",
                    "content": "Suggest five travel destinations suitable for a {vacation_type} vacation in {month}. For each destination, provide the name of the destination, the name of the nearest airport, and the airport's IATA code in parentheses in the following format: 'Destination Name - Nearest Airport Name (IATA Code)' output only the requested format."
                }
            ],
            "temperature": 0.5,
            "max_tokens": 150
        }
        
        try:
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
            if response.ok:
                suggestions = response.json()['choices'][0]['message']['content'].strip().split(',')
                return [destination.strip() for destination in suggestions]
            else:
                raise Exception(f"Failed to fetch suggestions: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            print("API Error:", str(e))
            raise Exception("Failed to fetch data from the OpenAI API.")

    def extract_iata_code(self, destination):
        match = re.search(r'\((.*?)\)', destination)
        iata_code = match.group(1) if match else None
        return iata_code

    def fetch_flights(self, to_city, date_out, date_return):
        departure_code = "TLV"
        arrival_code = self.extract_iata_code(to_city)
       
        if not arrival_code:
            raise Exception(f"Missing airport code for the destination city: {to_city}")

        params = {
            "engine": "google_flights",
            "departure_id": departure_code,
            "arrival_id": arrival_code,
            "outbound_date": date_out,
            "return_date": date_return,
            "currency": "USD",
            "hl": "en",
            "api_key": self.serpapi_key
        }

        try:
            response = requests.get(self.google_flights_base_url, params=params)
            response.raise_for_status()
            results = response.json()
            return self.parse_flight_data(results)
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch flight details: {e}")

    def fetch_hotel(self, destination, date_checkin, date_checkout, budget):
        params = {
            "engine": "google_hotels",
            "q": f"hotels in {destination} near main attractions and landmarks, offering amenities such as free Wi-Fi, breakfast, and airport shuttle services",
            "check_in_date": date_checkin,
            "check_out_date": date_checkout,
            "api_key": self.serpapi_key,
            "max_price": budget,
        }

        try:
            response = requests.get(self.google_hotels_base_url, params=params)
            response.raise_for_status()
            hotel_data = response.json()
            closest_hotel = self.parse_hotel_data(hotel_data, budget)
            return closest_hotel
        except requests.RequestException as e:
            print(f"Failed to fetch hotel details: {e}")
            raise Exception(f"Failed to fetch hotel details: {e}")

    def parse_flight_data(self, data):
        best_flights = data.get("best_flights", [])
        if not best_flights:
            return None

        cheapest_flight = min(best_flights, key=lambda x: x.get('price', float('inf')))

        flight_segments = cheapest_flight['flights']
        first_segment = flight_segments[0]
        last_segment = flight_segments[-1]

        departure_airport = first_segment['departure_airport'].get('name', 'Unknown')
        arrival_airport = last_segment['arrival_airport'].get('name', 'Unknown')
        departure_time = first_segment['departure_airport'].get('time', 'Unknown')
        arrival_time = last_segment['arrival_airport'].get('time', 'Unknown')
        duration = sum(segment.get('duration', 0) for segment in flight_segments)
        airplane = first_segment.get('airplane', 'Unknown')
        airline = first_segment.get('airline', 'Unknown')
        travel_class = first_segment.get('travel_class', 'Unknown')
        flight_number = first_segment.get('flight_number', 'Unknown')
        price = cheapest_flight.get('price', 'Unknown')

        return Flight(
            price=price,
            airline=airline,
            departure=departure_airport,
            arrival=arrival_airport,
            departure_time=departure_time,
            arrival_time=arrival_time,
            duration=duration,
            airplane=airplane,
            travel_class=travel_class,
            flight_number=flight_number
        )

    def parse_hotel_data(self, data, budget):
        hotels = data.get("properties", [])
        
        # Filter hotels that are within the budget
        affordable_hotels = [hotel for hotel in hotels if hotel.get('total_rate', {}).get('extracted_lowest', float('inf')) <= budget]
        if not affordable_hotels:
            print("No hotels found within the given budget.")
            return None

        # Find the hotel closest to the budget from below (i.e., the highest price under the budget)
        closest_hotel = max(affordable_hotels, key=lambda x: x['total_rate']['extracted_lowest'])

        # Create Hotel object for the closest hotel
        closest_hotel_obj = Hotel(price=closest_hotel['total_rate']['extracted_lowest'], name=closest_hotel['name'])

        return closest_hotel_obj
