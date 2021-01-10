# 1. Create a class hierarchy of animals with at
#    least 5 animals that have additional methods each.

class Carnivora:
    sound: str

    def __init__(self, animal_name):
        self.name = animal_name

    def make_a_sound(self):
        print(self.sound)


class Canidae(Carnivora):
    lags = 4

    def run(self):
        pass


class Feliformia(Carnivora):
    pass


class Dog(Canidae):
    sound = 'gow'

    def find_drugs(self):
        pass


class Wolf(Canidae):
    sound = 'Oooooooooooooooowhoo'
    def hunt_deer(self):
        pass


class Fox(Canidae):
    sound = 'yow-wow-wow'
    def hunt_birds(self):
        pass


class Cat(Feliformia):
    sound = 'meow'

    def destroy_sofa(self):
        pass

    def climb_tree(self):
        pass


class Lynx(Feliformia):
    sound = 'meow'
    def hunt_grouse(self):
        pass
