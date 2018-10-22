# =====================================================
# Imports - these are external bits of code that we use to make the model run properly.
# =====================================================

# Custom modules
from network import Network
from participant import Participant, CSV_Participant
from battery import Battery, Central_Battery
from tariffs import Tariffs
import util
from results import Results
import energy_sim
import financial_sim

# Required 3rd party libraries
import datetime
import pandas as pd
import numpy as np
import pprint
import csv
import os

#  ==================
# PROGRAM STARTS HERE
#  ==================
print('Good morning!')
# Directories where input and output data lives.
output_dir = 'output'
data_dir ='data'

# Create a network - this stores information on the electricity network we want to model.
mynetwork = Network('Byron')

# Name the test you're running
testname = '_25solar_flat'

print('About to add participants')
# Load the participants from a csv
mynetwork.add_participants_from_csv(data_dir,"emily_participant_meta_data_EN1.csv")
print('Successfully added participants')

# Create a central battery
battery_capacity = 0.00000001
central_battery = Central_Battery(cap_kWh=battery_capacity, cap_kW=battery_capacity, cycle_eff=0.99, ui_battery_discharge_windows_path=os.path.join(data_dir,"ui_battery_discharge_window_eg.csv"))
# Add the battery to the network.
mynetwork.add_central_battery(central_battery)
print('Successfully added battery')

# Create a 'tariffs' object that stores information and logic about different tariffs.
my_tariffs = Tariffs('Test',os.path.join(data_dir,"retail_tariffs.csv"),os.path.join(data_dir,"duos.csv"),os.path.join(data_dir,"tuos.csv"), os.path.join(data_dir,"nuos.csv"), os.path.join(data_dir,"ui_tariffs_eg.csv"))

# Define the start and end times of the simulation.
start = datetime.datetime(year=2012,month=7,day=1,hour=0,minute=30)     #start time for all data in emily_example
end = datetime.datetime(year=2013,month=6,day=30,hour=23,minute=30)     #end time for all data in emily_example
# end =  datetime.datetime(year=2016,month=7,day=30,hour=23) #this is an end time very near the start, good for testing code because we don't do many calculations.
# end =  datetime.datetime(year=2017,month=4,day=30,hour=23) #this is the total end time for all the data in the byron model

# Generate a list of time periods in half hour increments, on which to run the simulation. These must be included in the input time series.
time_periods = util.generate_dates_in_range(start, end, 30)
# Create a results object to store the results of the simulations
results = Results(time_periods, [p.get_id() for p in mynetwork.get_participants()])
print('About to run simulation')
# Perform energy simulations and store the results in our results object.
energy_sim.simulate(time_periods, mynetwork, my_tariffs, results)
print('About to run financial sim')
# Perform financial calculations based on the energy sim and store the results in our results object.
financial_sim.simulate(time_periods, mynetwork, my_tariffs, results)
# Print to CSV files
results.to_csv(output_dir, info_tag=testname)
