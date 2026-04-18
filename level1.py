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
                "pit":{"enter":False},
            })
        
        return {
            "initial_tyre_id": self.init_tyre_id,
            "laps": laps,
        }
        
def choose_init_tyre(self):
    best_id= None
    best_compound= None
    best_friction=-1.0

    for tyre_set in self.level.tyres.available_sets:
        friction=self.compute_tyre_friction(
            tyre_set.compound,
            self.start_weather.condition,
        )
        if friction > best_friction:
            best_friction=friction
            best_compound=tyre_set.compound
            best_id= tyre_set.ids[0]

    if best_id is None or best_compound is None:
        raise ValueError("No tyre sets available")
    return best_id, best_compound
def compute_tyre_friction(self, compound, weather_condition):
    base= Tyres.tyres[compound][0]
    props= self.level.tyres.properties[compound]

    if weather_condition == "dry":
        multiplier= props.dry_friction_mult
    elif weather_condition =="cold":
        multiplier= props.cold_friction_mult
    elif weather_condition =="light_rain":
        multiplier= props.light_rain_friction_mult
    elif weather_condition =="heavy_rain":
        multiplier= props.heavy_rain_friction_mult
    else:
        raise ValueError("Unsupported weather condition: "+ str(weather_condition))
    
    return base * multiplier

def compute_safe_corner_speed(self, radius_m)
    return math.sqrt(self.tyre_friction*9.8*radius_m)+self.level.car.crawl_const

def plan_straight(self, straight_length_m, entry_speed_mps, required_exit_speed_mps):
    max_speed= self.level.car.max_speed
    accel_dist_to_max = self._acceleraation_distance(entry_speed_mps,max_speed,self.effective_accel,)
    brake_dist=self._braking_distance(max_speed,required_exit_speed_mps,self.effective_brake,)

    

