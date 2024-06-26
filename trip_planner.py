from api_client import APIClient
from models import Flight, Hotel
from datetime import datetime
import requests

class TripPlanner:
    """
    A class to plan trips by fetching flight and hotel information, creating daily plans, and generating images for activities.
    """
    
    def __init__(self, openai_api_key, serpapi_key):
        """
        Initialize the TripPlanner with OpenAI and SerpAPI keys.
        
        :param openai_api_key: str: API key for OpenAI
        :param serpapi_key: str: API key for SerpAPI
        """
        self.client = APIClient(openai_api_key, serpapi_key)
        self.current_trip_options = []
        self.current_vacation_type = ""
        self.current_start_date = ""
        self.current_end_date = ""
        self.openai_api_key = openai_api_key 
        self.serpapi_key = serpapi_key        

    def plan_trip(self, vacation_type, start_date, end_date, budget):
        """
        Plan a trip based on the vacation type, dates, and budget.
        
        :param vacation_type: str: Type of vacation (e.g., beach, adventure)
        :param start_date: str: Start date of the trip in YYYY-MM-DD format
        :param end_date: str: End date of the trip in YYYY-MM-DD format
        :param budget: float: Total budget for the trip
        :return: list: List of trip options or a dictionary with an error message
        """
        month = datetime.strptime(start_date, "%Y-%m-%d").strftime('%B')
        self.current_vacation_type = vacation_type
        self.current_start_date = start_date
        self.current_end_date = end_date
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
                return []

            self.current_trip_options = self.show_trip_options(trip_options)
            return self.current_trip_options
        except Exception as e:
            print(f"Error suggesting destinations: {e}")
            return {"error": str(e)}

    def extract_activities(self, daily_plan):
        """
        Extract a list of activities from a daily plan.
        
        :param daily_plan: str: The daily plan as a single string
        :return: list: List of formatted activities
        """
        activities = daily_plan.split('\n')
        formatted_activities = [activity.strip() for activity in activities if activity.strip()]
        return formatted_activities[:4]

    def show_trip_options(self, trip_options):
        """
        Format trip options for display.
        
        :param trip_options: list: List of trip options (destination, flight, hotel, total price)
        :return: list: List of formatted trip options
        """
        trip_options_data = []
        for destination, flight, hotel, total_price in trip_options:
            option = {
                "destination": destination,
                "flight": {"airline": flight.airline, "price": flight.price},
                "hotel": {"name": hotel.name, "price": hotel.price},
                "total_price": total_price
            }
            trip_options_data.append(option)
        return trip_options_data

    def choose_trip_option(self, trip_options, choice):
        """
        Choose a specific trip option from the list.
        
        :param trip_options: list: List of available trip options
        :param choice: int: User's choice (1-based index)
        :return: dict: Selected trip option or None if invalid choice
        """
        if 1 <= choice <= len(trip_options):
            return trip_options[choice - 1]
        else:
            return None

    def create_daily_plan(self, destination, vacation_type, start_date, end_date, month):
        """
        Create a daily plan for the trip using OpenAI API.
        
        :param destination: str: Destination city
        :param vacation_type: str: Type of vacation
        :param start_date: str: Start date of the trip in YYYY-MM-DD format
        :param end_date: str: End date of the trip in YYYY-MM-DD format
        :param month: str: Month of the trip
        :return: str: Generated daily plan
        """
        prompt = (f"Create a daily plan for a {vacation_type} vacation in {destination} from {start_date} to {end_date}. "
                  f"Include activities and suggestions suitable for the month of {month}, make each day a plan.")

        headers = {
            'Authorization': f'Bearer {self.openai_api_key}',  
            'Content-Type': 'application/json'
        }

        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 3000
        }

        try:
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
            if response.ok:
                daily_plan = response.json()['choices'][0]['message']['content']
                return daily_plan
            else:
                raise Exception(f"Failed to create daily plan: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            raise Exception(f"Failed to create daily plan from the OpenAI API: {e}")

    def create_images(self, activities):
        """
        Create images for activities using the OpenAI API.
        
        :param activities: list: List of activities
        :return: list: List of image URLs
        """
        headers = {
            'Authorization': f'Bearer {self.openai_api_key}',  # Use the stored API key
            'Content-Type': 'application/json'
        }

        image_urls = []
        for activity in activities:
            prompt = f"{activity}"
            data = {
                "prompt": prompt,
                "n": 1,
                "size": "1024x1024"
            }

            try:
                response = requests.post('https://api.openai.com/v1/images/generations', headers=headers, json=data)
                if response.ok:
                    images = response.json()['data']
                    for img in images:
                        image_urls.append(img['url'])
                else:
                    print(f"Failed to create image: {response.status_code} - {response.text}")
            except requests.RequestException as e:
                print(f"API Error: {e}")

        return image_urls

    def suggest_activities_images(self, activities):
        """
        Suggest image prompts for activities using OpenAI API.
        
        :param activities: list: List of activities
        :return: list: List of suggested image prompts
        """
        headers = {
            'Authorization': f'Bearer {self.openai_api_key}',  # Use the stored API key
            'Content-Type': 'application/json'
        }

        data = {
            "model": "gpt-4",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert in planning trips and suggesting suitable image prompts for DALL-E."
                },
                {
                    "role": "user",
                    "content": f"Suggest 4 suitable image prompts for DALL-E that will describe the best attractions of this trip based on the destination and the given activities, make it nice and professional images: {activities}."
                }
            ],
            "temperature": 0.5,
            "max_tokens": 150
        }

        try:
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
            if response.ok:
                suggestions = response.json()['choices'][0]['message']['content'].strip().split('\n')
                return [suggestion.strip() for suggestion in suggestions if suggestion.strip()][:4]
            else:
                raise Exception(f"Failed to fetch suggestions: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            print("API Error:", str(e))
            raise Exception("Failed to fetch data from the OpenAI API.")
