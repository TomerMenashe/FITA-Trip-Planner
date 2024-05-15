import requests
from models import Flight, Hotel
import pandas as pd



class APIClient:
    def __init__(self):
        self.openai_api_key = 'sk-proj-qhejt5MEC6gIQsXrrXUqT3BlbkFJXscAWR9AGMkzSnhapvP7'
        self.serpapi_key = '5292a242909f3c34886aaa8b25982b4477e759672e4e3542417c23589d6922b9'
        self.google_flights_base_url = "https://serpapi.com//search?engine=google_flights"
        self.google_hotels_base_url = "https://serpapi.com/search?engine=google_hotels"


    def suggest_destinations(self, vacation_type, month):
        """
        Uses the OpenAI API to suggest five travel destinations based on the vacation type and month.
        The request format includes a system and user message to guide the GPT model.
        """
        headers = {
            'Authorization': f'Bearer {self.openai_api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "model": "gpt-4",
            "messages": [
                {
                    "role": "system",
                    "content": "Suggest five travel destinations, mention airports cities ita code suitable for the following type of vacation:"
                },
                {
                    "role": "user",
                    "content": f"{vacation_type} vacation in {month}"
                }
            ],
            "temperature": 0.5,
            "max_tokens": 150
        }
        
        try:
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
            if response.ok:
                suggestions = response.json()['choices'][0]['message']['content'].strip().split(',')
                print([destination.strip() for destination in suggestions])
                return [destination.strip() for destination in suggestions]
            else:
                raise Exception(f"Failed to fetch suggestions: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            print("API Error:", str(e))
            raise Exception("Failed to fetch data from the OpenAI API.")

    def extract_iata_code(self, destination):
        if '(' in destination and ')' in destination:
            start = destination.find('(') + 1
            end = destination.find(')')
            return destination[start:end].strip()
        return None

    def fetch_flights(self, from_city, to_city, date_out, date_return):
        departure_code = "TLV"
        arrival_code = self.extract_iata_code(to_city)

        if not arrival_code:
            raise Exception("Missing airport code for the destination city.")

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
            "max_price": budget
        }
        
        try:
            response = requests.get(self.google_hotels_base_url, params=params)
            response.raise_for_status()
            hotel_data = response.json()
            return self.parse_hotel_data(hotel_data, budget)
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch hotel details: {e}")

    def parse_flight_data(self, data):
        best_flights = data.get("best_flights", [])
        if not best_flights:
            return None

        cheapest_flight = min(best_flights, key=lambda x: x.get('price', float('inf')))

        flight_segments = cheapest_flight['flights']
        first_segment = flight_segments[0]
        last_segment = flight_segments[-1]

        departure_airport = first_segment['departure_airport']['name']
        arrival_airport = last_segment['arrival_airport']['name']
        departure_time = first_segment['departure_airport']['time']
        arrival_time = last_segment['arrival_airport']['time']
        duration = sum(segment['duration'] for segment in flight_segments)
        airplane = first_segment['airplane']
        airline = first_segment['airline']
        travel_class = first_segment['travel_class']
        flight_number = first_segment['flight_number']
        price = cheapest_flight['price']

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
        hotels = data.get("hotels_results", [])
        affordable_hotels = [hotel for hotel in hotels if hotel['price'] <= budget]
        if not affordable_hotels:
            return None
        best_hotel = max(affordable_hotels, key=lambda x: x['price'])
        return Hotel(
            price=best_hotel['price'], 
            name=best_hotel['name'], 
            rating=best_hotel.get('rating', 0)
        )

# Add test function for fetch_hotels
def test_fetch_hotels():
    client = APIClient()

    destinations = [
        "Bali",
        "Los Angeles",
        "Paris"
    ]
    date_checkin = "2024-06-01"
    date_checkout = "2024-06-15"
    budget = 500  # Maximum budget for hotel per night

    for destination in destinations:
        try:
            hotel = client.fetch_hotel(destination, date_checkin, date_checkout, budget)
            if hotel:
                print(f"Hotel: {hotel.name}, Price: ${hotel.price}, Rating: {hotel.rating}")
            else:
                print(f"No hotels found for {destination} within the budget of ${budget} per night")
        except Exception as e:
            print(f"Error fetching hotel details for {destination}: {e}")

if __name__ == "__main__":
    test_fetch_hotels()