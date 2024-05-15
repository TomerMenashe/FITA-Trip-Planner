from trip_planner import TripPlanner

def get_user_input():
    vacation_type = input("Enter your preferred type of vacation (ski, beach, city): ")
    start_date = input("Enter the start date of your trip (YYYY-MM-DD): ")
    end_date = input("Enter the end date of your trip (YYYY-MM-DD): ")
    budget = float(input("Enter your total budget for the trip in USD: "))
    return vacation_type, start_date, end_date, budget

def run_tests():
    keys = {
        "openai_api_key": "sk-proj-qhejt5MEC6gIQsXrrXUqT3BlbkFJXscAWR9AGMkzSnhapvP7",
        "serpapi_key": "d6a8654640ef0b2dcec805a7939d03430074b2c0fc69e0e6810e02a51c76e808"
    }
    planner = TripPlanner(keys["openai_api_key"], keys["serpapi_key"])

    test_cases = [
        ("beach", "2024-06-01", "2024-06-15", 3000),
        ("ski", "2024-12-01", "2024-12-15", 4000),
        ("city", "2024-09-01", "2024-09-15", 2500)
    ]

    for vacation_type, start_date, end_date, budget in test_cases:
        print(f"\nRunning test case: {vacation_type}, {start_date} to {end_date}, Budget: {budget}")
        planner.plan_trip(vacation_type, start_date, end_date, budget)

def main():
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        run_tests()
    else:
        keys = {
            "openai_api_key": "sk-proj-qhejt5MEC6gIQsXrrXUqT3BlbkFJXscAWR9AGMkzSnhapvP7",
            "serpapi_key": "d6a8654640ef0b2dcec805a7939d03430074b2c0fc69e0e6810e02a51c76e808"
        }

        vacation_type, start_date, end_date, budget = get_user_input()
        planner = TripPlanner(keys["openai_api_key"], keys["serpapi_key"])
        planner.plan_trip(vacation_type, start_date, end_date, budget)

if __name__ == "__main__":
    main()
