# 3. Create metaclass with inheritance
class MetaCheburek(type):
    def __new__(mcs, class_name, *args, **kwargs):
        print("We are created Cheburek class object")
        class_obj = super().__new__(mcs, class_name, *args, **kwargs)
        class_obj.ingredients = ['Potato, Cheese, Salad']
        return class_obj


class Food:
    pass


class Cheburek(food,
               metaclass=MetaCheburek):
    pass


print('class object', Cheburek)
print('object', Cheburek())
