
from network import Network
from participant import Participant, CSV_Participant
from battery import Battery, Central_Battery
from tariffs import Tariffs
import util
import datetime
import pandas as pd
import numpy as np
import pprint
import csv

DEFAULT_LOAD_DATA_PATH = "data/essential_load_data_aie_26_feb_1_may.csv"
def getParticipantNames():
    f = open(DEFAULT_LOAD_DATA_PATH, 'rb')
    reader = csv.reader(f)
    headers = reader.next()
    headers.remove('date_time')
    return headers

def run_en(scenario= None):
        
    TIME_PERIOD_LENGTH_MINS = 30

    # Create a network
    mynetwork = Network('Byron')

    # Create participants
    # participant_1 = Participant('building_1','solar', 'A', 'ENOVA')
    # participant_2 = Participant('building_2','load', 'B', 'ENOVA')
    # participant_3 = Participant('building_3','load', 'B', 'ENOVA')
    
    participant_1 = CSV_Participant('participant_1','solar', 'A', 'ENOVA',"data/bb_pvoutput_solar_data_26_feb_1_may.csv", "data/essential_load_data_aie_26_feb_1_may.csv",20)
    participant_2 = CSV_Participant('participant_2','solar', 'A', 'ENOVA',"data/bb_pvoutput_solar_data_26_feb_1_may.csv", "data/essential_load_data_aie_26_feb_1_may.csv",8)
    participant_3 = CSV_Participant('participant_3','solar', 'A', 'ENOVA',"data/bb_pvoutput_solar_data_26_feb_1_may.csv", "data/essential_load_data_aie_26_feb_1_may.csv",8)

    # Add participants to network
    mynetwork.add_participant(participant_1)
    mynetwork.add_participant(participant_2)
    mynetwork.add_participant(participant_3)
   

    # Add a central battery
    battery_1 = Central_Battery(10.0, 5.0, 0.99)
    mynetwork.add_central_battery(battery_1)

    # Add tariffs
    my_tariffs = Tariffs('Test')

    # Generate a list of time periods in half hour increments
    time_periods = util.generate_dates_in_range(datetime.datetime(year=2017,month=2,day=27,hour=1) , datetime.datetime(year=2017,month=2,day=27,hour=1) + datetime.timedelta(days = 1), 30)
    # Make empty df
    data_output = {
        "df_net_export" : pd.DataFrame(index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]),
        "df_network_energy_flows" : pd.DataFrame(index = time_periods, columns=['net_participant_export', 'central_battery_export', 'unallocated_local_solar', 'unallocated_central_battery_load']),
        "df_local_solar_import" : pd.DataFrame(index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]), 
        "df_participant_central_batt_import" : pd.DataFrame(index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]), 
        "df_local_solar_sales" : pd.DataFrame(index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]), 
        "df_central_batt_solar_sales" : pd.DataFrame(index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()])
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

        # Save any battery load left over after the allocation process to df_network_energy_flows
        data_output["df_network_energy_flows"].loc[time, 'unallocated_central_battery_load'] = available_batt_charging_load        

    # print(participants_list_sorted)
    # print(data_output)

    # ----------------------------------------------------------------------------------------------------------------------------
    # Financial flows

    # Charges are positive (if earning money then negative). Revenue is positive when earning money.
    financial_output = {
        "df_participant_variable_charge" : pd.DataFrame(index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]),
        "df_local_solar_import_charge" : pd.DataFrame(index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]), 
        "df_central_batt_import_charge" : pd.DataFrame(index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]), 
        "df_local_solar_sales_revenue" : pd.DataFrame(index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]), 
        "df_central_batt_solar_sales_revenue" : pd.DataFrame(index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]),
        "df_fixed_charge" : pd.DataFrame(index = time_periods, columns=[p.get_id() for p in mynetwork.get_participants()]),
        "df_dnsp_revenue" : pd.DataFrame(index = time_periods, columns=['grid_import_revenue_fixed','total_participant_grid_import_kWh','grid_import_revenue_variable','total_participant_local_solar_import_kWh','local_solar_import_revenue','total_participant_central_battery_import_kWh','central_batterY_import_revenue']),
        "df_retailer_revenue" : pd.DataFrame(index = time_periods, columns=['grid_import_revenue_fixed','total_participant_grid_import_kWh','grid_import_revenue_variable','total_participant_local_solar_import_kWh','local_solar_import_revenue','total_participant_central_battery_import_kWh','central_batterY_import_revenue'])
        }

    for time in time_periods:
        # Calc each participant in/out kWh
        for p in mynetwork.get_participants():

            net_export = data_output["df_net_export"].loc[time,p.get_id()]
            local_solar_import = data_output["df_local_solar_import"].loc[time,p.get_id()]
            participant_central_batt_import = data_output["df_participant_central_batt_import"].loc[time,p.get_id()]
            local_solar_sales = data_output["df_local_solar_sales"].loc[time,p.get_id()]
            central_batt_solar_sales = data_output["df_central_batt_solar_sales"].loc[time,p.get_id()]

            external_grid_import = abs(min(net_export,0)) - abs(max(0,local_solar_import)) - abs(max(0,participant_central_batt_import))

            financial_output["df_participant_variable_charge"].loc[time,p.get_id()] = my_tariffs.get_variable_tariff(time) * external_grid_import
            financial_output["df_local_solar_import_charge"].loc[time,p.get_id()] = my_tariffs.get_local_solar_tariff(time) * local_solar_import
            financial_output["df_central_batt_import_charge"].loc[time,p.get_id()] = my_tariffs.get_central_batt_tariff(time) * participant_central_batt_import
            financial_output["df_local_solar_sales_revenue"].loc[time,p.get_id()] = my_tariffs.get_local_solar_tariff(time) * local_solar_sales
            financial_output["df_central_batt_solar_sales_revenue"].loc[time,p.get_id()] = my_tariffs.get_central_batt_buy_tariff(time) * central_batt_solar_sales
            financial_output["df_fixed_charge"].loc[time,p.get_id()] = my_tariffs.get_fixed_tariff(TIME_PERIOD_LENGTH_MINS)


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

    

# print(run_en())

# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(run_en())

# print run_en_json()

