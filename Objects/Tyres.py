# Tyres

class Tyres:
    # "type": [base_fric_coeff, dry_mult, cold_mult, light_rain_mult, heavy_rain_mult, dry_rate_deg, cold_rate_deg, light_rain_rate_deg, heavy_rain_rate_deg]
    tyres = {
            "soft": [1.8, 1.18, 1.0, 0.92, 0.80, 0.11, 0.09, 0.12, 0.13],
            "medium": [1.7, 1.08, 0.97, 0.88, 0.74, 0.10, 0.08, 0.09, 0.10],
            "hard": [1.6, 0.98, 0.92, 0.82, 0.68, 0.07, 0.06, 0.07, 0.08],
            "intermediate": [1.2, 0.90, 0.96, 1.08, 1.02, 0.14, 0.11, 0.08, 0.09],
            "wet": [1.1, 0.72, 0.88, 1.02, 1.20, 0.16, 0.12, 0.09, 0.05]
        }
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
        

        
           