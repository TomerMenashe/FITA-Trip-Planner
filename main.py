from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime
from trip_planner import TripPlanner
import logging

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to the specific origin(s) if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Replace these with your actual API keys
OPENAI_API_KEY ="sk-proj-qhejt5MEC6gIQsXrrXUqT3BlbkFJXscAWR9AGMkzSnhapvP7"
SERPAPI_KEY = "18fa1d9f64bca597a1ea23757919cfe7045603ccc7b31d5b83c832d9db47d43d"

trip_planner = TripPlanner(OPENAI_API_KEY, SERPAPI_KEY)

class TripRequest(BaseModel):
    vacation_type: str
    start_date: str
    end_date: str
    budget: float

class TripChoice(BaseModel):
    choice: int

@app.post("/plan_trip")
async def plan_trip(trip_request: TripRequest):
    try:
        print(f"Received trip planning request: {trip_request}")
        trip_options = trip_planner.plan_trip(
            trip_request.vacation_type,
            trip_request.start_date,
            trip_request.end_date,
            trip_request.budget
        )
        if isinstance(trip_options, dict) and 'error' in trip_options:
            raise HTTPException(status_code=400, detail=trip_options['error'])
        return trip_options
    except Exception as e:
        print(f"Error planning trip: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/choose_trip")
async def choose_trip(trip_choice: TripChoice):
    try:
        print(f"Received trip choice request: {trip_choice}")
        trip_options = trip_planner.current_trip_options
        if not trip_options:
            raise HTTPException(status_code=400, detail="No trip options available. Please plan a trip first.")

        selected_trip = trip_planner.choose_trip_option(trip_options, trip_choice.choice)
        if not selected_trip:
            raise HTTPException(status_code=400, detail="Invalid choice")

        # Generate the detailed plan and images
        month = datetime.strptime(trip_planner.current_start_date, "%Y-%m-%d").strftime('%B')
        print(f"Generating daily plan for: {selected_trip['destination']}")
        daily_plan = trip_planner.create_daily_plan(
            selected_trip['destination'],
            trip_planner.current_vacation_type,
            trip_planner.current_start_date,
            trip_planner.current_end_date,
            month
        )
        selected_trip['daily_plan'] = daily_plan
        activities = trip_planner.extract_activities(daily_plan)
        print(f"Generating images for activities: {activities}")
        image_urls = trip_planner.create_images(activities)
        selected_trip['image_urls'] = image_urls

        print(f"Selected trip: {selected_trip}")
        return selected_trip
    except Exception as e:
        print(f"Error choosing trip: {e}")
        raise HTTPException(status_code=500, detail=str(e))