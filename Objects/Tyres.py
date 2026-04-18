# Tyres

class Tyres:
    def __init__(self, available_sets, ids, compound, life_span, dry_friction_mult, cold_friction_mult, light_rain_friction_mult, heavy_rain_friction_mult, dry_degradation_mult, cold_degradation_mult, light_rain_degradation_mult, heavy_rain_degradation_mult):
        self.available_sets = available_sets
        self.ids = ids
        self.compound = compound
        self.life_span = life_span
        self.dry_friction_mult = dry_friction_mult
        self.cold_friction_mult = cold_friction_mult
        self.light_rain_friction_mult = light_rain_friction_mult
        self.heavy_rain_friction_mult = heavy_rain_friction_mult
        self.dry_degradation_mult = dry_degradation_mult
        self.cold_degradation_mult = cold_degradation_mult
        self.light_rain_degradation_mult = light_rain_degradation_mult
        self.heavy_rain_degradation_mult = heavy_rain_degradation_mult
        
           