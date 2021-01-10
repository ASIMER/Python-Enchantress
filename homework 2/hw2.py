from abc import ABC, abstractmethod
from random import randint
from datetime import date
from threading import Lock

HOUSES = set()
REALTORS = set()


class House:
    _cost = 20000
    _area = 40
    _discount: float = 0

    def __init__(self, cost, area):
        self.cost = cost
        self.area = area

    @property
    def area(self):
        return self._area

    @area.setter
    def area(self, area):
        if area < 40:
            raise Exception("House too small")
        else:
            self._area = area

    @property
    def discount(self):
        return self._discount

    @discount.setter
    def discount(self, discount):
        if discount < 0:
            raise Exception("Discount is negative")
        else:
            self._discount = discount

    @property
    def cost(self):
        return self._cost * (1 - self._discount)

    @cost.setter
    def cost(self, cost):
        if cost < 20000:
            Exception("House too low cost")
        else:
            self._cost = cost


class Human(ABC):
    # save money
    money = 0
    buildings = set()
    name: str
    _birth_date: date

    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, birth_date: date):
        birth = date.today() - birth_date
        if birth.days <= 0:
            raise Exception('too low birth date')
        else:
            self._birth_date = birth_date

    @abstractmethod
    def make_money(self, salary):
        raise NotImplementedError('Not implemented make_money method')

    def buy_house(self, house: House):
        if self.money < house.cost:
            raise Exception("Human hasn't enough money")
        self.money -= house.cost
        self.buildings.add(house)
        HOUSES.discard(house)
        for r in REALTORS:
            r.houses_for_sell.discard(house)

    # for inheritance and presents
    def add_house(self, house):
        self.buildings.add(house)

    def get_age(self):
        from_birth = date.today() - self.birth_date
        return from_birth.days // 365

    def get_personal_information(self):
        return {'name': self.name,
                'birth': self.birth_date,
                'money': self.money}


class RealtorMeta(type):
    # multi thread realization of singleton
    _instances = {}
    # I'm lock all threads
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(cls, *args, **kwargs)
                cls._instances[cls] = instance
            return cls._instances[cls]


class Person(Human):
    def __init__(self, name, birth_date, money):
        self.name = name
        self.birth_date = birth_date
        self.money = money

    def make_money(self, salary):
        self.money += salary


class Realtor(Human):
    __metaclass__ = RealtorMeta
    houses_for_sell = set()

    def __init__(self, name, birth_date, money):
        self.name = name
        self.birth_date = birth_date
        self.money = money

    def sell_house(self, house: House, person: Person):
        salary = 0
        # steal money with 10% chance
        if randint(1, 101) < 10:
            salary += house.cost * 0.05

        salary += house.cost * 0.05
        person.money -= house.cost + salary
        self.make_money(salary)
        HOUSES.discard(house)
        self.houses_for_sell.discard(house)

    def get_discounts(self):
        return [house.discount for house in self.houses_for_sell]

    def add_house_to_sell(self, house: House):
        self.houses_for_sell.add(house)

    def make_money(self, salary):
        self.money += salary


if __name__ == '__main__':
    realtor = Realtor(name='Ivan',
                      birth_date=date(year=1998, day=11, month=11),
                      money=999999)
    REALTORS.add(realtor)
    person1 = Person(name='Irma',
                     birth_date=date(year=1998, day=11, month=11),
                     money=999999)
    person2 = Person(name='Alex',
                     birth_date=date(year=1998, day=11, month=11),
                     money=99999)
    HOUSES.add(House(99999, 45))
    HOUSES.add(House(9999, 46))
    HOUSES.add(House(9999, 48))
    HOUSES.add(House(9999, 90))
