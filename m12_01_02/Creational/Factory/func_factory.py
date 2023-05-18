class Dog:
    def __init__(self, name):
        self.name = name
        self.sound = 'Woof!'

    def say(self):
        return self.sound


class Cat:
    def __init__(self, name):
        self.name = name
        self.sound = 'Meow!'

    def say(self):
        return self.sound


def get_pet(type_pet="dog"):
    pets = {
        "dog": Dog('Bobik'),
        "cat": Cat('Simon')
    }
    return pets.get(type_pet)


if __name__ == '__main__':
    dog = get_pet('dog')
    print(dog.say())

    cat = get_pet('cat')
    print(cat.say())
