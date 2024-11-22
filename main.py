from typing import List


class CustomError(Exception):
    pass


class Name:
    def __init__(self, surname: str, name: str):
        self.surname = surname
        self.name = name


class Address:
    def __init__(self, city: str, street: str, house: int):
        self.city = city
        self.street = street
        self.house = house


class Ticket:
    def __init__(self, cost: int, payment_time: str):
        self.cost = cost
        self.payment_time = payment_time


class Person:
    def __init__(self, name: Name, age: int):
        self._name = name
        self._age = age


class Passenger(Person):
    def __init__(self, passenger_id: int,
                 ticket: Ticket, name: Name, age: int):
        super().__init__(name, age)
        self.__passenger_id = passenger_id
        self._ticket = ticket

    def get_passenger_id(self):
        return self.__passenger_id


class Transport:
    def __init__(self, passengers: List[Passenger], license_plate: str,
                 passenger_capacity: int, driver: Person):
        self._passengers = passengers
        self.__current_passenger_id = 1
        self._license_plate = license_plate
        self._passenger_capacity = passenger_capacity
        self._driver = driver

    def add_passenger(self, ticket: Ticket, name: Name, age: int):
        if (self.__current_passenger_id + 1) > self._passenger_capacity:
            raise CustomError("Can`t add passenger, transport is full")
        passenger = Passenger(self.__current_passenger_id, ticket, name, age)
        self._passengers.append(passenger)
        self.__current_passenger_id += 1
        return passenger

    def read_all_passengers(self):
        return self._passengers

    def read_by_passenger_id(self, passenger_id: int):
        for passenger in self._passengers:
            if passenger.get_passenger_id() == passenger_id:
                return passenger
        return None

    def update_passenger(self, passenger_id: int, name: Name = None,
                         age: int = None, ticket=None) -> bool:
        passenger = self.read_by_passenger_id(passenger_id)
        if passenger:
            if name is not None:
                    passenger.name = name
            if age is not None:
                if age > 0:
                    passenger.age = age
                else:
                    raise ValueError("age must be positive int")
            if ticket is not None:
                 passenger.ticket = ticket
            return True
        return False

    def delete_passenger(self, passenger_id: int) -> bool:
        passenger = self.read_by_passenger_id(passenger_id)
        if passenger:
            self._passengers.remove(passenger)
            return True
        return False


class TransportationCompany:
    def __init__(self, name: str, address: str, contact_info: str):
        self.name = name
        self.address = address
        self.contact_info = contact_info


class Route:
    def __init__(self, route_id: int, number_route: str):
        self.__route_id = route_id
        self._number_route = number_route

    def get_route_id(self):
        return self.__route_id

class BusStop:
    def __init__(self, bus_id: int, name: str, location: str,
                 routes: List[Route]):
        self.__current_route_id = 1
        self._bus_id = bus_id
        self._name = name
        self._location = location
        self._routes = routes

    def add_route(self, number_route):
        route = Route(self.__current_route_id, number_route)
        self._routes.append(route)
        self.__current_route_id += 1
        return route

    def read_all_routes(self):
        return self._routes

    def read_by_route_id(self, route_id):
        for route in self._routes:
            if route.get_route_id() == route_id:
                return route
        return None

    def update_route(self, route_id: int, number_route: str) -> bool:
        route = self.read_by_route_id(route_id)
        if route:
            route._number_route = number_route
            return True
        return False

    def delete_route(self, route_id: int) -> bool:
        route = self.read_by_route_id(route_id)
        if route:
            self._routes.remove(route)
            return True
        return False


class Bus(Transport):
    def __init__(self, route_number: str,
                 transportation_company: TransportationCompany,
                 passengers: List[Passenger], license_plate: str,
                 passenger_capacity: int, driver: Person):
        super().__init__(passengers, license_plate, passenger_capacity, driver)
        self._route_number = route_number
        self._transportation_company = transportation_company


class Taxi(Transport):
    def __init__(self, departure_address: Address,
                 destination_address: Address,
                 travel_time: int, cost: int, passengers: List[Passenger],
                 license_plate: str, passenger_capacity: int, driver: Person):
        super().__init__(passengers, license_plate, passenger_capacity, driver)
        self._departure_address = departure_address
        self._destination_address = destination_address
        self._travel_time = travel_time
        self._cost = cost
