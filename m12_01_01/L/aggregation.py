class Animal:
    def __init__(self, nickname, age):
        self.nickname = nickname
        self.age = age

    def get_info(self):
        return f"{self.nickname}: {self.age}"


class Owner:
    def __init__(self, fullname, phone):
        self.fullname = fullname
        self.phone = phone

    def call_phone(self):
        print(f"Call phone {self.phone}")


class Cat(Animal):
    def __init__(self, nickname, age, owner: Owner):
        super().__init__(nickname, age)
        self.owner = owner

    def say(self):
        return f"{self.nickname} say meow!"


if __name__ == '__main__':
    owner = Owner('Sergiy', 1234567)
    cat = Cat('Mur4ik', 6, owner)
