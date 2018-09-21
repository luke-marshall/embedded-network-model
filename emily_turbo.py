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
from threading import Thread

# Required 3rd party libraries
import datetime
import pandas as pd
import numpy as np
import pprint
import csv
import os
import random
random.seed(9001)

#  ==================
# PROGRAM STARTS HERE
#  ==================
data_dir ='data'

def run(random_seed , dictlist, data_dir, participant_csv):

    print('Good morning!')
    # Directories where input and output data lives.
    output_dir = 'output'


    # Create a network - this stores information on the electricity network we want to model.
    mynetwork = Network('Byron')

    # Name the test you're running
    testname = '_25solar_flat_'

    solar_participant_fraction=0.25

    print('About to add participants')
    # Load the participants from a csv
    # unique_id = mynetwork.add_participants_from_csv_randomise_has_solar(data_dir,"emily_participant_meta_data_EN1.csv", solar_participant_fraction=solar_participant_fraction, random_seed=random_seed)
    unique_id = mynetwork.add_participants_from_dictlist_randomise_has_solar(dictlist, data_dir,"emily_participant_meta_data_EN1.csv", solar_participant_fraction=solar_participant_fraction, random_seed=random_seed)

    # unique_id = mynetwork.add_participants_from_dictlist_randomise_has_solar(dictlist, solar_participant_fraction=solar_participant_fraction, random_seed=random_seed)
    
    
    print('Successfully added participants', unique_id)
    # append the unique id to the test name.
    testname  += unique_id

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
    end = datetime.datetime(year=2012,month=7,day=1,hour=23,minute=30)     #end time for all data in emily_example
    # end =  datetime.datetime(year=2016,month=7,day=30,hour=23) #this is an end time very near the start, good for testing code because we don't do many calculations.
    # end =  datetime.datetime(year=2017,month=4,day=30,hour=23) #this is the total end time for all the data in the byron model

    # Generate a list of time periods in half hour increments, on which to run the simulation. These must be included in the input time series.
    time_periods = util.generate_dates_in_range(start, end, 30)
    # Create a results object to store the results of the simulations
    results = Results(time_periods, [p.get_id() for p in mynetwork.get_participants()])
    print(unique_id,'About to run simulation')
    # Perform energy simulations and store the results in our results object.
    energy_sim.simulate(time_periods, mynetwork, my_tariffs, results)
    print(unique_id, 'About to run financial sim')
    # Perform financial calculations based on the energy sim and store the results in our results object.
    financial_sim.simulate(time_periods, mynetwork, my_tariffs, results)
    # Print to CSV files
    print(unique_id, 'Outputting to files')
    out_path = os.path.join(output_dir, str(solar_participant_fraction))
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    results.to_csv(out_path, info_tag=testname)
    print(unique_id, 'Done')


if __name__ == "__main__":
    # if not os.path.isdir(os.path.join('output', 'test')):
    #     os.mkdir(os.path.join('output', 'test'))
    data_dir ='data'
    participant_csv = "emily_participant_meta_data_EN1.csv"
    with open(os.path.join(data_dir,participant_csv)) as f:
        reader = csv.DictReader(f, delimiter = ",")
        participants = [line for line in reader]

        for i in range(6):
            t = Thread(target=run, args=(i, participants, data_dir, participant_csv))
            t.start()
    # run()