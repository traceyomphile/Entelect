# Weather

class Weather:
    def __init__(self, condition, id, duration, acc_mult, dec_mult):
        self.condition = condition  # defaulr is dry
        self.id = id
        self.duration = duration
        self.acc_mult = acc_mult
        self.dec_mult = dec_mult

        