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
    if accel_dist_to_max + brake_dist <= straight_length_m:
            return StraightPlan(
                target_mps=int(math.floor(max_speed)),
                brake_start_m_before_next=int(math.ceil(brake_dist)),
            )
    accel = self.effective_accel
    brake = self.effective_brake
    denom = (1.0 / (2.0 * accel)) + (1.0 / (2.0 * brake)) 
    numer = (
        straight_length_m
            + (entry_speed_mps ** 2) / (2.0 * accel)
            + (required_exit_speed_mps ** 2) / (2.0 * brake)
        )
    peak_speed = min(math.sqrt(max(0.0, numer / denom)), max_speed)

    target_speed = int(math.floor(peak_speed))
    target_speed = max(target_speed, int(math.ceil(required_exit_speed_mps)))

    brake_distance = self._braking_distance(
            float(target_speed),
            required_exit_speed_mps,
            self.effective_brake,
        )

    return StraightPlan(
            target_mps=target_speed,
            brake_start_m_before_next=int(math.ceil(brake_distance)),
        )
def _build_lap_segments(self, entry_speed_at_lap_start):
        current_speed = entry_speed_at_lap_start
        outputs = []
        index = 0
        total_segments = len(self.level.track.segments)

        while index < total_segments:
            segment = self.level.track.segments[index]

            if segment.type == "straight":
                required_exit_speed = self._next_corner_block_speed(index)
                straight_plan = self.plan_straight(
                    straight_length_m=segment.length_m,
                    entry_speed_mps=current_speed,
                    required_exit_speed_mps=required_exit_speed,
                )
                outputs.append(
                    {
                        "id": segment.id,
                        "type": "straight",
                        "target_m/s": straight_plan.target_mps,
                        "brake_start_m_before_next": straight_plan.brake_start_m_before_next,
                    }
                )
                current_speed = required_exit_speed
                index += 1
                continue

            if segment.type == "corner":
                if index == 0 or self.level.track.segments[index - 1].type != "corner":
                    current_speed = self._corner_block_speed_from(index)

                outputs.append({"id": segment.id, "type": "corner"})
                index += 1
                continue

            raise ValueError("Unknown segment type: " + str(segment.type))

        return outputs, current_speed

def _get_start_weather(self):
        weather_id = self.level.race.start_weather_cond
        for item in self.level.weather.conditions:
            if item.id == weather_id:
                return item
        raise ValueError("Starting weather id not found: " + str(weather_id))
def _compute_corner_safe_speeds(self):
        result = {}
        for segment in self.level.track.segments:
            if segment.type == "corner":
                if segment.radius_m is None:
                    raise ValueError("Corner segment is missing radius_m: " + str(segment.id))
                result[segment.id] = self.compute_safe_corner_speed(segment.radius_m)
        return result

def _corner_block_speed_from(self, start_index):
        if self.level.track.segments[start_index].type != "corner":
            raise ValueError("Corner block must start on a corner segment.")

        index = start_index
        block_speed = float("inf")
        while index < len(self.level.track.segments) and self.level.track.segments[index].type == "corner":
            block_speed = min(
                block_speed,
                self.corner_safe_speeds[self.level.track.segments[index].id],
            )
            index += 1
        return block_speed

def _next_corner_block_speed(self, straight_index):
        total_segments = len(self.level.track.segments)
        for offset in range(1, total_segments + 1):
            next_index = (straight_index + offset) % total_segments
            if self.level.track.segments[next_index].type == "corner":
                return self._corner_block_speed_from(next_index)
        raise ValueError("No corner found after straight.")

@staticmethod
def _acceleration_distance(initial_speed_mps, final_speed_mps, accel_mps2):
        if final_speed_mps <= initial_speed_mps:
            return 0.0
        return ((final_speed_mps ** 2) - (initial_speed_mps ** 2)) / (2.0 * accel_mps2)

@staticmethod
def _braking_distance(initial_speed_mps, final_speed_mps, brake_mps2):
        if final_speed_mps >= initial_speed_mps:
            return 0.0
        return ((initial_speed_mps ** 2) - (final_speed_mps ** 2)) / (2.0 * brake_mps2)


def main():
    if len(sys.argv) != 3:
        print("Usage: python level1.py <input_json_file> <output_json_file>")
        return 1

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    level = LevelData.from_file(input_path)
    solver = level1(level)
    result = solver.solve()

    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)

    print("Level 1 output written to " + output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
                                     
    
                
            

       

