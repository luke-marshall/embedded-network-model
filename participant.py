import numpy as np
import pandas as pd
import datetime

class Participant: 
    def __init__(self, participant_id, participant_type, tariff_type, retailer):
        self.participant_id = participant_id
        self.participant_type = participant_type
        self.tariff_type = tariff_type
        self.retailer = retailer
    
    def print_attributes(self):
        print(self.participant_type, self.tariff_type, self.retailer)

    # TODO - make this work
    def calc_net_export(self, date_time, interval_min):
        return np.random.uniform(-10,10) 

    def get_id(self):
        return self.participant_id

class CSV_Participant(Participant):
    def __init__(self, participant_id, participant_type, tariff_type, retailer, solar_path, load_path, solar_capacity):
        Participant.__init__(self, participant_id, participant_type, tariff_type, retailer)
        solar_data = pd.read_csv(solar_path,index_col = 'HHE', parse_dates=True)
        load_data = pd.read_csv(load_path,index_col = 'date_time', parse_dates=True)
        # Delete all cols not relevant to this participant
        self.load_data = load_data[participant_id]
        # Apply capacity to solar data
        self.solar_data = solar_data['solar']
        self.solar_data = solar_data * solar_capacity

    def calc_net_export(self, date_time, interval_min):
        solar_data = float(self.solar_data.loc[date_time])
        load_data = float(self.load_data.loc[date_time])
        net_export = solar_data - load_data
        return net_export


        # print(solar_data)
        # print(load_data)

participant = CSV_Participant('participant_1','solar', 'A', 'ENOVA',"data/bb_pvoutput_solar_data_26_feb_1_may.csv", "data/essential_load_data_aie_26_feb_1_may.csv",8)

print(participant.calc_net_export(datetime.datetime(year=2017,month=2,day=27,hour=1),30))