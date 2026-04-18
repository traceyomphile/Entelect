import json
import math
import sys

from sympy import Segment

from Objects.Track import Track
from Objects.Tyres import Tyres 
from Objects.Car import Car
from Objects.Weather import Weather
from Objects.Race import Race 

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

        car = Car(max_speed=car_data['max_speed_m/s'],
                  acc=car_data['accel_m/se2'],
                  brake=car_data['brake_m/se2'],
                  limp_const=car_data['limp_const_m/s'],
                  crawl_const=car_data['crawl_const_m/s'],
                  fuel_tank_capacity=car_data.get('fuel_tank_capacity_l', 0.0),  # Default to 0 if not provided
                  inital_fuel=car_data.get('inital_fuel_l', 0.0),
        )
        race = Race(name=race_data['name'],
                    laps=race_data['laps'],
                    pit_tyr_swap_time=race_data.get('pit_tyr_swap_time_s',0.0),
                    base_pit_stp_time=race_data.get('base_pit_stp_time_s',0.0),
                    pit_refuel_rate=race_data.get('pit_refuel_rate_l/s',0.0),
                    corner_crash_penalty=race_data['corner_crash_penalty_s']

                    pit_exit_speed=race_data.get('pit_exit_speed_m/s',0.0),
                    fuel_soft_cap_limiy=race_data.get('fuel_soft_cap_limiy_l',0.0),
                    start_weather_cond=race_data['start_weather_condition_id'],
    )
        segments=[]
        for item in track_data['segments']:
            segments.append(Segment(segment_id=item['id'], 
                            segment_type=item['type'], 
                            length_m=item['length_m'], 
                            radius_m=item.get('radius_m')
                            ))
        track = Track(name=track_data['name'],segments=segments)
        tyre_properties ={}
        for compound, props in tyres_data['properties'].items():
            tyre_properties[compound] = TyreProperties(
                compound=compound,
                life_span=props['life_span'],
                dry_friction_mult=props['dry_friction_multiplier'],
                cold_friction_mult=props['cold_friction_multiplier'],
                light_rain_friction_mult=props['light_rain_friction_multiplier'],
                heavy_rain_friction_mult=props['heavy_rain_friction_multiplier'],
                dry_degradation_mult=props['dry_degradation'],
                cold_degradation_mult=props['cold_degradation'],
                light_rain_degradation_mult=props['light_rain_degradation'],
                heavy_rain_degradation_mult=props['heavy_rain_degradation'],
            )
        available_sets=[]
        sets_data=tyres_data.get('available_sets')
        if sets data is  None:
          sets_data=data.get('available_sets',[])
        for item in sets_data:
            available_sets.append(AvailableTyreSet(ids=item['ids'], compound=item['compound']))
        tyres= Tyers(properties=tyre_properties, available_sets=available_sets)

        conditions=[]
        for item in weather_data['conditions']:
            conditions.append(Weather( condition_id=item['id'],
                                        condition=item['condition'],
                                        duration=item['duration_s'], 
                                        acc_mult=item['acc_multiplier'],
                                        dec_mult=item['dec_multiplier']))

        weather = Weather(conditions=conditions)
        return cls(car=car, race=race, track=track, tyres=tyres, weather=weather)

def from_file(cls, file_path):
    with open(file_path, 'r', encoding='utf-8') as handle:
     return cls.from_dict(json.load(handle))
                                                
                                                
    
                
            

       

