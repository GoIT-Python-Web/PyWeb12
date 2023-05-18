class Car:
    def __init__(self):
        self.type = None

    def get_type(self):
        return self.type


class SportCar(Car):
    def __init__(self):
        super().__init__()
        self.type = 'Sport Car'


class ElectroCar(Car):
    def __init__(self):
        super().__init__()
        self.type = 'Elector Car'


class FactoryCar:
    def __init__(self):
        self.cars = {}

    def register(self, car_type, car_class):
        self.cars[car_type] = car_class

    def create(self, car_type):
        if car_type not in self.cars:
            raise ValueError(f"Invalid car type {car_type}")
        return self.cars.get(car_type)()


if __name__ == '__main__':
    factory = FactoryCar()
    factory.register('sports', SportCar)
    factory.register('electro', ElectroCar)

    car = factory.create('electro')
    print(car.get_type())
