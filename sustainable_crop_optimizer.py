"""
Precision Agriculture AI: Evapotranspiration & Soil Moisture Optimization
Author: Akash V (@akashvenkey)
"""
import numpy as np

class SmartIrrigationOptimizer:
    def __init__(self, field_capacity=30.0, wilting_point=12.0):
        self.field_capacity = field_capacity
        self.wilting_point = wilting_point

    def compute_evapotranspiration(self, temp_c, solar_rad_mj, humidity_pct):
        """Hargreaves-Samani formulation for reference evapotranspiration (ET0)."""
        et0 = 0.0023 * (temp_c + 17.8) * np.sqrt(max(0, temp_c - 10)) * (solar_rad_mj / 2.45)
        humidity_factor = (100 - humidity_pct) / 100.0
        return max(0.0, et0 * (1 + 0.1 * humidity_factor))

    def evaluate_water_deficit(self, current_moisture, daily_et):
        threshold = self.wilting_point + 0.5 * (self.field_capacity - self.wilting_point)
        if current_moisture < threshold:
            needed_liters_m2 = (self.field_capacity - current_moisture) * 1.2 + daily_et
            return True, round(needed_liters_m2, 2)
        return False, 0.0

if __name__ == "__main__":
    opt = SmartIrrigationOptimizer()
    et = opt.compute_evapotranspiration(temp_c=28.5, solar_rad_mj=18.2, humidity_pct=55)
    irrigate, liters = opt.evaluate_water_deficit(current_moisture=18.0, daily_et=et)
    print(f"Daily ET0: {et:.2f} mm/day | Irrigation Needed: {irrigate} ({liters} L/m²)")