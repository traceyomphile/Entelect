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
        
        

