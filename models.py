class Flight:
    def __init__(self, departure, arrival, price, airline, departure_time, arrival_time, duration, airplane, travel_class, flight_number):
        self.departure = departure
        self.arrival = arrival
        self.price = price
        self.airline = airline
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.duration = duration
        self.airplane = airplane
        self.travel_class = travel_class
        self.flight_number = flight_number
    
    def __repr__(self):
        return f"Flight from {self.departure} to {self.arrival} with {self.airline} at ${self.price}, departing at {self.departure_time}, arriving at {self.arrival_time}, duration {self.duration} minutes, airplane {self.airplane}, class {self.travel_class}, flight number {self.flight_number}"

class Hotel:
    def __init__(self, name, price, rating):
        self.name = name
        self.price = price
        self.rating = rating
    
    def __repr__(self):
        return f"Hotel {self.name} at ${self.price} with rating {self.rating}"
