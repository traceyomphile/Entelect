# Weather

class WeatherCondition:
    def __init__(self, condition_id, condition, duration, acc_mult, dec_mult):
        self.id = condition_id
        self.condition = condition
        self.duration = duration
        self.acc_mult = acc_mult
        self.dec_mult = dec_mult

class Weather:
    def __init__(self, conditions):
        self.conditions = conditions

        