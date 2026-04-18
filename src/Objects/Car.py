# Car object

class Car:
    def __init__(self, max_speed, acc, brake, limp_const, crawl_const, fuel_tank_capacity, inital_fuel):
        self.max_speed = max_speed       # m/s
        self.acc = acc          # m_s^2
        self.brake = brake         # m/s^2
        self.limp_const = limp_const        # m/s
        self.crawl_const = crawl_const      # m/s
        self.fuel_tank_capacity = fuel_tank_capacity        # litres
        self.initial_fuel = inital_fuel         # litres

    

