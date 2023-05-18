class PersonPhoneNumber:
    def __init__(self, code, phone):
        self.phone = phone
        self.code = code

    def value_of(self):
        return f'+380{self.code}{self.phone}'


class PersonAddress:
    def __init__(self, zip, city, street):
        self.zip = zip
        self.city = city
        self.street = street

    def value_of(self):
        return f'{self.zip}, {self.city}, {self.street}'


class Person:
    def __init__(self, name, address, phone):
        self.name = name
        self.address = address
        self.phone = phone

    def get_address(self):
        return self.address.value_of()

    def get_phone(self):
        return self.phone.value_of()


if __name__ == '__main__':
    person = Person('Alexander', PersonAddress('36007', 'Poltava', 'European, 28'), PersonPhoneNumber('50', '1234567'))
    print(person.get_address())
    print(person.get_phone())
