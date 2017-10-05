import numpy as np
import pandas as pd
import datetime

class Battery:
    def __init__(self, cap_kWh, cap_kW, cycle_eff):
        """Make note: cycle efficiency must be between zero and one."""
        self.cap_kWh = cap_kWh
        self.cap_kW = cap_kW
        self.cycle_eff = cycle_eff
        self.charge_level_kWh = 0  
        self.num_cycles = 0      

    def charge(self, kWh):
        # Increase battery charge level by the input kWh
        amount_to_charge = min(self.cap_kWh - self.charge_level_kWh, kWh)
        self.charge_level_kWh += amount_to_charge * self.cycle_eff
        return kWh - amount_to_charge

    def discharge(self, kWh_request):
        discharge_amount = min(kWh_request, self.charge_level_kWh)
        self.charge_level_kWh -= discharge_amount
        self.num_cycles += float(discharge_amount) / float(self.cap_kWh)
        return discharge_amount

    def get_num_cycles(self):
        return self.num_cycles

class Central_Battery(Battery):
    def __init__(self, cap_kWh, cap_kW, cycle_eff, ui_battery_discharge_windows_path):
        Battery.__init__(self, cap_kWh, cap_kW, cycle_eff)
        self.ui_battery_discharge_windows_path = ui_battery_discharge_windows_path
        self.discharge_times_data = pd.read_csv(ui_battery_discharge_windows_path)
        # print(self.discharge_times_data)
    
    def make_export_decision(self, net_participant_kWh, date_time):
        """Takes amount of available energy (positive = can charge, negative = there is demand on the network). Makes a decision about whether to charge or discharge. 
        Returns positive if discharging, negative if charging."""
        # Case where there is energy available to charge
        if net_participant_kWh >= 0 :
            # Charge - note this returns what ever is left over after charging
            return (net_participant_kWh - self.charge(net_participant_kWh)) * -1
        
        # Case where there is demand on the network
        else :
            # Hours which discharge is allowed (note midnight is 00:00)
            all_hours = pd.Series(list(range(0,24,1)))
            # allowed_discharge_hours = 
            # allowed_discharge_hours = allowed_discharge_hours[allowed_discharge_hours == ]
            # Check whether hour limitation applies
            if date_time.hour in all_hours:
                return self.discharge(abs(net_participant_kWh))
        
        

my_batt = Central_Battery(10,5,0.9,"data/ui_battery_discharge_window_eg.csv")

allowed_discharge_hours = pd.Series(list(range(0,24,1)))
print(allowed_discharge_hours)
