class HouseToSmallError(Exception):
    def __init__(self):
        super().__init__("House too small")


class DiscountValueError(Exception):
    def __init__(self):
        super().__init__("Discount should be from 0 to 1")


class HouseCostError(Exception):
    def __init__(self):
        super().__init__("House too low cost")


class HumanBirthDateError(Exception):
    def __init__(self):
        super().__init__('Too low birth date')


class HumanNoMoneyError(Exception):
    def __init__(self):
        super().__init__("Human hasn't enough money")