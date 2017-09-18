
from network import Network
from participant import Participant
from battery import Battery, Central_Battery
import util
import datetime
import pandas as pd
import numpy as np

# Create a network
mynetwork = Network('Byron')

# Create participants
participant_1 = Participant('building_1','solar', 'A', 'ENOVA')
participant_2 = Participant('building_2','load', 'B', 'ENOVA')

# Add participants to network
mynetwork.add_participant(participant_1)
mynetwork.add_participant(participant_2)

# Add a central battery
battery_1 = Central_Battery(10.0, 5.0, 0.99)
mynetwork.add_central_battery(battery_1)

# At each time period...
time_periods = util.generate_dates_in_range(datetime.datetime.now() - datetime.timedelta(weeks = 4), datetime.datetime.now(), 30)
# Make empty df
data_output = {
    "df_net_export" : pd.DataFrame(index = time_periods, columns=[p.get_id() for p in mynetwork.get_paricipants()]),
    "df_network_energy_flows" : pd.DataFrame(index = time_periods, columns=['net_participant_export', 'central_battery_export'])
    }
# print(data_output)


for time in time_periods:
    # Calc each participant in/out kWh
    for p in mynetwork.get_paricipants():
        data_output['df_net_export'].loc[time,p.get_id()] = p.calc_net_export(time, 30)

    # Calc exces solar sharing / sales
    net_participant_export =  mynetwork.calc_total_participant_export(time, 30)
    data_output['df_network_energy_flows'].loc[time, 'net_participant_export'] = net_participant_export
    
    # Calc central battery in/out kWh
    central_battery_export = mynetwork.get_batteries()[0].make_export_decision(net_participant_export)
    data_output['df_network_energy_flows'].loc[time, 'central_battery_export'] = central_battery_export

    # Calc network in/out kWh
    data_output['df_network_energy_flows'].loc[time, 'net_network_export'] = net_participant_export + central_battery_export

print(data_output)