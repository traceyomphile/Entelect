# Race

class Race:
    def __init__(self, name, laps, pit_tyr_swap_time, base_pit_stp_time, pit_refuel_rate, corner_crash_penalty, pit_exit_speed, fuel_soft_cap_limiy, start_weather_cond):
        self.name = name
        self.laps = laps
        self.pit_tyr_swap_time = pit_tyr_swap_time
        self.base_pit_stp_time = base_pit_stp_time
        self.pit_refuel_rate = pit_refuel_rate
        self.corner_crash_penalty = corner_crash_penalty
        self.pit_exit_speed = pit_exit_speed
        self.fuel_soft_cap_limiy = fuel_soft_cap_limiy
        self.start_weather_cond = start_weather_cond
        