# Track

class Segment:
    def __init__(self, segment_id, segment_type, length_m, radius_m=None):
        self.id = segment_id
        self.type = segment_type
        self.length_m = length_m
        self.radius_m = radius_m

class Track:
    degradation_types = {
        "K_STRAIGHT": 0.0000166,
        "K_BRAKING": 0.0398,
        "K_CORNER": 0.000265
    }
    
    def __init__(self, name, segments):
        self.name = name
        self.segments = segments
        