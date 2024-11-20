from typing import List


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
    def __init__(self, cost: int, payment_time: str):
        self._cost = cost
        self._payment_time = payment_time


class Person:
    def __init__(self, name: Name, age: int):
        self._name = name
        self._age = age


class Passenger(Person):
    def __init__(self, ticket: Ticket, name: Name, age: int):
        super().__init__(name, age)
        self._ticket = ticket


class Transport:
    def __init__(self, license_plate: str,
                 passenger_capacity: int, driver: Person, passengers: List[Passenger]):
        self._license_plate = license_plate
        self._passenger_capacity = passenger_capacity
        self._driver = driver
        self._passengers = passengers


class TransportationCompany:
    def __init__(self, name: str, address: str, contact_info: str):
        self.name = name
        self.address = address
        self.contact_info = contact_info

class BusStop:
    def __init__(self, name: str, location: str):
        self._name = name
        self._location = location
        self._routes = []


class Bus(Transport):
    def __init__(self, route_number: str, bus_stops: List[BusStop], transportation_company: TransportationCompany, license_plate: str,
                 passenger_capacity: int, driver: Person, passengers: List[Passenger]):
        super().__init__(license_plate, passenger_capacity, driver, passengers)
        self._route_number = route_number
        self._bus_stops = bus_stops
        self._transportation_company = transportation_company


class Taxi(Transport):
    def __init__(self, departure_address: Address,
                 destination_address: Address,
                 travel_time: int, cost: int, license_plate: str,
                 passenger_capacity: int, driver: Person, passengers: List[Passenger]):
        super().__init__(license_plate, passenger_capacity, driver, passengers)
        self._departure_address = departure_address
        self._destination_address = destination_address
        self._travel_time = travel_time
        self._cost = cost
