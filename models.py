class Flight:
    """
    A class to represent a flight.
    """
    
    def __init__(self, departure, arrival, price, airline, departure_time, arrival_time, duration, airplane, travel_class, flight_number):
        """
        Initialize the Flight object with the necessary details.
        
        :param departure: str: Departure airport name
        :param arrival: str: Arrival airport name
        :param price: float: Flight price
        :param airline: str: Airline name
        :param departure_time: str: Departure time
        :param arrival_time: str: Arrival time
        :param duration: int: Flight duration in minutes
        :param airplane: str: Airplane type
        :param travel_class: str: Travel class (e.g., Economy, Business)
        :param flight_number: str: Flight number
        """
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
        """
        Return a string representation of the Flight object.
        
        :return: str: String representation of the Flight
        """
        return (f"Flight from {self.departure} to {self.arrival} with {self.airline} at ${self.price}, "
                f"departing at {self.departure_time}, arriving at {self.arrival_time}, "
                f"duration {self.duration} minutes, airplane {self.airplane}, class {self.travel_class}, "
                f"flight number {self.flight_number}")


class Hotel:
    """
    A class to represent a hotel.
    """
    
    def __init__(self, name, price):
        """
        Initialize the Hotel object with the necessary details.
        
        :param name: str: Hotel name
        :param price: float: Hotel price per night
        """
        self.name = name
        self.price = price
    
    def __repr__(self):
        """
        Return a string representation of the Hotel object.
        
        :return: str: String representation of the Hotel
        """
        return f"Hotel {self.name} at ${self.price}"
