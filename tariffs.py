import numpy as np
import pandas as pd
import datetime

class Tariffs :
    def __init__(self, scheme_name, retail_tariff_data_path, duos_data_path, tuos_data_path):
        self.scheme_name = scheme_name
        self.retail_tariff_data_path = retail_tariff_data_path
        self.duos_data_path = duos_data_path
        self.tuos_data_path = tuos_data_path
        # Get tariff data (note tuos not considered as yet)
        self.retail_tariff_data = pd.read_csv(retail_tariff_data_path, index_col = ['offer_name'])
        self.duos_tariff_data = pd.read_csv(duos_data_path, index_col = ['offer_name'])
        # print(self.retail_tariff_data)
        # print(self.duos_tariff_data)
    
    def get_variable_tariff(self, date_time, retail_tariff_type):
        """Variable tariff component from retail tariff data."""
        # Get data from df
        flat_charge = self.retail_tariff_data.loc[retail_tariff_type,'flat_charge']
        peak_charge	= self.retail_tariff_data.loc[retail_tariff_type,'peak_charge']
        shoulder_charge	= self.retail_tariff_data.loc[retail_tariff_type,'shoulder_charge']
        offpeak_charge = self.retail_tariff_data.loc[retail_tariff_type,'offpeak_charge']
        block_1_charge = self.retail_tariff_data.loc[retail_tariff_type,'block_1_charge']
        block_2_charge = self.retail_tariff_data.loc[retail_tariff_type,'block_2_charge']
        controlled_load	= self.retail_tariff_data.loc[retail_tariff_type,'controlled_load']
        peak_start_time	= self.retail_tariff_data.loc[retail_tariff_type,'peak_start_time']
        peak_end_time = self.retail_tariff_data.loc[retail_tariff_type,'peak_end_time']
        peak_start_time_2 = self.retail_tariff_data.loc[retail_tariff_type,'peak_start_time_2']
        peak_end_time_2	= self.retail_tariff_data.loc[retail_tariff_type,'peak_end_time_2']
        shoulder_start_time	= self.retail_tariff_data.loc[retail_tariff_type,'shoulder_start_time']
        shoulder_end_time = self.retail_tariff_data.loc[retail_tariff_type,'shoulder_end_time']
        shoulder_start_time_2 = self.retail_tariff_data.loc[retail_tariff_type,'shoulder_start_time_2']
        shoulder_end_time_2	= self.retail_tariff_data.loc[retail_tariff_type,'shoulder_end_time_2']
        block_1_volume = self.retail_tariff_data.loc[retail_tariff_type,'block_1_volume']
        block_2_volume = self.retail_tariff_data.loc[retail_tariff_type,'block_2_volume']
        demand_charge = self.retail_tariff_data.loc[retail_tariff_type,'demand']
        tou_weekday_only_flag = self.retail_tariff_data.loc[retail_tariff_type, 'tou_weekday_only_flag']

        if retail_tariff_type == 'Business Anytime':
            variable_tariff = (block_1_charge, block_2_charge, block_1_volume)

        if retail_tariff_type == 'Business TOU':
            variable_tariff = (peak_charge, shoulder_charge, offpeak_charge, peak_start_time, peak_end_time, peak_start_time_2, peak_end_time_2, shoulder_start_time, shoulder_end_time, shoulder_start_time_2, shoulder_end_time_2, tou_weekday_only_flag)

        if retail_tariff_type == 'Controlled Load 1':
            variable_tariff = (controlled_load)
        
        if retail_tariff_type == 'Controlled Load 2':
            variable_tariff = (controlled_load)

        return variable_tariff

    def get_local_solar_tariff(self,date_time):
        """Input in UI"""
        return 0.10

    def get_central_batt_tariff(self,date_time):
        """This is the tariff paid by the battery to the solar owner when importing solar."""
        """Input in UI"""
        return self.get_local_solar_tariff(date_time) + 0.02
    
    def get_retail_solar_tariff(self,date_time, retail_tariff_type, solar_capacity):
        """Solar FiT component from retail tariff data."""
        # Get solar threshold from retail data sheet
        solar_capacity_threshold = self.retail_tariff_data.loc[retail_tariff_type,'solar_cap_1']
        # If below or equal to the threshold, return the relevant solar rate in $/kWh. 
        if solar_capacity <= solar_capacity_threshold:
            retail_solar_tariff = self.retail_tariff_data.loc[retail_tariff_type,'solar_tariff_1']
        # Else return the rate for systems above the threshold.
        else :
            retail_solar_tariff = self.retail_tariff_data.loc[retail_tariff_type,'solar_tariff_2']
        return retail_solar_tariff
    
    def get_central_batt_buy_tariff(self,date_time):
        """This is the tariff paid by the participant to the battery when consuming battery export electricity."""
        """Input in UI"""
        return 0.14

    def get_fixed_tariff(self, fixed_period_minutes, retail_tariff_type):
        """Fixed tariff component from retail tariff data. Returns fixed value expressed per fixed period minutes (input)."""
        fixed_tariff = self.retail_tariff_data.loc[retail_tariff_type,'daily_charge'] * (float(fixed_period_minutes)/float(60*24))
        return fixed_tariff



    # Things the network is paid (fixed DUOS charges, variable DUOS charges, local solar DUOS charges, central battery DUOS charges)
    # Apply to amounts consumer each time period then sum for total network income
    def get_duos_on_grid_import_fixed(self,fixed_period_minutes, duos_tariff_type):
        fixed_tariff = self.duos_tariff_data.loc[duos_tariff_type,'daily_charge'] * (float(fixed_period_minutes)/float(60*24))
        return fixed_tariff

    def get_duos_on_grid_import_variable(self,date_time, duos_tariff_type):
        """Variable tariff component from DUOS tariff data."""
        # Get data from df
        flat_charge = self.duos_tariff_data.loc[duos_tariff_type,'flat_charge']
        peak_charge	= self.duos_tariff_data.loc[duos_tariff_type,'peak_charge']
        shoulder_charge	= self.duos_tariff_data.loc[duos_tariff_type,'shoulder_charge']
        offpeak_charge = self.duos_tariff_data.loc[duos_tariff_type,'offpeak_charge']
        block_1_charge = self.duos_tariff_data.loc[duos_tariff_type,'block_1_charge']
        block_2_charge = self.duos_tariff_data.loc[duos_tariff_type,'block_2_charge']
        controlled_load	= self.duos_tariff_data.loc[duos_tariff_type,'controlled_load']
        peak_start_time	= self.duos_tariff_data.loc[duos_tariff_type,'peak_start_time']
        peak_end_time = self.duos_tariff_data.loc[duos_tariff_type,'peak_end_time']
        peak_start_time_2 = self.duos_tariff_data.loc[duos_tariff_type,'peak_start_time_2']
        peak_end_time_2	= self.duos_tariff_data.loc[duos_tariff_type,'peak_end_time_2']
        shoulder_start_time	= self.duos_tariff_data.loc[duos_tariff_type,'shoulder_start_time']
        shoulder_end_time = self.duos_tariff_data.loc[duos_tariff_type,'shoulder_end_time']
        shoulder_start_time_2 = self.duos_tariff_data.loc[duos_tariff_type,'shoulder_start_time_2']
        shoulder_end_time_2	= self.duos_tariff_data.loc[duos_tariff_type,'shoulder_end_time_2']
        block_1_volume = self.duos_tariff_data.loc[duos_tariff_type,'block_1_volume']
        block_2_volume = self.duos_tariff_data.loc[duos_tariff_type,'block_2_volume']
        demand_charge = self.duos_tariff_data.loc[duos_tariff_type,'demand']
        tou_weekday_only_flag = self.duos_tariff_data.loc[duos_tariff_type, 'tou_weekday_only_flag']

        if duos_tariff_type == 'Controlled Load 1':
            variable_tariff = (controlled_load)

        if duos_tariff_type == 'Controlled Load 2':
            variable_tariff = (controlled_load)

        if duos_tariff_type == 'LV Small Business Anytime':
            variable_tariff = (flat_charge)           

        # Note, demand charge included in returned values to make calculations in main.py nicer to work with (avoid repeating TOU calcs for demand charge case)
        if duos_tariff_type == 'LV TOU <100MWh':
            variable_tariff = (peak_charge, shoulder_charge, offpeak_charge, peak_start_time, peak_end_time, peak_start_time_2, peak_end_time_2, shoulder_start_time, shoulder_end_time, shoulder_start_time_2, shoulder_end_time_2, tou_weekday_only_flag, demand_charge)
        
        # Note, demand charge included in returned values to make calculations in main.py nicer to work with (avoid repeating TOU calcs for demand charge case)
        if duos_tariff_type == 'LV Business TOU_Interval meter':
            variable_tariff = (peak_charge, shoulder_charge, offpeak_charge, peak_start_time, peak_end_time, peak_start_time_2, peak_end_time_2, shoulder_start_time, shoulder_end_time, shoulder_start_time_2, shoulder_end_time_2, tou_weekday_only_flag, demand_charge)

        if duos_tariff_type == 'Small Business - Opt in Demand':
            variable_tariff = (peak_charge, shoulder_charge, offpeak_charge, peak_start_time, peak_end_time, peak_start_time_2, peak_end_time_2, shoulder_start_time, shoulder_end_time, shoulder_start_time_2, shoulder_end_time_2, tou_weekday_only_flag, demand_charge)

        return variable_tariff

 

    def get_duos_on_local_solar_import(self,date_time):
        return 0.03

    def get_duos_on_central_batt_import(self,date_time):
        """This is the DUOS paid by the customer when consuming battery export."""
        return 0.01

    def get_duos_on_central_batt_solar_import(self,date_time):
        """This is the DUOS paid by the battery when importing local solar."""
        return 0.01

    # Transmission use of service charges - will presumably be zero for local solar and battery import
    def get_tuos_on_grid_import_fixed(self,fixed_period_minutes):
        return 0.0

    def get_tuos_on_grid_import_variable(self,date_time):
        return 0.0    

    def get_tuos_on_local_solar_import(self,date_time):
        return 0.0

    def get_tuos_on_central_batt_import(self,date_time):
        """This is the TUOS paid by the customer when consuming battery export."""
        return 0.0
    
    def get_tuos_on_central_batt_solar_import(self,date_time):
        """This is the TUOS paid by the battery when importing local solar."""
        return 0.0

    # Things the retailer is paid (fixed retail charges, variable retail charges, local solar retail charges, central battery retail charges)
    # Maybe unnecessary - could possibly subtract network income from customer bill
    def get_retail_income_on_grid_import_fixed(self,fixed_period_minutes):
        return 0.10

    def get_retail_income_on_grid_import_variable(self,date_time):
        return 0.05
    
    def get_retail_income_on_local_solar_import(self,date_time):
        return 0.04

    def get_retail_income_on_central_batt_import(self,date_time):
        """This is the retailer charge paid by the customer when consuming battery export."""
        return 0.04

    def get_retail_income_on_central_batt_solar_import(self,date_time):
        """This is the retailer charge paid by the battery when importing local solar."""
        return 0.01

    # Total battery import tariff (i.e. what the battery has to pay when importing energy) Includes energy payment + NUOS payment + retail payment
    def get_total_central_battery_import_tariff(self, date_time):
        total_battery_import_tariff = self.get_central_batt_tariff(date_time) + self.get_duos_on_central_batt_solar_import(date_time) + self.get_tuos_on_central_batt_solar_import(date_time) + self.get_retail_income_on_central_batt_solar_import(date_time)
        return total_battery_import_tariff


# test_tariff = Tariffs('test_scheme',"data/retail_tariffs.csv","data/duos.csv","test")
# print(test_tariff.get_variable_tariff(30,'Business TOU'))

