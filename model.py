
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

DEFAULT_LOAD_DATA_PATH = "data/essential_load_data_aie_26_feb_1_may.csv"
def getParticipantNames():
    f = open(DEFAULT_LOAD_DATA_PATH, 'rb')
    reader = csv.reader(f)
    headers = reader.next()
    headers.remove("date_time")
    return headers

def run_en(scenario= None, status_callback=None, data_dir='data'):
    
    TIME_PERIOD_LENGTH_MINS = 30

    # Create a network
    mynetwork = Network('Byron')

    # Create participants

    participant_1 = CSV_Participant('participant_1','solar', 'Business TOU', 'LV TOU <100MWh','ENOVA',os.path.join(data_dir,"bb_pvoutput_solar_data_26_feb_1_may.csv"), os.path.join(data_dir,"essential_load_data_aie_26_feb_1_may.csv"),0)
    participant_2 = CSV_Participant('participant_2','solar', 'Business TOU', 'LV TOU <100MWh','ENOVA',os.path.join(data_dir,"bb_pvoutput_solar_data_26_feb_1_may.csv"), os.path.join(data_dir,"essential_load_data_aie_26_feb_1_may.csv"),0)
    participant_3 = CSV_Participant('participant_3','solar', 'Business TOU', 'LV TOU <100MWh','ENOVA',os.path.join(data_dir,"bb_pvoutput_solar_data_26_feb_1_may.csv"), os.path.join(data_dir,"essential_load_data_aie_26_feb_1_may.csv"),0)
    participant_4 = CSV_Participant('participant_4','solar', 'Business TOU', 'LV TOU <100MWh','ENOVA',os.path.join(data_dir,"bb_pvoutput_solar_data_26_feb_1_may.csv"), os.path.join(data_dir,"essential_load_data_aie_26_feb_1_may.csv"),26)
    participant_5 = CSV_Participant('participant_5','solar', 'Business TOU', 'LV TOU <100MWh','ENOVA',os.path.join(data_dir,"bb_pvoutput_solar_data_26_feb_1_may.csv"), os.path.join(data_dir,"essential_load_data_aie_26_feb_1_may.csv"),0)
    participant_6 = CSV_Participant('participant_6','solar', 'Business TOU', 'LV TOU <100MWh','ENOVA',os.path.join(data_dir,"bb_pvoutput_solar_data_26_feb_1_may.csv"), os.path.join(data_dir,"essential_load_data_aie_26_feb_1_may.csv"),14.8)
    participant_7 = CSV_Participant('participant_7','solar', 'Business TOU', 'LV TOU <100MWh','ENOVA',os.path.join(data_dir,"bb_pvoutput_solar_data_26_feb_1_may.csv"), os.path.join(data_dir,"essential_load_data_aie_26_feb_1_may.csv"),0)
    participant_8 = CSV_Participant('participant_8','solar', 'Business TOU', 'LV TOU <100MWh','ENOVA',os.path.join(data_dir,"bb_pvoutput_solar_data_26_feb_1_may.csv"), os.path.join(data_dir,"essential_load_data_aie_26_feb_1_may.csv"),27.5)
    participant_9 = CSV_Participant('participant_9','solar', 'Business Anytime', 'LV Small Business Anytime','ENOVA',os.path.join(data_dir,"bb_pvoutput_solar_data_26_feb_1_may.csv"), os.path.join(data_dir,"essential_load_data_aie_26_feb_1_may.csv"),3)
    participant_10 = CSV_Participant('participant_10','solar', 'Business Anytime', 'LV Small Business Anytime','ENOVA',os.path.join(data_dir,"bb_pvoutput_solar_data_26_feb_1_may.csv"), os.path.join(data_dir,"essential_load_data_aie_26_feb_1_may.csv"),0)
    participant_11 = CSV_Participant('participant_11','solar', 'Business Anytime', 'LV Small Business Anytime','ENOVA',os.path.join(data_dir,"bb_pvoutput_solar_data_26_feb_1_may.csv"), os.path.join(data_dir,"essential_load_data_aie_26_feb_1_may.csv"),0)

    # participant_1 = Participant('building_1','solar','Business TOU','LV TOU <100MWh', 'ENOVA')
    # participant_2 = Participant('building_2','load','Business TOU','Small Business - Opt in Demand', 'ENOVA')
    # participant_3 = Participant('building_3','load','Business TOU','Small Business - Opt in Demand', 'ENOVA')


    # Add participants to network
    mynetwork.add_participant(participant_1)
    mynetwork.add_participant(participant_2)
    mynetwork.add_participant(participant_3)
    mynetwork.add_participant(participant_4)
    mynetwork.add_participant(participant_5)
    mynetwork.add_participant(participant_6)
    mynetwork.add_participant(participant_7)
    mynetwork.add_participant(participant_8)
    mynetwork.add_participant(participant_9)
    mynetwork.add_participant(participant_10)
    mynetwork.add_participant(participant_11)
   

    # Add a central battery
    # See if the user has configured a battery capacity - if not, just use 1 MWh
    capacity = scenario['battery_capacity'] if 'battery_capacity' in scenario else 1
    # Create the battery object.
    battery_1 = Central_Battery(capacity, capacity, 0.99, os.path.join(data_dir,"ui_battery_discharge_window_eg.csv"))
    # Add the battery to the network.
    mynetwork.add_central_battery(battery_1)

    # Add tariffs
    # my_tariffs = Tariffs('Test',os.path.join(data_dir,"retail_tariffs.csv"),os.path.join(data_dir,"duos.csv",)"test")
    my_tariffs = Tariffs('Test',os.path.join(data_dir,"retail_tariffs.csv"),os.path.join(data_dir,"duos.csv"),os.path.join(data_dir,"tuos.csv"), os.path.join(data_dir,"nuos.csv"), os.path.join(data_dir,"ui_tariffs_eg.csv"))
    # Generate a list of time periods in half hour increments
    start = datetime.datetime(year=2017,month=2,day=26,hour=4)
    end =  datetime.datetime(year=2017,month=2,day=26,hour=23)
    # end =  datetime.datetime(year=2017,month=4,day=30,hour=23)
    time_periods = util.generate_dates_in_range(start, end, 30)
    

   

    results = Results(time_periods, [p.get_id() for p in mynetwork.get_participants()])
    
    if status_callback:
        status_callback('Performing Energy Calculations: 0%')
        percent_finished = 0
        single_step_percent = 100.0 / float(len(time_periods))
        
    for time in time_periods:
        if status_callback:
            percent_finished += single_step_percent
            status_callback('Performing Energy Calculations: '+str(round(percent_finished))+"%")
        # print "Energy",time
        # Calc each participant in/out kWh
        for p in mynetwork.get_participants():
            results.set_net_export(time, p.get_id(), p.calc_net_export(time, 30))

        
        # Calc exces solar sharing / sales
        net_participant_export =  mynetwork.calc_total_participant_export(time, 30)
        results.set_net_participant_export(time, net_participant_export)
        
        # Calc central battery in/out kWh
        central_battery_export = sum(b.make_export_decision(net_participant_export, time) for b in mynetwork.get_batteries())
        # central_battery_export = sum(b.make_export_decision(net_participant_export) for b in mynetwork.get_batteries())

        results.set_central_battery_export(time, central_battery_export)

        # Calc network in/out kWh
        results.set_net_network_export(time, net_participant_export + central_battery_export)

        # Run local solar allocation algorithm
        # Initialise an empty df with column name net_export
        participants_list_sorted = pd.DataFrame(columns=['net_export'])
        # Add net export data for participants with load
        for p in mynetwork.get_participants():
            # Get data point from df_net_export df
            net_export = results.get_net_export(time, p.get_id())
            # If there is load (i.e. export < 0 ) add to list
            if net_export < 0 :
                participants_list_sorted.loc[p.get_id(), 'net_export'] = net_export
        # Sort list of participants with load
        participants_list_sorted = participants_list_sorted.sort_values('net_export')

        # Calculate total solar available in this time period
        available_batt = max(central_battery_export,0)
        available_solar = 0
        for participant in mynetwork.get_participants():
            net_export = results.get_net_export(time, participant.get_id())
            if net_export > 0 :
                available_solar += net_export
        
        
        # If there exist participants with load then allocate solar
        if len(participants_list_sorted) != 0 :
            # Calculate solar allocation - assume even split between participants with load
            num_remaining_participants = len(participants_list_sorted)
            solar_allocation = float(available_solar) / float(num_remaining_participants)
            battery_allocation = float(available_batt) / float(num_remaining_participants)

            # Initialise for use in second if statement
            reject_solar = 0

            # For each participant with load, find how much of their allocated solar is consumed and calculate the leftover ('reject solar')
            for p in participants_list_sorted.index.values :
                if solar_allocation > 0:
                    # Allocating solar 
                    local_solar_import = min(abs(solar_allocation), abs(participants_list_sorted.loc[p, 'net_export']))
                    results.set_local_solar_import(time, p, local_solar_import)
                    # Find reject solar
                    reject_solar = solar_allocation - local_solar_import
                    # Find new available solar (based on what was used)
                    available_solar -= local_solar_import
                    # Decrement the number of remaining participants
                    num_remaining_participants -= 1
                    # Calculate the new solar allocation
                    solar_allocation = float(available_solar) / float(num_remaining_participants) if num_remaining_participants > 0 else 0
                # If the sale doesn't happen, then these things should be zero
                else :
                    reject_solar = 0
                    local_solar_import = 0

                # Allocate battery export when there is battery export and all solar has been used by this participant
                if battery_allocation > 0 and reject_solar <= 0 :
                    participant_net_export = participants_list_sorted.loc[p,'net_export']
                    participant_central_batt_import = min(abs(battery_allocation), abs(participant_net_export) - abs(local_solar_import))
                    results.set_participant_central_batt_import(time, p, participant_central_batt_import)
                    available_batt -= participant_central_batt_import
                    battery_allocation = float(available_batt) / float(num_remaining_participants) if num_remaining_participants > 0 else 0

                    
        # Save any solar left over after the allocation process to df_network_energy_flows
        results.set_unallocated_local_solar(time, available_solar)

        # Run local load allocation algorithm (aka solar sales)
        # Initialise an empty df with column name net export
        solar_sales_participant_list = pd.DataFrame(columns = ['net_export'])
        # Add net export data for participants with generation
        for p in mynetwork.get_participants():
            # Get data point from df_net_export df
            net_export = results.get_net_export(time, p.get_id())
            # If there is generation (i.e. export > 0 ) add to list
            if net_export > 0 :
                solar_sales_participant_list.loc[p.get_id(), 'net_export'] = net_export
        # Sort list of participants with load
        solar_sales_participant_list = solar_sales_participant_list.sort_values('net_export')

        # Calculate total load available in this time period
        # TODO - central battery
        available_load = 0
        available_batt_charging_load = abs(min(central_battery_export,0))

        #     # NOTE available load is positive
        #     if net_export < 0 :
        #         available_load += abs(net_export)

        for participant in mynetwork.get_participants():
            net_export = results.get_net_export(time, participant.get_id())
            # NOTE available load is positive
            if net_export < 0 :
                available_load += abs(net_export)

        # If there exists participant with solar, allocate load
        if len(solar_sales_participant_list) != 0 :
            num_remaining_participants = len(solar_sales_participant_list)
            load_allocation = float(available_load) / float(num_remaining_participants)
            batt_charging_allocation = float(available_batt_charging_load) / float(num_remaining_participants)

            for p in solar_sales_participant_list.index.values :
                if load_allocation > 0:
                    participant_solar_sale = min(abs(load_allocation), abs(solar_sales_participant_list.loc[p,'net_export']))
                    results.set_local_solar_sales(time, p, participant_solar_sale)
                    reject_load = load_allocation - participant_solar_sale
                    available_load -= participant_solar_sale
                    num_remaining_participants -= 1
                    load_allocation = float(available_load) / float(num_remaining_participants) if num_remaining_participants > 0 else 0
                # If the sale doesn't happen, then these things should be zero
                else :
                    reject_load = 0
                    participant_solar_sale = 0

                if available_batt_charging_load > 0 and reject_load <= 0 :
                    participant_solar_sale = min(abs(batt_charging_allocation), abs(solar_sales_participant_list.loc[p,'net_export']) - abs(participant_solar_sale))
                    results.set_central_batt_solar_sales(time, p, participant_solar_sale)
                    available_batt_charging_load -= participant_solar_sale
                    batt_charging_allocation = float(available_batt_charging_load) / float(num_remaining_participants) if num_remaining_participants > 0 else 0



        # Grid impacts for each customer. Import from grid and solar export to grid.
        for p in mynetwork.get_participants():
            # First, solar export to grid
            net_export = results.get_net_export(time, p.get_id())
            local_solar_sales = results.get_local_solar_sales(time, p.get_id())
            central_battery_solar_sales = results.get_central_batt_solar_sales(time, p.get_id())
            # Calc and save to df
            export_to_grid_solar_sales = max(0,net_export) - max(0,local_solar_sales) - max(0,central_battery_solar_sales)
            results.set_export_to_grid_solar_sales(time, p.get_id(), export_to_grid_solar_sales)
            # Then, electricity import from grid
            local_solar_import = results.get_local_solar_import(time, p.get_id())
            participant_central_batt_import = results.get_participant_central_batt_import(time, p.get_id())
            # Left over load which requires grid import. Calc and save to df.
            external_grid_import = abs(min(net_export,0)) - abs(max(0,local_solar_import)) - abs(max(0,participant_central_batt_import))
            results.set_external_grid_elec_import(time, p.get_id(), external_grid_import)

        # Save any battery load left over after the allocation process to df_network_energy_flows
        results.set_unallocated_central_battery_load(time, available_batt_charging_load)
        
        # For the financial calcs for retailer/NSPs, calculate the gross grid import - i.e. how much did all the participants import during this time interval (only considers import - discards export). Also local solar and central battery import.
        results.set_gross_participant_grid_import(time, abs(min(results.get_net_participant_export(time),0)))
        results.set_gross_participant_local_solar_import(time, max( sum([results.get_local_solar_import(time, participant.get_id()) for participant in mynetwork.get_participants() ]) ,0))
        results.set_gross_participant_central_battery_import(time, max( sum( [results.get_participant_central_batt_import(time, participant.get_id()) for participant in mynetwork.get_participants()] ),0))


    
        

    # ----------------------------------------------------------------------------------------------------------------------------
    # Financial flows

    # Charges are positive (if earning money then negative). Revenue is positive when earning money.
    financial_output = {
        "df_participant_variable_charge" : pd.DataFrame(0,index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]),
        "df_local_solar_import_charge" : pd.DataFrame(0,index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]), 
        "df_central_batt_import_charge" : pd.DataFrame(0,index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]), 
        "df_local_solar_sales_revenue" : pd.DataFrame(0,index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]), 
        "df_central_batt_solar_sales_revenue" : pd.DataFrame(0,index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]),
        "df_export_to_grid_solar_sales_revenue" : pd.DataFrame(0,index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]),
        "df_fixed_charge" : pd.DataFrame(0,index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]),
        "df_total_participant_bill" : pd.DataFrame(0,index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]),
        # The df_participant_duos_payments df contains the amount paid by each participant in DUOS charges. This is summed to find the DNSP variable revenue from grid import
        "df_participant_duos_payments": pd.DataFrame(0,index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]),
        "df_participant_tuos_payments": pd.DataFrame(0,index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]),
        # Where nuos = duos + tuos + green scheme stuff
        "df_participant_nuos_payments": pd.DataFrame(0,index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]),
        "df_dnsp_revenue" : pd.DataFrame(0,index = time_periods, columns=['grid_import_revenue_fixed','grid_import_revenue_variable','local_solar_import_revenue','central_battery_import_revenue','total_revenue']),
        "df_tnsp_revenue" : pd.DataFrame(0,index = time_periods, columns=['grid_import_revenue_fixed','grid_import_revenue_variable','local_solar_import_revenue','central_battery_import_revenue','total_revenue']),
        "df_nuos_revenue" : pd.DataFrame(0,index = time_periods, columns=['grid_import_revenue_fixed','grid_import_revenue_variable','local_solar_import_revenue','central_battery_import_revenue','total_revenue']),
        "df_retailer_revenue" : pd.DataFrame(0,index = time_periods, columns=['grid_import_revenue_fixed','grid_import_revenue_variable','local_solar_import_revenue','central_battery_import_revenue','total_revenue']),
        "df_central_battery_revenue" : pd.DataFrame(0,index = time_periods, columns=['central_battery_revenue'])
        }

    # --------------------------------------------------------------
    # Participant financial calcs
    # --------------------------------------------------------------
    # Status Reporting
    if status_callback:
        status_callback('Calculating Financial Flows: 0%')
        percent_finished = 0
        single_step_percent = 100.0 / float(len(time_periods) * len(mynetwork.get_participants()))
        

    for p in mynetwork.get_participants():
        # Initialise params used in block tariff calcs.
        total_usage_today = 0
        previous_time = time_periods[0]

        for time in time_periods:
            if status_callback:
                percent_finished += single_step_percent
                status_callback('Calculating Financial Flows: '+str(round(percent_finished))+"%")
            
            retail_tariff_type = p.get_retail_tariff_type()
            network_tariff_type = p.get_network_tariff_type()

            net_export = results.get_net_export(time, p.get_id())
            local_solar_import = results.get_local_solar_import(time, p.get_id())
            participant_central_batt_import = results.get_participant_central_batt_import(time, p.get_id())
            local_solar_sales = results.get_local_solar_sales(time, p.get_id())
            central_batt_solar_sales = results.get_central_batt_solar_sales(time, p.get_id())
            # Left over solar which is exported to the grid. Calculated in energy flows above.
            export_to_grid_solar_sales = results.get_export_to_grid_solar_sales(time, p.get_id())
            # Left over load which requires grid import. Calculated in energy flows above.
            external_grid_import = results.get_external_grid_elec_import(time, p.get_id())

            
            # Calc resultant financial flows (all except variable charge - this is done below)
            
            financial_output["df_local_solar_import_charge"].loc[time,p.get_id()] = my_tariffs.get_local_solar_import_tariff(time) * local_solar_import
            financial_output["df_central_batt_import_charge"].loc[time,p.get_id()] = my_tariffs.get_central_batt_tariff(time) * participant_central_batt_import
            financial_output["df_local_solar_sales_revenue"].loc[time,p.get_id()] = my_tariffs.get_local_solar_export_tariff(time) * local_solar_sales
            financial_output["df_central_batt_solar_sales_revenue"].loc[time,p.get_id()] = my_tariffs.get_central_batt_buy_tariff(time) * central_batt_solar_sales
            financial_output["df_export_to_grid_solar_sales_revenue"].loc[time,p.get_id()] = my_tariffs.get_retail_solar_tariff(time,retail_tariff_type,8) * export_to_grid_solar_sales
            financial_output["df_fixed_charge"].loc[time,p.get_id()] = my_tariffs.get_fixed_tariff(TIME_PERIOD_LENGTH_MINS,retail_tariff_type)
            
            # Variable charges - apply retail tariffs to external grid import
            # May be worth moving this section of code into util?
            
            # Block tariff ---------------
            # The block tariffs will be applied by counting the volume of energy used within the period and applying the appropriate tariff accordingly
            if retail_tariff_type == 'Business Anytime':
                block_1_charge, block_2_charge, block_1_volume = my_tariffs.get_variable_tariff(time,retail_tariff_type)

                # First, calculate the current cumulative energy usage
                # Check whether it's a new day. If the current hour is midnight and the previous hour was 11pm, then it's a new day.
                if time.hour == 0 and previous_time.hour == 23 :
                    # If it's a new day then reset the block counter
                    total_usage_today = 0
                    # Set the previous time equal to current time for next loop.
                    previous_time = time
                else:
                    # Add the grid import during this period to the total usage for the day
                    # NOTE _ we are assuming only grid import applies to the block total
                    total_usage_today += external_grid_import
                
                # If the usage today has not yet exceeded the block max, then use the first block rate, else the second rate.
                if total_usage_today < block_1_volume :
                    variable_tariff = block_1_charge
                else:
                    variable_tariff = block_2_charge

                # Apply the tariff 
                financial_output["df_participant_variable_charge"].loc[time,p.get_id()] = variable_tariff * external_grid_import
            
            # TOU Tariffs ---------------
            # The TOU tariffs will be applied by using if statements to determine whether peak/shoulder/off-peak
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

                # In the case where TOU periods only apply on weekdays then check for weekdays and apply the same logic as above.
                elif tou_weekday_only_flag == 1 and (time.weekday() >= 0 and time.weekday() <=4) :
                    if (time.hour > peak_start_time and time.hour <= peak_end_time) or (time.hour > peak_start_time_2 and time.hour <= peak_end_time_2) :
                        variable_tariff = peak_charge
                    elif (time.hour > shoulder_start_time and time.hour <= shoulder_end_time) or (time.hour > shoulder_start_time_2 and time.hour <= shoulder_end_time_2) :
                        variable_tariff = shoulder_charge
                    else:
                        variable_tariff = offpeak_charge

                # Else assume it's off-peak time
                else:
                    variable_tariff = offpeak_charge
                # Apply the tariff
                financial_output["df_participant_variable_charge"].loc[time,p.get_id()] = variable_tariff * external_grid_import

            # Controlled Load and Flat Tariffs ---------------
            # The controlled load tariffs and the flat tariff will be applied simply as the tariff times by the volume of electricity consumed, so the same calculation is applied.
            if retail_tariff_type == 'Controlled Load 1' or retail_tariff_type == 'Controlled Load 2' or retail_tariff_type == 'flat_charge':
                variable_tariff = my_tariffs.get_variable_tariff(time, retail_tariff_type)
                financial_output["df_participant_variable_charge"].loc[time,p.get_id()] = variable_tariff * external_grid_import
            
            # Total bill
            participant_variable_charge = financial_output["df_participant_variable_charge"].loc[time, p.get_id()]
            local_solar_import_charge = financial_output["df_local_solar_import_charge"].loc[time, p.get_id()]
            central_batt_import_charge = financial_output["df_central_batt_import_charge"].loc[time, p.get_id()]
            local_solar_sales_revenue = financial_output["df_local_solar_sales_revenue"].loc[time, p.get_id()]
            central_batt_solar_sales_revenue = financial_output["df_central_batt_solar_sales_revenue"].loc[time, p.get_id()]
            export_to_grid_solar_sales_revenue = financial_output["df_export_to_grid_solar_sales_revenue"].loc[time, p.get_id()]
            fixed_charge = financial_output["df_fixed_charge"].loc[time, p.get_id()]

            # Add charges and subtract revenue for total bill
            financial_output["df_total_participant_bill"].loc[time,p.get_id()] = participant_variable_charge + local_solar_import_charge + central_batt_import_charge + fixed_charge - local_solar_sales_revenue - central_batt_solar_sales_revenue - export_to_grid_solar_sales_revenue 

    
    # --------------------------------------------------------------
    # DNSP financial calcs
    # --------------------------------------------------------------  
    if status_callback:
        status_callback('Calculating DNSP Finances:0%')
        percent_finished = 0
        single_step_percent = 100.0 / float(len(time_periods) * len(mynetwork.get_participants()))
    # Initialise df used in demand tariff calcs (stores max demand values)      
    df_participant_max_monthly_demand = pd.DataFrame(0, index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]) 


    for p in mynetwork.get_participants():
        # Initialise params used in demand tariff calcs
        max_demand = 0
        max_demand_time = time_periods[0]
        previous_month = time_periods[0].month

        for time in time_periods:
            # Update callback status
            if status_callback:
                percent_finished += single_step_percent
                status_callback('Calculating DNSP Finances: '+str(round(percent_finished))+"%")       

            # Required energy flows for retailer / DNSP / TNSP calcs
            gross_participant_grid_import = results.get_gross_participant_grid_import(time)
            gross_participant_local_solar_import = results.get_gross_participant_local_solar_import(time)
            gross_participant_central_battery_import = results.get_gross_participant_central_battery_import(time)
            

            # Financial calcs for DNSP
            # Fixed charges revenue is the fixed charge times by the number of customers paying this charge
            financial_output["df_dnsp_revenue"].loc[time,'grid_import_revenue_fixed'] = my_tariffs.get_duos_on_grid_import_fixed(TIME_PERIOD_LENGTH_MINS, network_tariff_type) * len(mynetwork.get_participants())
            financial_output["df_dnsp_revenue"].loc[time, 'local_solar_import_revenue'] = my_tariffs.get_duos_on_local_solar_import(time) * gross_participant_local_solar_import
            financial_output["df_dnsp_revenue"].loc[time,'central_battery_import_revenue'] = my_tariffs.get_duos_on_central_batt_import(time) * gross_participant_central_battery_import

            # Variable component - will need to be the sum of each individual participant's dnsp payment because each may be on a different tariff.
            
            network_tariff_type = p.get_network_tariff_type()

            # Left over load which requires grid import. Calculated in energy flows above.
            external_grid_import = results.get_external_grid_elec_import(time, p.get_id())

            # Controlled Load and Flat Tariffs ---------------
            # The controlled load tariffs and the flat tariff will be applied simply as the tariff times by the volume of electricity consumed, so the same calculation is applied.
            if network_tariff_type == 'Controlled Load 1' or network_tariff_type == 'Controlled Load 2' or network_tariff_type == 'LV Small Business Anytime':
                variable_tariff = my_tariffs.get_duos_on_grid_import_variable(time, network_tariff_type)
                financial_output["df_participant_duos_payments"].loc[time,p.get_id()] = variable_tariff * external_grid_import

            # TOU Tariffs ---------------
            # The TOU tariffs will be applied by using if statements to determine whether peak/shoulder/off-peak
            if network_tariff_type == 'LV TOU <100MWh' or network_tariff_type == 'LV Business TOU_Interval meter' or network_tariff_type == 'Small Business - Opt in Demand':
                peak_charge, shoulder_charge, offpeak_charge, peak_start_time, peak_end_time, peak_start_time_2, peak_end_time_2, shoulder_start_time, shoulder_end_time, shoulder_start_time_2, shoulder_end_time_2, tou_weekday_only_flag, demand_charge = my_tariffs.get_duos_on_grid_import_variable(time,network_tariff_type)

                # If the TOU periods apply all days and not just weekdays then the flag will be zero
                if tou_weekday_only_flag == 0 :
                    # Check for whether it's a peak time
                    if (time.hour > peak_start_time and time.hour <= peak_end_time) or (time.hour > peak_start_time_2 and time.hour <= peak_end_time_2) :
                        variable_tariff = peak_charge
                    # If not, check whether it's shoulder time
                    elif (time.hour > shoulder_start_time and time.hour <= shoulder_end_time) or (time.hour > shoulder_start_time_2 and time.hour <= shoulder_end_time_2) :
                        variable_tariff = shoulder_charge

                # In the case where TOU periods only apply on weekdays then check for weekdays and apply the same logic as above.
                elif tou_weekday_only_flag == 1 and (time.weekday() >= 0 and time.weekday() <=4) :
                    if (time.hour > peak_start_time and time.hour <= peak_end_time) or (time.hour > peak_start_time_2 and time.hour <= peak_end_time_2) :
                        variable_tariff = peak_charge
                    elif (time.hour > shoulder_start_time and time.hour <= shoulder_end_time) or (time.hour > shoulder_start_time_2 and time.hour <= shoulder_end_time_2) :
                        variable_tariff = shoulder_charge

                # Else assume it's off-peak time
                else:
                    variable_tariff = offpeak_charge
                # Apply the tariff 
                financial_output["df_participant_duos_payments"].loc[time,p.get_id()] = variable_tariff * external_grid_import
            
            # Demand tariff includes TOU component which is handled above. In addition, the demand component is calculated for each participant
            if network_tariff_type == 'Small Business - Opt in Demand' :
                current_month = time.month
                
                # If it's a new month, then print the max demand value to the df at the max demand time, reset the max demand to zero and set the month to the new month.
                if current_month != previous_month:
                    # Print to df in units of power (kVA, assume unity pf)
                    df_participant_max_monthly_demand.loc[max_demand_time, p.get_id()] = max_demand * (60/TIME_PERIOD_LENGTH_MINS)
                    max_demand = 0
                    previous_month = current_month

                # Left over load which requires grid import. Calculated in energy flows above.
                external_grid_import = results.get_external_grid_elec_import(time, p.get_id())
                
                # If the load in this period is greater than the currently recorded max demand then update max demand and max demand time
                if external_grid_import > max_demand :
                    max_demand = external_grid_import
                    max_demand_time = time

                # In the case where there is less than 1 month of data (i.e. start and end months are the same) AND the loop is on the final time period, then print max to df.
                if time_periods[0].month == time_periods[-1].month and time == time_periods[-1] :
                    # Print to df in units of power (kVA, assume unity pf)
                    df_participant_max_monthly_demand.loc[max_demand_time, p.get_id()] = max_demand * (60/TIME_PERIOD_LENGTH_MINS)
        
        # After looping through all time periods for the current participant
        if network_tariff_type == 'Small Business - Opt in Demand' :
            # Need a separate time loop to calculate demand charges since the max kVA values are entered into the df 'retrospectively'
            for time in time_periods:
                demand_payment = df_participant_max_monthly_demand.loc[time, p.get_id()] * demand_charge
                financial_output["df_participant_duos_payments"].loc[time,p.get_id()] = financial_output["df_participant_duos_payments"].loc[time,p.get_id()] + demand_payment
    
    # Finally, calculate the sum across participants to find the DNSP's variable DUOS revenue. Then calculate the DNSP's total revenue (i.e. including fixed charges etc).
    financial_output["df_dnsp_revenue"]['grid_import_revenue_variable'] = financial_output["df_participant_duos_payments"].sum(axis=1)
    # Sum across columns for total dnsp revenue 
    for time in time_periods:    
        financial_output["df_dnsp_revenue"].loc[time,'total_revenue'] = financial_output["df_dnsp_revenue"].loc[time,['grid_import_revenue_fixed','grid_import_revenue_variable','local_solar_import_revenue','central_battery_import_revenue']].sum()

    # --------------------------------------------------------------
    # TNSP financial calcs 
    # --------------------------------------------------------------
    if status_callback:
        status_callback('Calculating TNSP Finances:0%')
        percent_finished = 0
        single_step_percent = 100.0 / float(len(time_periods) * len(mynetwork.get_participants()))
    # Initialise df used in demand tariff calcs (stores max demand values)      
    df_participant_max_monthly_demand = pd.DataFrame(0, index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]) 


    for p in mynetwork.get_participants():
        # Initialise params used in demand tariff calcs
        max_demand = 0
        max_demand_time = time_periods[0]
        previous_month = time_periods[0].month

        for time in time_periods:
            # Update callback status
            if status_callback:
                percent_finished += single_step_percent
                status_callback('Calculating TNSP Finances: '+str(round(percent_finished))+"%")       

            # Required energy flows for retailer / DNSP / TNSP calcs
            gross_participant_grid_import = results.get_gross_participant_grid_import(time)
            gross_participant_local_solar_import = results.get_gross_participant_local_solar_import(time)
            gross_participant_central_battery_import = results.get_gross_participant_central_battery_import(time)

            # Financial calcs for TNSP
            # Fixed charges revenue is the fixed charge times by the number of customers paying this charge
            financial_output["df_tnsp_revenue"].loc[time,'grid_import_revenue_fixed'] = my_tariffs.get_tuos_on_grid_import_fixed(TIME_PERIOD_LENGTH_MINS, network_tariff_type) * len(mynetwork.get_participants())
            financial_output["df_tnsp_revenue"].loc[time, 'local_solar_import_revenue'] = my_tariffs.get_tuos_on_local_solar_import(time) * gross_participant_local_solar_import
            financial_output["df_tnsp_revenue"].loc[time,'central_battery_import_revenue'] = my_tariffs.get_tuos_on_central_batt_import(time) * gross_participant_central_battery_import

            # Variable component - will need to be the sum of each individual participant's tnsp payment because each may be on a different tariff.
            
            network_tariff_type = p.get_network_tariff_type()

            # Left over load which requires grid import. Calculated in energy flows above.
            external_grid_import = results.get_external_grid_elec_import(time, p.get_id())

            # Controlled Load and Flat Tariffs ---------------
            # The controlled load tariffs and the flat tariff will be applied simply as the tariff times by the volume of electricity consumed, so the same calculation is applied.
            if network_tariff_type == 'Controlled Load 1' or network_tariff_type == 'Controlled Load 2' or network_tariff_type == 'LV Small Business Anytime':
                variable_tariff = my_tariffs.get_tuos_on_grid_import_variable(time, network_tariff_type)
                financial_output["df_participant_tuos_payments"].loc[time,p.get_id()] = variable_tariff * external_grid_import

            # TOU Tariffs ---------------
            # The TOU tariffs will be applied by using if statements to determine whether peak/shoulder/off-peak
            if network_tariff_type == 'LV TOU <100MWh' or network_tariff_type == 'LV Business TOU_Interval meter' or network_tariff_type == 'Small Business - Opt in Demand':
                peak_charge, shoulder_charge, offpeak_charge, peak_start_time, peak_end_time, peak_start_time_2, peak_end_time_2, shoulder_start_time, shoulder_end_time, shoulder_start_time_2, shoulder_end_time_2, tou_weekday_only_flag, demand_charge = my_tariffs.get_tuos_on_grid_import_variable(time,network_tariff_type)

                # If the TOU periods apply all days and not just weekdays then the flag will be zero
                if tou_weekday_only_flag == 0 :
                    # Check for whether it's a peak time
                    if (time.hour > peak_start_time and time.hour <= peak_end_time) or (time.hour > peak_start_time_2 and time.hour <= peak_end_time_2) :
                        variable_tariff = peak_charge
                    # If not, check whether it's shoulder time
                    elif (time.hour > shoulder_start_time and time.hour <= shoulder_end_time) or (time.hour > shoulder_start_time_2 and time.hour <= shoulder_end_time_2) :
                        variable_tariff = shoulder_charge

                # In the case where TOU periods only apply on weekdays then check for weekdays and apply the same logic as above.
                elif tou_weekday_only_flag == 1 and (time.weekday() >= 0 and time.weekday() <=4) :
                    if (time.hour > peak_start_time and time.hour <= peak_end_time) or (time.hour > peak_start_time_2 and time.hour <= peak_end_time_2) :
                        variable_tariff = peak_charge
                    elif (time.hour > shoulder_start_time and time.hour <= shoulder_end_time) or (time.hour > shoulder_start_time_2 and time.hour <= shoulder_end_time_2) :
                        variable_tariff = shoulder_charge

                # Else assume it's off-peak time
                else:
                    variable_tariff = offpeak_charge
                # Apply the tariff 
                financial_output["df_participant_tuos_payments"].loc[time,p.get_id()] = variable_tariff * external_grid_import
            
            # Demand tariff includes TOU component which is handled above. In addition, the demand component is calculated for each participant
            if network_tariff_type == 'Small Business - Opt in Demand' :
                current_month = time.month
                
                # If it's a new month, then print the max demand value to the df at the max demand time, reset the max demand to zero and set the month to the new month.
                if current_month != previous_month:
                    # Print to df in units of power (kVA, assume unity pf)
                    df_participant_max_monthly_demand.loc[max_demand_time, p.get_id()] = max_demand * (60/TIME_PERIOD_LENGTH_MINS)
                    max_demand = 0
                    previous_month = current_month

                # Left over load which requires grid import. Calculated in energy flows above.
                external_grid_import = results.get_external_grid_elec_import(time, p.get_id())
                
                # If the load in this period is greater than the currently recorded max demand then update max demand and max demand time
                if external_grid_import > max_demand :
                    max_demand = external_grid_import
                    max_demand_time = time

                # In the case where there is less than 1 month of data (i.e. start and end months are the same) AND the loop is on the final time period, then print max to df.
                if time_periods[0].month == time_periods[-1].month and time == time_periods[-1] :
                    # Print to df in units of power (kVA, assume unity pf)
                    df_participant_max_monthly_demand.loc[max_demand_time, p.get_id()] = max_demand * (60/TIME_PERIOD_LENGTH_MINS)
        
        # After looping through all time periods for the current participant
        if network_tariff_type == 'Small Business - Opt in Demand' :
            # Need a separate time loop to calculate demand charges since the max kVA values are entered into the df 'retrospectively'
            for time in time_periods:
                demand_payment = df_participant_max_monthly_demand.loc[time, p.get_id()] * demand_charge
                financial_output["df_participant_tuos_payments"].loc[time,p.get_id()] = financial_output["df_participant_tuos_payments"].loc[time,p.get_id()] + demand_payment
    
    # Finally, calculate the sum across participants to find the TNSP's variable TUOS revenue. Then calculate the TNSP's total revenue (i.e. including fixed charges etc).
    financial_output["df_tnsp_revenue"]['grid_import_revenue_variable'] = financial_output["df_participant_tuos_payments"].sum(axis=1)
    # Sum across columns for total tnsp revenue 
    for time in time_periods:    
        financial_output["df_tnsp_revenue"].loc[time,'total_revenue'] = financial_output["df_tnsp_revenue"].loc[time,['grid_import_revenue_fixed','grid_import_revenue_variable','local_solar_import_revenue','central_battery_import_revenue']].sum()

    # --------------------------------------------------------------
    # NUOS financial calcs - NOTE this is not paid to a specific entity as NUOS = DUOS + TUOS + green schemes
    # --------------------------------------------------------------
    if status_callback:
        status_callback('Calculating NUOS Finances:0%')
        percent_finished = 0
        single_step_percent = 100.0 / float(len(time_periods) * len(mynetwork.get_participants()))
    # Initialise df used in demand tariff calcs (stores max demand values)      
    df_participant_max_monthly_demand = pd.DataFrame(0, index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]) 


    for p in mynetwork.get_participants():
        # Initialise params used in demand tariff calcs
        max_demand = 0
        max_demand_time = time_periods[0]
        previous_month = time_periods[0].month

        for time in time_periods:
            # Update callback status
            if status_callback:
                percent_finished += single_step_percent
                status_callback('Calculating NUOS Finances: '+str(round(percent_finished))+"%")       

            # Required energy flows for retailer / DNSP / TNSP calcs
            gross_participant_grid_import = results.get_gross_participant_grid_import(time)
            gross_participant_local_solar_import = results.get_gross_participant_local_solar_import(time)
            gross_participant_central_battery_import = results.get_gross_participant_central_battery_import(time)

            # Financial calcs for NUOS
            # Fixed charges revenue is the fixed charge times by the number of customers paying this charge
            financial_output["df_nuos_revenue"].loc[time,'grid_import_revenue_fixed'] = my_tariffs.get_nuos_on_grid_import_fixed(TIME_PERIOD_LENGTH_MINS, network_tariff_type) * len(mynetwork.get_participants())
            financial_output["df_nuos_revenue"].loc[time, 'local_solar_import_revenue'] = my_tariffs.get_nuos_on_local_solar_import(time) * gross_participant_local_solar_import
            financial_output["df_nuos_revenue"].loc[time,'central_battery_import_revenue'] = my_tariffs.get_nuos_on_central_batt_import(time) * gross_participant_central_battery_import

            # Variable component - will need to be the sum of each individual participant's NUOS payment because each may be on a different tariff.
            
            network_tariff_type = p.get_network_tariff_type()

            # Left over load which requires grid import. Calculated in energy flows above.
            external_grid_import = results.get_external_grid_elec_import(time, p.get_id())

            # Controlled Load and Flat Tariffs ---------------
            # The controlled load tariffs and the flat tariff will be applied simply as the tariff times by the volume of electricity consumed, so the same calculation is applied.
            if network_tariff_type == 'Controlled Load 1' or network_tariff_type == 'Controlled Load 2' or network_tariff_type == 'LV Small Business Anytime':
                variable_tariff = my_tariffs.get_nuos_on_grid_import_variable(time, network_tariff_type)
                financial_output["df_participant_nuos_payments"].loc[time,p.get_id()] = variable_tariff * external_grid_import

            # TOU Tariffs ---------------
            # The TOU tariffs will be applied by using if statements to determine whether peak/shoulder/off-peak
            if network_tariff_type == 'LV TOU <100MWh' or network_tariff_type == 'LV Business TOU_Interval meter' or network_tariff_type == 'Small Business - Opt in Demand':
                peak_charge, shoulder_charge, offpeak_charge, peak_start_time, peak_end_time, peak_start_time_2, peak_end_time_2, shoulder_start_time, shoulder_end_time, shoulder_start_time_2, shoulder_end_time_2, tou_weekday_only_flag, demand_charge = my_tariffs.get_nuos_on_grid_import_variable(time,network_tariff_type)

                # If the TOU periods apply all days and not just weekdays then the flag will be zero
                if tou_weekday_only_flag == 0 :
                    # Check for whether it's a peak time
                    if (time.hour > peak_start_time and time.hour <= peak_end_time) or (time.hour > peak_start_time_2 and time.hour <= peak_end_time_2) :
                        variable_tariff = peak_charge
                    # If not, check whether it's shoulder time
                    elif (time.hour > shoulder_start_time and time.hour <= shoulder_end_time) or (time.hour > shoulder_start_time_2 and time.hour <= shoulder_end_time_2) :
                        variable_tariff = shoulder_charge

                # In the case where TOU periods only apply on weekdays then check for weekdays and apply the same logic as above.
                elif tou_weekday_only_flag == 1 and (time.weekday() >= 0 and time.weekday() <=4) :
                    if (time.hour > peak_start_time and time.hour <= peak_end_time) or (time.hour > peak_start_time_2 and time.hour <= peak_end_time_2) :
                        variable_tariff = peak_charge
                    elif (time.hour > shoulder_start_time and time.hour <= shoulder_end_time) or (time.hour > shoulder_start_time_2 and time.hour <= shoulder_end_time_2) :
                        variable_tariff = shoulder_charge

                # Else assume it's off-peak time
                else:
                    variable_tariff = offpeak_charge
                # Apply the tariff 
                financial_output["df_participant_nuos_payments"].loc[time,p.get_id()] = variable_tariff * external_grid_import
            
            # Demand tariff includes TOU component which is handled above. In addition, the demand component is calculated for each participant
            if network_tariff_type == 'Small Business - Opt in Demand' :
                current_month = time.month
                
                # If it's a new month, then print the max demand value to the df at the max demand time, reset the max demand to zero and set the month to the new month.
                if current_month != previous_month:
                    # Print to df in units of power (kVA, assume unity pf)
                    df_participant_max_monthly_demand.loc[max_demand_time, p.get_id()] = max_demand * (60/TIME_PERIOD_LENGTH_MINS)
                    max_demand = 0
                    previous_month = current_month

                # Left over load which requires grid import. Calculated in energy flows above.
                external_grid_import = results.get_external_grid_elec_import(time, p.get_id())
                
                # If the load in this period is greater than the currently recorded max demand then update max demand and max demand time
                if external_grid_import > max_demand :
                    max_demand = external_grid_import
                    max_demand_time = time

                # In the case where there is less than 1 month of data (i.e. start and end months are the same) AND the loop is on the final time period, then print max to df.
                if time_periods[0].month == time_periods[-1].month and time == time_periods[-1] :
                    # Print to df in units of power (kVA, assume unity pf)
                    df_participant_max_monthly_demand.loc[max_demand_time, p.get_id()] = max_demand * (60/TIME_PERIOD_LENGTH_MINS)
        
        # After looping through all time periods for the current participant
        if network_tariff_type == 'Small Business - Opt in Demand' :
            # Need a separate time loop to calculate demand charges since the max kVA values are entered into the df 'retrospectively'
            for time in time_periods:
                demand_payment = df_participant_max_monthly_demand.loc[time, p.get_id()] * demand_charge
                financial_output["df_participant_nuos_payments"].loc[time,p.get_id()] = financial_output["df_participant_nuos_payments"].loc[time,p.get_id()] + demand_payment
    
    # Finally, calculate the sum across participants to find the total variable NUOS revenue. Then calculate the total NUOS revenue (i.e. including fixed charges etc).
    financial_output["df_nuos_revenue"]['grid_import_revenue_variable'] = financial_output["df_participant_nuos_payments"].sum(axis=1)
    # Sum across columns for total nuos revenue 
    for time in time_periods:    
        financial_output["df_nuos_revenue"].loc[time,'total_revenue'] = financial_output["df_nuos_revenue"].loc[time,['grid_import_revenue_fixed','grid_import_revenue_variable','local_solar_import_revenue','central_battery_import_revenue']].sum()



    # --------------------------------------------------------------
    # Retailer financial calcs
    # --------------------------------------------------------------
    if status_callback:
        status_callback('Calculating Retail Finances')
    for time in time_periods:
        # print "Financial", time
        # Fixed charges revenue is the fixed charge times by the number of customers paying this charge
        # TODO - check whether .sum() is working as expected! See test file.
        financial_output["df_retailer_revenue"].loc[time,'grid_import_revenue_fixed'] = my_tariffs.get_retail_income_on_grid_import_fixed(TIME_PERIOD_LENGTH_MINS) * len(mynetwork.get_participants())
        financial_output["df_retailer_revenue"].loc[time, 'grid_import_revenue_variable'] = my_tariffs.get_retail_income_on_grid_import_variable(time) * gross_participant_grid_import
        financial_output["df_retailer_revenue"].loc[time, 'local_solar_import_revenue'] = my_tariffs.get_retail_income_on_local_solar_import(time) * gross_participant_local_solar_import
        financial_output["df_retailer_revenue"].loc[time,'central_battery_import_revenue'] = my_tariffs.get_retail_income_on_central_batt_import(time) * gross_participant_central_battery_import
        financial_output["df_retailer_revenue"].loc[time,'total_revenue'] = financial_output["df_retailer_revenue"].loc[time,['grid_import_revenue_fixed','grid_import_revenue_variable','local_solar_import_revenue','central_battery_import_revenue']].sum()
        
        # Central Battery revenue
        # Energy imported by the battery
        battery_import = sum([results.get_central_batt_solar_sales(time, participant.get_id()) for participant in mynetwork.get_participants()])
        # Energy exported by the battery
        # TODO - will need to update thif is the battery can also import from the grid.
        battery_export = sum([results.get_participant_central_batt_import(time, participant.get_id()) for participant in mynetwork.get_participants()])
        # Calculate income for battery which is export(kWh) * export tariff for energy paid by consumer (c/kWh) minus import (kWh) * import tariff for energy paid by battery (c/kWh, includes energy,retail,NUOS)
        financial_output["df_central_battery_revenue"].loc[time,'central_battery_revenue'] = battery_export * my_tariffs.get_central_batt_buy_tariff(time) - battery_import * my_tariffs.get_total_central_battery_import_tariff(time)

    return {'financial_output':financial_output, 'data_output':results.energy_output}

def run_en_json(scenario=None):
    result = run_en(scenario)

    financial_output = result['financial_output']
    data_output = result['data_output']

    new_financial_output = {}
    for key in financial_output:
        new_financial_output[key]=[]
        for date, row in financial_output[key].T.iteritems():
            row_dict = {'dt_str':str(date)}
            for col_header in financial_output[key]:
                row_dict[col_header] = float(row[col_header]) if not pd.isnull(row[col_header]) else 0
            new_financial_output[key].append(row_dict)    
                # print col_header+": "+str(row[col_header])
    

    new_energy_output = {}
    for key in data_output:
        new_energy_output[key]=[]
        for date, row in data_output[key].T.iteritems():
            row_dict = {'dt_str':str(date)}
            for col_header in data_output[key]:
                row_dict[col_header] = float(row[col_header]) if not pd.isnull(row[col_header]) else 0
            
                # print col_header+": "+str(row[col_header])
            new_energy_output[key].append(row_dict)

    return {'financial_output':new_financial_output, 'energy_output': new_energy_output}


def run_en_csv(output_dir, data_dir, scenario=None, status_callback=None):
    if status_callback:
        status_callback('Running EN CSV')

    result = run_en(scenario, status_callback=status_callback, data_dir=data_dir)
    print "Writing to CSV"
    if status_callback:
        status_callback('Writing Output to CSV Files')
    battery_capacity = str(scenario['battery_capacity']) if 'battery_capacity' in scenario else ""
    # battery_capacity = str(network.get_batteries()[0].cap_kWh)+"kWh" if len(network.get_batteries()) > 0 else ""
    for label in result['financial_output']:
        print label
        result['financial_output'][label].to_csv(path_or_buf=os.path.join(output_dir, label+battery_capacity+".csv"))
    for label in result['data_output']:
        print label
        result['data_output'][label].to_csv(path_or_buf=os.path.join(output_dir, label+battery_capacity+".csv"))
    
    if status_callback:
        status_callback('Finished')





# Start here! :)

if __name__ == "__main__":
    print "Running Simulation: ",0, "kWh"
    run_en_csv('output', 'data', {'battery_capacity':0.001})
    # for battery_capacity in range(5,35,5):
    #     print "Running Simulation: ",battery_capacity, "kWh"
    #     run_en_csv('output', 'data', {'battery_capacity':battery_capacity})
