from trip_planner import TripPlanner

def get_user_input():
    vacation_type = input("Enter your preferred type of vacation (ski, beach, city): ")
    start_date = input("Enter the start date of your trip (YYYY-MM-DD): ")
    end_date = input("Enter the end date of your trip (YYYY-MM-DD): ")
    budget = float(input("Enter your total budget for the trip in USD: "))
    return vacation_type, start_date, end_date, budget



def main():
    vacation_type, start_date, end_date, budget = get_user_input()
    planner = TripPlanner()
    planner.plan_trip(vacation_type, start_date, end_date, budget)


if __name__ == "__main__":
    main()
