# Track

class Track:
    degration_types = {
        "K_STRAIGHT": 0.0000166,
        "K_BRAKING": 0.0398,
        "K_CORNER": 0.000265
    }
    
    def __init__(self, name, segments, id, type, length, radius, ):
        self.name = name
        self.segments = segments
        self.id = id
        self.type = type    
        self.length = length
        self.radius = radius

    def 

        