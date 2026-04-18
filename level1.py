import json
import math
import sys

from src.Objects.Track import Track
from src.Objects.Tyres import Tyres 
from src.Objects.Car import Car
from src.Objects.Weather import Weather
from src.Objects.Race import Race 

class LevelData:
    def __init__(self,car,race,track,tyres,weather):
        self.car = car
        self.race=race
        self.track=track
        self.tyres=tyres
        self.weather=weather
    
    def from_dict(self, data):
        car_data= data['car']
        race_data= data["race"]
        track_data= data["track"]
        tyres_data= data["tyres"]
        weather_data= data["weather"]

class StraightPlan:
    def __init__(self, target_mps,brake_start):
        self.target_mps=target_mps
        self.brake_start=brake_start

class level1:
    def __init__(self, level):
        self.level=level
        self.start_weather=self .start._get_start_weather()
        self.effective_accel=self.car.acc* self.start_weather.acc_mult
        self.effective_brake=self.level.car.brake * self.start_weather.dec_mult  
        self.init_tyre_id, self_init_compound =self.choose_init_tyre()
        self.tyre_friction= self.compute_tyre_friction(
            self.init_compoud,
            self.start_weather.condition,
        )
        self.corner_safe_speeds= self. _compute_corner_safe_speed ()
    
    def solve(self):
        laps =[]
        current_speed =0.0
        for lap_number in range(1, self.level.race.laps +1):
            lap_segments, current_speed = self._build_lap_segment(current_speed)
            laps.append({
                "lap": lap_number,
                "segments":lap_segments,
                "pit":{"enter":false},
            })
        

