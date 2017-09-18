
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
    "net_export" : pd.DataFrame(index = time_periods, columns=[p.get_id() for p in mynetwork.get_paricipants()]),
    "TBC" : pd.DataFrame(index = time_periods, columns=[p.get_id() for p in mynetwork.get_paricipants()])
    }
# print(data_output)


for time in time_periods:
    # Calc each participant in/out kWh
    for p in mynetwork.get_paricipants():
        data_output['net_export'].loc[time,p.get_id()] = p.calc_net_export(time, 30)

    # Calc exces solar sharing / sales
    network_net_excess = mynetwork.calc_total_participant_export(time, 30)

    # Calc central battery in/out kWh


    # Calc network in.out kWh

print(data_output)