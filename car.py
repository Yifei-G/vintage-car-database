

class Car:

    def __init__(self, id, brand, model, product_year, convertible):
        self.id = id
        self.brand = brand
        self.model = model
        self.production_year = product_year
        self.convertible = convertible

    def jsonEncoder(car):
        if isinstance(car, Car):
            return car.__dict__
        else:
            raise TypeError(car.__class__.__name__ + "is not JSON seriazable")
