
from network import Network
from participant import Participant
from battery import Battery, Central_Battery
from tariffs import Tariffs
import util
import datetime
import pandas as pd
import numpy as np
import pprint

def run_en():
        
    TIME_PERIOD_LENGTH_MINS = 30

    # Create a network
    mynetwork = Network('Byron')

    # Create participants
    participant_1 = Participant('building_1','solar','Business TOU','LV Small Business Anytime', 'ENOVA')
    participant_2 = Participant('building_2','load','Business TOU','LV Small Business Anytime', 'ENOVA')

    # Add participants to network
    mynetwork.add_participant(participant_1)
    mynetwork.add_participant(participant_2)

    # Add a central battery
    battery_1 = Central_Battery(10.0, 5.0, 0.99)
    mynetwork.add_central_battery(battery_1)

    # Add tariffs
    my_tariffs = Tariffs('Test',"data/retail_tariffs.csv","data/duos.csv","test")

    # Generate a list of time periods in half hour increments
    time_periods = util.generate_dates_in_range(datetime.datetime.now() - datetime.timedelta(days = 2), datetime.datetime.now(), 30)
    # Make empty df
    data_output = {
        "df_net_export" : pd.DataFrame(index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]),
        "df_network_energy_flows" : pd.DataFrame(index = time_periods, columns=['net_participant_export', 'central_battery_export', 'unallocated_local_solar', 'unallocated_central_battery_load','gross_participant_grid_import','gross_participant_local_solar_import','gross_participant_central_battery_import']),
        "df_local_solar_import" : pd.DataFrame(index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]), 
        "df_participant_central_batt_import" : pd.DataFrame(index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]), 
        "df_local_solar_sales" : pd.DataFrame(index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]), 
        "df_central_batt_solar_sales" : pd.DataFrame(index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]),
        "df_export_to_grid_solar_sales" : pd.DataFrame(index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]),
        "df_external_grid_elec_import": pd.DataFrame(index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()])
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
        central_battery_export = sum(b.make_export_decision(net_participant_export) for b in mynetwork.get_batteries())

        data_output['df_network_energy_flows'].loc[time, 'central_battery_export'] = central_battery_export

        # Calc network in/out kWh
        data_output['df_network_energy_flows'].loc[time, 'net_network_export'] = net_participant_export + central_battery_export

        # Run local solar allocation algorithm
        # Initialise an empty df with column name net_export
        participants_list_sorted = pd.DataFrame(columns=['net_export'])
        # Add net export data for participants with load
        for p in mynetwork.get_participants():
            # Get data point from df_net_export df
            net_export = data_output['df_net_export'].loc[time, p.get_id()]
            # If there is load (i.e. export < 0 ) add to list
            if net_export < 0 :
                participants_list_sorted.loc[p.get_id(), 'net_export'] = net_export
        # Sort list of participants with load
        participants_list_sorted = participants_list_sorted.sort_values('net_export')

        # Calculate total solar available in this time period
        available_batt = max(central_battery_export,0)
        available_solar = 0
        for col in data_output['df_net_export']:
            net_export = data_output['df_net_export'].loc[time, col]
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
                    data_output["df_local_solar_import"].loc[time, p] = local_solar_import
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
                    participant_central_batt_import = min(abs(battery_allocation), abs(participants_list_sorted.loc[p,'net_export']) - abs(local_solar_import))
                    data_output["df_participant_central_batt_import"].loc[time, p] = participant_central_batt_import
                    available_batt -= participant_central_batt_import
                    battery_allocation = float(available_batt) / float(num_remaining_participants) if num_remaining_participants > 0 else 0

                    
        # Save any solar left over after the allocation process to df_network_energy_flows
        data_output["df_network_energy_flows"].loc[time, 'unallocated_local_solar'] = available_solar


        # Run local load allocation algorithm (aka solar sales)
        # Initialise an empty df with column name net export
        solar_sales_participant_list = pd.DataFrame(columns = ['net_export'])
        # Add net export data for participants with generation
        for p in mynetwork.get_participants():
            # Get data point from df_net_export df
            net_export = data_output['df_net_export'].loc[time, p.get_id()]
            # If there is generation (i.e. export > 0 ) add to list
            if net_export > 0 :
                solar_sales_participant_list.loc[p.get_id(), 'net_export'] = net_export
        # Sort list of participants with load
        solar_sales_participant_list = solar_sales_participant_list.sort_values('net_export')

        # Calculate total load available in this time period
        # TODO - central battery
        available_load = 0
        available_batt_charging_load = abs(min(central_battery_export,0))

        for col in data_output['df_net_export']:
            net_export = data_output['df_net_export'].loc[time, col]
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
                    data_output["df_local_solar_sales"].loc[time, p] = participant_solar_sale
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
                    data_output["df_central_batt_solar_sales"].loc[time, p] = participant_solar_sale
                    available_batt_charging_load -= participant_solar_sale
                    batt_charging_allocation = float(available_batt_charging_load) / float(num_remaining_participants) if num_remaining_participants > 0 else 0

        # Grid impacts for each customer. Import from grid and solar export to grid.
        for p in mynetwork.get_participants():
            # First, solar export to grid
            net_export = data_output["df_net_export"].loc[time,p.get_id()]
            local_solar_sales = data_output["df_local_solar_sales"].loc[time,p.get_id()]
            central_battery_solar_sales = data_output["df_central_batt_solar_sales"].loc[time,p.get_id()]
            # Calc and save to df
            export_to_grid_solar_sales = max(0,net_export) - max(0,local_solar_sales) - max(0,central_battery_solar_sales)
            data_output["df_export_to_grid_solar_sales"].loc[time,p.get_id()] = export_to_grid_solar_sales
            
            # Then, electricity import from grid
            local_solar_import = data_output["df_local_solar_import"].loc[time,p.get_id()]
            participant_central_batt_import = data_output["df_participant_central_batt_import"].loc[time,p.get_id()]
            # Left over load which requires grid import. Calc and save to df.
            external_grid_import = abs(min(net_export,0)) - abs(max(0,local_solar_import)) - abs(max(0,participant_central_batt_import))
            data_output["df_external_grid_elec_import"].loc[time,p.get_id()] = external_grid_import

        # Save any battery load left over after the allocation process to df_network_energy_flows
        data_output["df_network_energy_flows"].loc[time, 'unallocated_central_battery_load'] = available_batt_charging_load        
        
        # For the financial calcs for retailer/NSPs, calculate the gross grid import - i.e. how much did all the participants import during this time interval (only considers import - discards export). Also local solar and central battery import.
        data_output["df_network_energy_flows"].loc[time, 'gross_participant_grid_import'] = abs(min(data_output['df_network_energy_flows'].loc[time, 'net_participant_export'],0))
        data_output["df_network_energy_flows"].loc[time, 'gross_participant_local_solar_import'] = max(data_output['df_local_solar_import'].loc[time].sum(),0)
        data_output["df_network_energy_flows"].loc[time, 'gross_participant_central_battery_import'] = max(data_output["df_participant_central_batt_import"].loc[time].sum(),0)

    # print(participants_list_sorted)
    # print(data_output["df_export_to_grid_solar_sales"])

    # ----------------------------------------------------------------------------------------------------------------------------
    # Financial flows

    # Charges are positive (if earning money then negative). Revenue is positive when earning money.
    financial_output = {
        "df_participant_variable_charge" : pd.DataFrame(index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]),
        "df_local_solar_import_charge" : pd.DataFrame(index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]), 
        "df_central_batt_import_charge" : pd.DataFrame(index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]), 
        "df_local_solar_sales_revenue" : pd.DataFrame(index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]), 
        "df_central_batt_solar_sales_revenue" : pd.DataFrame(index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]),
        "df_export_to_grid_solar_sales_revenue" : pd.DataFrame(index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]),
        "df_fixed_charge" : pd.DataFrame(index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]),
        # The df_participant_duos_payments df contains the amount paid by each participant in DUOS charges. This is summed to find the DNSP variable revenue from grid import
        "df_participant_duos_payments": pd.DataFrame(index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]),
        "df_dnsp_revenue" : pd.DataFrame(index = time_periods, columns=['grid_import_revenue_fixed','grid_import_revenue_variable','local_solar_import_revenue','central_battery_import_revenue','total_revenue']),
        "df_tnsp_revenue" : pd.DataFrame(index = time_periods, columns=['grid_import_revenue_fixed','grid_import_revenue_variable','local_solar_import_revenue','central_battery_import_revenue','total_revenue']),
        "df_retailer_revenue" : pd.DataFrame(index = time_periods, columns=['grid_import_revenue_fixed','grid_import_revenue_variable','local_solar_import_revenue','central_battery_import_revenue','total_revenue']),
        "df_central_battery_revenue" : pd.DataFrame(index = time_periods, columns=['central_battery_revenue'])
        }

    # Initialise block tariff counter for use in applying the block tariffs and set the 'previous time' to be the first interval in the data set.
    total_usage_today = 0
    previous_time = time_periods[0]

    for time in time_periods:
        # Calc each participant in/out kWh and $
        for p in mynetwork.get_participants():
            
            retail_tariff_type = p.get_retail_tariff_type()
            network_tariff_type = p.get_network_tariff_type()

            net_export = data_output["df_net_export"].loc[time,p.get_id()]
            local_solar_import = data_output["df_local_solar_import"].loc[time,p.get_id()]
            participant_central_batt_import = data_output["df_participant_central_batt_import"].loc[time,p.get_id()]
            local_solar_sales = data_output["df_local_solar_sales"].loc[time,p.get_id()]
            central_batt_solar_sales = data_output["df_central_batt_solar_sales"].loc[time,p.get_id()]
            # Left over solar which is exported to the grid. Calculated in energy flows above.
            export_to_grid_solar_sales = data_output["df_export_to_grid_solar_sales"].loc[time,p.get_id()]
            # Left over load which requires grid import. Calculated in energy flows above.
            external_grid_import = data_output["df_external_grid_elec_import"].loc[time,p.get_id()]

            # Calc resultant financial flows (all except variable charge - this is done below)
            financial_output["df_local_solar_import_charge"].loc[time,p.get_id()] = my_tariffs.get_local_solar_tariff(time) * local_solar_import
            financial_output["df_central_batt_import_charge"].loc[time,p.get_id()] = my_tariffs.get_central_batt_tariff(time) * participant_central_batt_import
            financial_output["df_local_solar_sales_revenue"].loc[time,p.get_id()] = my_tariffs.get_local_solar_tariff(time) * local_solar_sales
            financial_output["df_central_batt_solar_sales_revenue"].loc[time,p.get_id()] = my_tariffs.get_central_batt_buy_tariff(time) * central_batt_solar_sales
            financial_output["df_export_to_grid_solar_sales_revenue"].loc[time,p.get_id()] = my_tariffs.get_retail_solar_tariff(time,retail_tariff_type,8) * export_to_grid_solar_sales
            financial_output["df_fixed_charge"].loc[time,p.get_id()] = my_tariffs.get_fixed_tariff(TIME_PERIOD_LENGTH_MINS,retail_tariff_type)
            
            # Variable charges
            # May be worth moving this into util?
            
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
                financial_output["df_participant_variable_charge"].loc[time,p.get_id()] = variable_tariff * external_grid_import

            # Controlled Load and Flat Tariffs ---------------
            # The controlled load tariffs and the flat tariff will be applied simply as the tariff times by the volume of electricity consumed, so the same calculation is applied.
            if retail_tariff_type == 'Controlled Load 1' or retail_tariff_type == 'Controlled Load 2' or retail_tariff_type == 'flat_charge':
                variable_tariff = my_tariffs.get_variable_tariff(time, retail_tariff_type)
                financial_output["df_participant_variable_charge"].loc[time,p.get_id()] = variable_tariff * external_grid_import
            

        # Required energy flows for retailer / DNSP / TNSP calcs
        gross_participant_grid_import = data_output["df_network_energy_flows"].loc[time, 'gross_participant_grid_import'] 
        gross_participant_local_solar_import = data_output["df_network_energy_flows"].loc[time, 'gross_participant_local_solar_import']
        gross_participant_central_battery_import = data_output["df_network_energy_flows"].loc[time, 'gross_participant_central_battery_import']

        # Financial calcs for DNSP
        # Fixed charges revenue is the fixed charge times by the number of customers paying this charge
        financial_output["df_dnsp_revenue"].loc[time,'grid_import_revenue_fixed'] = my_tariffs.get_duos_on_grid_import_fixed(TIME_PERIOD_LENGTH_MINS) * len(mynetwork.get_participants())
        financial_output["df_dnsp_revenue"].loc[time, 'local_solar_import_revenue'] = my_tariffs.get_duos_on_local_solar_import(time) * gross_participant_local_solar_import
        financial_output["df_dnsp_revenue"].loc[time,'central_battery_import_revenue'] = my_tariffs.get_duos_on_central_batt_import(time) * gross_participant_central_battery_import
        financial_output["df_dnsp_revenue"].loc[time,'total_revenue'] = financial_output["df_dnsp_revenue"].loc[time,['grid_import_revenue_fixed','grid_import_revenue_variable','local_solar_import_revenue','central_battery_import_revenue']].sum()

        # Variable component - will need to be the sum of each individual participant's dnsp payment because each may be on a different tariff.
        for p in mynetwork.get_participants():
            
            network_tariff_type = p.get_network_tariff_type()

            # Left over load which requires grid import. Calculated in energy flows above.
            external_grid_import = data_output["df_external_grid_elec_import"].loc[time,p.get_id()]

            # Controlled Load and Flat Tariffs ---------------
            # The controlled load tariffs and the flat tariff will be applied simply as the tariff times by the volume of electricity consumed, so the same calculation is applied.
            if network_tariff_type == 'Controlled Load 1' or network_tariff_type == 'Controlled Load 2' or network_tariff_type == 'LV Small Business Anytime':
                variable_tariff = my_tariffs.get_duos_on_grid_import_variable(time, network_tariff_type)
                financial_output["df_participant_duos_payments"].loc[time,p.get_id()] = variable_tariff * external_grid_import

            # TOU Tariffs ---------------
            # The TOU tariffs will be applied by using if statements to determine whether peak/shoulder/off-peak
            if network_tariff_type == 'LV TOU <100MWh' or network_tariff_type == 'LV Business TOU_Interval meter' or 'Small Business - Opt in Demand':
                peak_charge, shoulder_charge, offpeak_charge, peak_start_time, peak_end_time, peak_start_time_2, peak_end_time_2, shoulder_start_time, shoulder_end_time, shoulder_start_time_2, shoulder_end_time_2, tou_weekday_only_flag = my_tariffs.get_variable_tariff(time,network_tariff_type)
                
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
                # TODO - BOOKMARK - need to complete this section.


        # Finally, calculate the sum.
        financial_output["df_dnsp_revenue"].loc[time, 'grid_import_revenue_variable'] = my_tariffs.get_duos_on_grid_import_variable(time) * gross_participant_grid_import




        # Financial calcs for TNSP
        # Fixed charges revenue is the fixed charge times by the number of customers paying this charge
        # financial_output["df_tnsp_revenue"].loc[time,'grid_import_revenue_fixed'] = my_tariffs.get_tuos_on_grid_import_fixed(TIME_PERIOD_LENGTH_MINS) * len(mynetwork.get_participants())
        # financial_output["df_tnsp_revenue"].loc[time, 'grid_import_revenue_variable'] = my_tariffs.get_tuos_on_grid_import_variable(time) * gross_participant_grid_import
        # financial_output["df_tnsp_revenue"].loc[time, 'local_solar_import_revenue'] = my_tariffs.get_tuos_on_local_solar_import(time) * gross_participant_local_solar_import
        # financial_output["df_tnsp_revenue"].loc[time,'central_battery_import_revenue'] = my_tariffs.get_tuos_on_central_batt_import(time) * gross_participant_central_battery_import
        # financial_output["df_tnsp_revenue"].loc[time,'total_revenue'] = financial_output["df_tnsp_revenue"].loc[time,['grid_import_revenue_fixed','grid_import_revenue_variable','local_solar_import_revenue','central_battery_import_revenue']].sum()

        # Financial calcs for Retailer
        # Fixed charges revenue is the fixed charge times by the number of customers paying this charge
        financial_output["df_retailer_revenue"].loc[time,'grid_import_revenue_fixed'] = my_tariffs.get_retail_income_on_grid_import_fixed(TIME_PERIOD_LENGTH_MINS) * len(mynetwork.get_participants())
        financial_output["df_retailer_revenue"].loc[time, 'grid_import_revenue_variable'] = my_tariffs.get_retail_income_on_grid_import_variable(time) * gross_participant_grid_import
        financial_output["df_retailer_revenue"].loc[time, 'local_solar_import_revenue'] = my_tariffs.get_retail_income_on_local_solar_import(time) * gross_participant_local_solar_import
        financial_output["df_retailer_revenue"].loc[time,'central_battery_import_revenue'] = my_tariffs.get_retail_income_on_central_batt_import(time) * gross_participant_central_battery_import
        financial_output["df_retailer_revenue"].loc[time,'total_revenue'] = financial_output["df_retailer_revenue"].loc[time,['grid_import_revenue_fixed','grid_import_revenue_variable','local_solar_import_revenue','central_battery_import_revenue']].sum()
        
        # Central Battery revenue
        # Energy imported by the battery
        battery_import = data_output["df_central_batt_solar_sales"].loc[time].sum()
        # Energy exported by the battery
        # TODO - will need to update thif is the battery can also import from the grid.
        battery_export = data_output["df_participant_central_batt_import"].loc[time].sum()
        # Calculate income for battery which is export(kWh) * export tariff for energy paid by consumer (c/kWh) minus import (kWh) * import tariff for energy paid by battery (c/kWh, includes energy,retail,NUOS)
        financial_output["df_central_battery_revenue"].loc[time,'central_battery_revenue'] = battery_export * my_tariffs.get_central_batt_buy_tariff(time) - battery_import * my_tariffs.get_total_central_battery_import_tariff(time)



    # dts = financial_output["df_participant_variable_charge"].index.values.tolist()
    # print dts
    # new_indices = [dt.isoformat() for dt in dts]
    # financial_output["df_participant_variable_charge"].reset_index
    # financial_output["df_participant_variable_charge"].reindex(index=new_indices)
    # print (financial_output["df_participant_variable_charge"])
    
    # for key in financial_output:
    #     financial_output[key].index = financial_output[key].index.to_series().astype(str)
    # for key in data_output:
    #     data_output[key].index = data_output[key].index.to_series().astype(str)
    
    # # print(financial_output)

    # for key in financial_output:
    #     financial_output[key] = financial_output[key].T.to_dict('index')

    # for key in data_output:
    #     data_output[key] = data_output[key].T.to_dict('index')

    # new_financial_output = {}
    return {'financial_output':financial_output, 'data_output':data_output}

def run_en_json():
    result = run_en()

    financial_output = result['financial_output']
    data_output = result['data_output']

    new_financial_output = {}
    for key in financial_output:
        new_financial_output[key]=[]
        for date, row in financial_output[key].T.iteritems():
            row_dict = {'dt_str':str(date)}
            for col_header in financial_output[key]:
                row_dict[col_header] = float(row[col_header]) if type(row[col_header]) == "float" else 0
            new_financial_output[key].append(row_dict)    
                # print col_header+": "+str(row[col_header])
    

    new_energy_output = {}
    for key in data_output:
        new_energy_output[key]=[]
        for date, row in data_output[key].T.iteritems():
            row_dict = {'dt_str':str(date)}
            for col_header in data_output[key]:
                row_dict[col_header] = float(row[col_header]) if type(row[col_header]) == "float" else 0
            
                # print col_header+": "+str(row[col_header])
            new_energy_output[key].append(row_dict)

   
    
    return {'financial_output':new_financial_output, 'energy_output': new_energy_output}

    

# print(run_en())
run_en()

# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(run_en())

# print run_en_json()

