class Name:
    def __init__(self, surname: str, name: str):
        self._surname = surname
        self._name = name


class Address:
    def __init__(self, city: str, street: str, house: int):
        self._city = city
        self._street = street
        self._house = house


class Ticket:
    def __init__(self, cost: int, departure_address: Address,
                 destination_address: Address):
        self._cost = cost
        self._departure_address = departure_address
        self._destination_address = destination_address


class Transport:
    def __init__(self, license_plate: str,
                 passenger_capacity: int, driver: Name):
        self._license_plate = license_plate
        self._passenger_capacity = passenger_capacity
        self._driver = driver
        self.passengers = []


class Passenger:
    def __init__(self, name: Name, age: int, ticket: Ticket):
        self._name = name
        self._age = age
        self._ticket = ticket


class Bus(Transport):
    def __init__(self, route_number: str, bus_stops: list, license_plate: str,
                 passenger_capacity: int, driver: Name):
        super().__init__(license_plate, passenger_capacity, driver)
        self._route_number = route_number
        self._bus_stops = bus_stops


class Taxi(Transport):
    def __init__(self, departure_address: Address,
                 destination_address: Address, taxi_type: str,
                 travel_time: int, cost: int, license_plate: str,
                 passenger_capacity: int, driver: Name):
        super().__init__(license_plate, passenger_capacity, driver)
        self._departure_address = departure_address
        self._destination_address = destination_address
        self._taxi_type = taxi_type
        self._travel_time = travel_time
        self._cost = cost
