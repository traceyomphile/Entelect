import json
import math
import sys

from src.Objects.Track import Track, Segment
from src.Objects.Tyres import Tyres, AvailableTyreSet, TyreProperties 
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
    
    def from_dict(cls, data):
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
                    corner_crash_penalty=race_data['corner_crash_penalty_s'],

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
        if sets_data is  None:
          sets_data=data.get('available_sets',[])
        for item in sets_data:
            available_sets.append(AvailableTyreSet(ids=item['ids'], compound=item['compound']))
        tyres= Tyres(properties=tyre_properties, available_sets=available_sets)

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

def compute_safe_corner_speed(self, radius_m):
    return math.sqrt(self.tyre_friction*9.8*radius_m)+self.level.car.crawl_const

def plan_straight(self, straight_length_m, entry_speed_mps, required_exit_speed_mps):
    max_speed= self.level.car.max_speed
    accel_dist_to_max = self._acceleraation_distance(entry_speed_mps,max_speed,self.effective_accel,)
    brake_dist=self._braking_distance(max_speed,required_exit_speed_mps,self.effective_brake,)

    

                                               
    
                
            

       

