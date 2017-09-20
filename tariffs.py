import numpy as np

class Tariffs :
    def __init__(self, scheme_name):
        self.scheme_name = scheme_name
    
    def get_variable_tariff(self, date_time):
        return 0.30

    def get_local_solar_tariff(self,date_time):
        return 0.10

    def get_central_batt_tariff(self,date_time):
        return self.get_local_solar_tariff(date_time) + 0.02
    
    def get_retail_solar_tariff(self,date_time):
        return 0.06
    
    def get_central_batt_buy_tariff(self,date_time):
        return 0.08

    def get_fixed_tariff(self, fixed_period_minutes):
        return 1.20 * (fixed_period_minutes/(60*24))

