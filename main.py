from typing import List
import json
import xml.etree.ElementTree as ET
import os


class CustomError(Exception):
    pass


class CapacityError(CustomError):
    def __init__(self, transport_id):
        self.message = f"Can`t add passenger, transport with id {transport_id} is full"
        super().__init__(self.message)


class TransportNotFoundError(CustomError):
    def __init__(self, vehicle_id):
        self.message=f"Transport with id {vehicle_id} not found"
        super().__init__(self.message)


class InvalidVehicleDataError(CustomError):
    def __init__(self, message):
        super().__init__(message)


class IODataBaseError(CustomError):
    def __init__(self, message):
        super().__init__(message)


class FileError(CustomError):
    def __init__(self, filename, message):
        super().__init__(f"{filename}: {message}")


class Name:
    def __init__(self, surname: str, name: str):
        self.surname = surname
        self.name = name

    def to_dict(self):
        return {
            "surname": self.surname,
            "name": self.name
        }

    def from_dict(self, data):
        self.surname = data["surname"]
        self.name = data["name"]


class Address:
    def __init__(self, city: str, street: str, house: int):
        self.city = city
        self.street = street
        self.house = house

    def to_dict(self):
        return {
            "city": self.city,
            "street": self.street,
            "house": self.house
        }

    def from_dict(self, data):
        self.city = data["city"]
        self.street = data["street"]
        self.house = data["house"]


class Ticket:
    def __init__(self, cost: int, payment_time: str):
        self.cost = cost
        self.payment_time = payment_time

    def to_dict(self):
        return {
            "cost": self.cost,
            "payment_time": self.payment_time
        }

    def from_dict(self, data):
        self.cost = data["cost"]
        self.payment_time = data["payment_time"]


class Person:
    def __init__(self, name: str, age: int):
        if not isinstance(name, str):
            raise TypeError("Name must be str")
        if not isinstance(age, int) or age < 0:
            raise ValueError("Age must be positive int")
        self.name = name
        self.age = age

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age
        }

    def from_dict(self, data):
        self.name = data["name"]
        self.age = data["age"]


class Passenger(Person):
    def __init__(self, passenger_id: int,
                 ticket: Ticket, name: str, age: int):
        super().__init__(name, age)
        self.__passenger_id = passenger_id
        self.ticket = ticket

    def get_passenger_id(self):
        return self.__passenger_id

    def to_dict(self):
        return {
            "passenger_id": self.__passenger_id,
            "name": self.name,
            "age": self.age,
            "ticket": self.ticket.to_dict()
        }

    def from_dict(self, data):
        self.__passenger_id = data["passenger_id"]
        self.name = data["name"]
        self.age = data["age"]
        self.ticket.from_dict(data["ticket"])


class Transport:
    def __init__(self, transport_id: int, passengers: List[Passenger],
                 license_plate: str, passenger_capacity: int, driver: Person):
        self.__transport_id = transport_id
        if len(passengers) <= passenger_capacity:
            self._passengers = passengers
        else:
            raise CapacityError(self.__transport_id)
        self.__current_passenger_id = 1
        self._license_plate = license_plate
        self._passenger_capacity = passenger_capacity
        self._driver = driver

    def get_transport_id(self):
        return self.__transport_id

    def add_passenger(self, ticket: Ticket, name: str, age: int):
        if (self.__current_passenger_id + 1) > self._passenger_capacity:
            raise CapacityError(self.__transport_id)
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

    def update_passenger(self, passenger_id: int, name: str = None,
                         age: int = None, ticket=None) -> bool:
        passenger = self.read_by_passenger_id(passenger_id)
        if passenger:
            if name is not None:
                if isinstance(name, str):
                    passenger.name = name
                else:
                    raise TypeError("Name must be str")
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

    def to_dict(self):
        return {
            "transport_id": self.__transport_id,
            "license_plate": self._license_plate,
            "passenger_capacity": self._passenger_capacity,
            "driver": self._driver.to_dict(),
            "passengers": {
                f"passenger_{passenger.get_passenger_id()}":
                    passenger.to_dict() for passenger in self._passengers
            }
        }

    def from_dict(self, data):
        self.__transport_id = data["transport_id"]
        self._license_plate = data["license_plate"]
        self._passenger_capacity = data["passenger_capacity"]
        self._driver.from_dict(data["driver"])
        for i, pas in data['passengers'].items():
            passenger = Passenger(0, Ticket(0, ""), "", 0)
            passenger.from_dict(pas)
            self._passengers.append(passenger)


class TransportationCompany:
    def __init__(self, name: str, address: str, contact_info: str):
        self.name = name
        self.address = address
        self.contact_info = contact_info

    def to_dict(self):
        return {
            "name": self.name,
            "address": self.address,
            "contact_info": self.contact_info
        }

    def from_dict(self, data):
        self.name = data["name"]
        self.address = data["address"]
        self.contact_info = data["contact_info"]


class Bus(Transport):
    def __init__(self, route_number: str,
                 transportation_company: TransportationCompany,
                 transport_id: int, passengers: List[Passenger],
                 license_plate: str, passenger_capacity: int, driver: Person):
        super().__init__(transport_id, passengers, license_plate,
                         passenger_capacity, driver)
        self._route_number = route_number
        self._transportation_company = transportation_company

    def to_dict(self):
        data = Transport.to_dict(self)
        data["route_number"] = self._route_number
        data["transportation_company"] = self._transportation_company.to_dict()\
            if not isinstance(self._transportation_company, dict)\
            else self._transportation_company
        return data

    def from_dict(self, data):
        Transport.from_dict(self, data)
        self._route_number = data["route_number"]
        self._transportation_company = data["transportation_company"]


class TransportDataBase:
    def __init__(self, filename: str):
        self.__transport = {}
        self.__filename = filename

    def add_transport(self, transp: Transport):
        if transp in self.__transport:
            raise InvalidVehicleDataError(
                f"Transport {transp.get_transport_id()} already exists")
        self.__transport[f"{transp.get_transport_id()}"] = transp.to_dict()\
            if not isinstance(transp, dict) else transp

    def get_transport(self, transport_id: int) -> Transport:
        if transport_id not in self.__transport:
            raise TransportNotFoundError(transport_id)
        return self.__transport[transport_id]

    def update_transport(self, transport_id: int, transport: Transport):
        if transport_id not in self.__transport:
            raise TransportNotFoundError(transport_id)
        self.__transport[transport_id] = transport

    def delete_vehicle(self, transport_id: int):
        if transport_id not in self.__transport:
            raise TransportNotFoundError(transport_id)
        self.__transport.pop(transport_id)

    def to_json(self, filename: str):
        try:
            with open(filename, "w") as file:
                json.dump(self.__transport, file, indent = 4)
        except Exception as ex:
            print(f"JSON error: {ex}")

    def from_json(self, filename: str):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
            for transport_id, transport_data in data.items():
                transport = Bus("", TransportationCompany("","", ""),
                                0, [], "", 0, Person("", 0))
                transport.from_dict(transport_data)
                self.add_transport(transport)
        except Exception as ex:
            print(f"Error when load from JSON: {ex}")

def main():
    db1 = TransportDataBase("db1.json")
    db2 = TransportDataBase("copy_db1.json")
    passenger1 = Passenger(1, Ticket(55, "8:30"), "Aleksey", 19)
    passenger2 = Passenger(2, Ticket(55, "9:00"), "Vladimir", 19)
    passenger3 = Passenger(3, Ticket(55, "9:00"), "Nikita", 20)
    bus1 = Bus("404",
               TransportationCompany("MosGorTrans", "Moscow", "88005553535"),
               1, [passenger1, passenger2, passenger3], "X333XX", 1,
               Person("Vodila", 52))
    bus2 = Bus("400",
               TransportationCompany("MosGorTrans", "Moscow", "88005553535"),
               2, [passenger1, passenger2, passenger3], "X332XX", 100,
               Person("Vodila", 52))
    db1.add_transport(bus1)
    db1.add_transport(bus2)
    db1.to_json("Bus.json")
    db2.from_json("Bus.json")
    db2.to_json("copy_Bus.json")


if __name__ == "__main__":
    try:
        main()
    except CapacityError as ex:
        print(ex)
    except TransportNotFoundError as ex:
        print(ex)
    except InvalidVehicleDataError as ex:
        print(ex)
    except IODataBaseError as ex:
        print(ex)
    except FileError as ex:
        print(ex)
    except Exception as ex:
        print(ex)