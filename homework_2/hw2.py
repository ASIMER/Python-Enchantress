from abc import ABC, abstractmethod
from random import randint
from datetime import date
from threading import Lock
from homework_2.exceptions import *

# all houses stored in set, because order is not important
HOUSES = set()
# all realtors stored in set, because order is not important.
# unless realtors is singleton, I want to create scalable code
REALTORS = set()


class House:
    """House class, which describe simple house
    cost - how much one house cost in $, can't be less than 20000$,
    area - house area, can't be less than 40 square meters,
    discount - house discount, which can be from 0% to 100% of house cost"""

    def __init__(self, cost, area, discount = 0):
        self.cost = cost
        self.area = area
        self.discount = discount

    @property
    def area(self):
        return self._area

    @area.setter
    def area(self, area):
        if area < 40:
            raise HouseToSmallError
        else:
            self._area = area

    @property
    def discount(self):
        return self._discount

    @discount.setter
    def discount(self, discount):
        if not (discount >= 0) and (discount <= 1):
            raise DiscountValueError
        else:
            self._discount = discount

    @property
    def cost(self):
        return self._cost * (1 - self._discount)

    @cost.setter
    def cost(self, cost):
        if cost < 20000:
            raise HouseCostError
        else:
            self._cost = cost


class Human(ABC):
    """Human abstract class,
    money - start capital,
    name - human name,
    birth_date - date of birth, datetime,
    buildings - set of buildings (houses etc)"""
    # save money
    buildings = set()

    def __init__(self, name, birth_date, money):
        self.name = name
        self.birth_date = birth_date
        self.money = money

    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, birth_date: date):
        birth = date.today() - birth_date
        if birth.days <= 0:
            raise HumanBirthDateError
        else:
            self._birth_date = birth_date

    @abstractmethod
    def make_money(self, salary):
        raise NotImplementedError('Not implemented make_money method')

    def buy_house(self, house: House):
        if self.money < house.cost:
            raise HumanNoMoneyError
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
    """simple person class,
    only can buy houses or get them without buying (presents),
    also can make_money, but job not implemented yet
    """
    def make_money(self, salary):
        self.money += salary


class Realtor(Human):
    """Realtor class (singleton),
    money - start capital,
    name - human name,
    birth_date - date of birth, datetime,
    buildings - set of buildings (houses etc),
    houses_for_sell - set of houses which realtor can sell
    """
    __metaclass__ = RealtorMeta
    houses_for_sell = set()

    def sell_house(self, house: House, person: Person):
        # sell house to person, with cash withdraw
        # applies discount for house cost (in property method)
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
        # return realtor houses discounts
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
    HOUSES.add(House(99999, 46))
    HOUSES.add(House(99999, 48))
    HOUSES.add(House(99999, 90))
