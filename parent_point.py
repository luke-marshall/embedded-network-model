# Custom modules
from network import Network
from participant import Participant, CSV_Participant
from battery import Battery, Central_Battery
from tariffs import Tariffs
import util
from results import Results

# Required 3rd party libraries
import datetime
import pandas as pd
import numpy as np
import pprint
import csv
import os

TIME_PERIOD_LENGTH_MINS = 30




if retail_tariff_type == 'Business TOU':
                peak_charge, shoulder_charge, offpeak_charge, peak_start_time, peak_end_time, peak_start_time_2, peak_end_time_2, shoulder_start_time, shoulder_end_time, shoulder_start_time_2, shoulder_end_time_2, tou_weekday_only_flag = my_tariffs.get_variable_tariff(time,retail_tariff_type)

                # If the TOU periods apply all days and not just weekdays then the flag will be zero
                if tou_weekday_only_flag == 0 :
                    # Check for whether it's a peak time
                    if (time.hour > peak_start_time and time.hour <= peak_end_time) or (time.hour > peak_start_time_2 and time.hour <= peak_end_time_2) :
                        variable_tariff = peak_charge
                    # If not, check whether it's shoulder time
                    elif (time.hour > shoulder_start_time and time.hour <= shoulder_end_time) or (time.hour > shoulder_start_time_2 and time.hour <= shoulder_end_time_2) :
                        variable_tariff = shoulder_charge
                    else:
                        variable_tariff = offpeak_charge
