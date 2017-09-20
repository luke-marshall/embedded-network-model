
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
    "df_net_export" : pd.DataFrame(index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]),
    "df_network_energy_flows" : pd.DataFrame(index = time_periods, columns=['net_participant_export', 'central_battery_export', 'unallocated_local_solar']),
    "df_local_solar_import" : pd.DataFrame(index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()])
    }
# print(data_output)


for time in time_periods:
    # Calc each participant in/out kWh
    for p in mynetwork.get_participants():
        data_output['df_net_export'].loc[time,p.get_id()] = p.calc_net_export(time, 30)

    # Calc exces solar sharing / sales
    net_participant_export =  mynetwork.calc_total_participant_export(time, 30)
    data_output['df_network_energy_flows'].loc[time, 'net_participant_export'] = net_participant_export
    
    # Calc central battery in/out kWh
    central_battery_export = mynetwork.get_batteries()[0].make_export_decision(net_participant_export)
    data_output['df_network_energy_flows'].loc[time, 'central_battery_export'] = central_battery_export

    # Calc network in/out kWh
    data_output['df_network_energy_flows'].loc[time, 'net_network_export'] = net_participant_export + central_battery_export

    # Run local solar allocation algorithm
    # Create a sorted list of participants and their net export
    participants_list_sorted = pd.DataFrame(columns=['net_export'])
    
    for p in mynetwork.get_participants():
        # Get data point from df_net_export df
        net_export = data_output['df_net_export'].loc[time, p.get_id()]
        # If there is load (i.e. export < 0 ) add to list
        if net_export < 0 :
            participants_list_sorted.loc[p.get_id(), 'net_export'] = net_export
    # Sort list
    participants_list_sorted = participants_list_sorted.sort_values('net_export')

    # Calculate solar available in this time period
    available_solar = 0
    for col in data_output['df_net_export']:
        net_export = data_output['df_net_export'].loc[time, col]
        if net_export > 0 :
            available_solar += net_export
    
    if len(participants_list_sorted) != 0 :
        # Calculate solar allocation - assume even split between participants with load
        solar_allocation = float(available_solar) / float(len(participants_list_sorted))
        num_remaining_participants = len(participants_list_sorted)

        for p in participants_list_sorted.index.values :
            local_solar_import = min(abs(solar_allocation), abs(participants_list_sorted.loc[p, 'net_export']))
            data_output["df_local_solar_import"].loc[time, p] = local_solar_import
            # Find reject solar
            reject_solar = solar_allocation - local_solar_import
            # Find new available solar (based on what was used)
            available_solar -= local_solar_import
            # Decrement the number of remaining participants
            num_remaining_participants -= 1
            solar_allocation = float(available_solar) / float(num_remaining_participants) if num_remaining_participants > 0 else 0
    data_output["df_network_energy_flows"].loc[time, 'unallocated_local_solar'] = available_solar

# print(participants_list_sorted)
print(data_output['df_local_solar_import'])