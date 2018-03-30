import pandas as pd


class Results():
	def __init__(self, time_periods, participant_ids):
		# Make empty df
		self.data_output = {
			"df_net_export" : pd.DataFrame(0,index = time_periods, columns=[p for p in participant_ids]),
			"df_network_energy_flows" : pd.DataFrame(0,index = time_periods, columns=['net_participant_export', 'central_battery_export', 'unallocated_local_solar', 'unallocated_central_battery_load','gross_participant_grid_import','gross_participant_local_solar_import','gross_participant_central_battery_import']),
			"df_local_solar_import" : pd.DataFrame(0,index = time_periods, columns=[p for p in participant_ids]), 
			"df_participant_central_batt_import" : pd.DataFrame(0,index = time_periods, columns=[p for p in participant_ids]), 
			"df_local_solar_sales" : pd.DataFrame(0,index = time_periods, columns=[p for p in participant_ids]), 
			"df_central_batt_solar_sales" : pd.DataFrame(0,index = time_periods, columns=[p for p in participant_ids]),
			"df_export_to_grid_solar_sales" : pd.DataFrame(0,index = time_periods, columns=[p for p in participant_ids]),
			"df_external_grid_elec_import": pd.DataFrame(0,index = time_periods, columns=[p for p in participant_ids])
			}
	
	def set_net_export(self, time, participant_id, value):
		self.data_output['df_net_export'].loc[time,participant_id] = value
	
	def get_net_export(self, time, participant_id):
		return self.data_output['df_net_export'].loc[time,participant_id]

	# NOTE there was a typo here where we werent setting it to participant id but the actual participant object. might have been causing an issue.
	# If differences come out in results, I'd suggest this might have been a cause
	# To test that, try passing the participant object in the participant id spot and see if it makes a difference. 
	def set_local_solar_import(self, time, participant_id, value):
		self.data_output["df_local_solar_import"].loc[time, participant_id] = value
	def get_local_solar_import(self, time, participant_id):
		return self.data_output["df_local_solar_import"].loc[time, participant_id]

	# NOTE there was a typo here where we werent setting it to participant id but the actual participant object. might have been causing an issue.
	# If differences come out in results, I'd suggest this might have been a cause
	# To test that, try passing the participant object in the participant id spot and see if it makes a difference. 
	def set_participant_central_batt_import(self, time, participant_id, value):
		self.data_output["df_participant_central_batt_import"].loc[time, participant_id] = value
	def get_participant_central_batt_import(self, time, participant_id):
		return self.data_output["df_participant_central_batt_import"].loc[time, participant_id]

	# NOTE there was a typo here where we werent setting it to participant id but the actual participant object. might have been causing an issue.
	# If differences come out in results, I'd suggest this might have been a cause
	# To test that, try passing the participant object in the participant id spot and see if it makes a difference. 
	def set_local_solar_sales(self, time, participant_id, value):
		self.data_output["df_local_solar_sales"].loc[time, participant_id] = value
	def get_local_solar_sales(self, time, participant_id):
		return self.data_output["df_local_solar_sales"].loc[time, participant_id]

	# NOTE there was a typo here where we werent setting it to participant id but the actual participant object. might have been causing an issue.
	# If differences come out in results, I'd suggest this might have been a cause
	# To test that, try passing the participant object in the participant id spot and see if it makes a difference. 
	def set_central_batt_solar_sales(self, time, participant_id, value):
		self.data_output["df_central_batt_solar_sales"].loc[time, participant_id] = value
	def get_central_batt_solar_sales(self, time, participant_id):
		return self.data_output["df_central_batt_solar_sales"].loc[time, participant_id]

	def set_export_to_grid_solar_sales(self, time, participant_id, value):
		self.data_output["df_export_to_grid_solar_sales"].loc[time,participant_id] = value
	def get_export_to_grid_solar_sales(self, time, participant_id,):
		return self.data_output["df_export_to_grid_solar_sales"].loc[time,participant_id]

	def set_external_grid_elec_import(self, time, participant_id, value):
		self.data_output["df_external_grid_elec_import"].loc[time,participant_id] = value
	def get_external_grid_elec_import(self, time, participant_id):
		return self.data_output["df_external_grid_elec_import"].loc[time,participant_id]


	# 'Network Energy Flows'
	def set_net_participant_export(self, time, value):
		self.data_output['df_network_energy_flows'].loc[time, 'net_participant_export'] = value
	
	def get_net_participant_export(self, time):
		return self.data_output['df_network_energy_flows'].loc[time, 'net_participant_export']
	
	def set_central_battery_export(self, time, value):
		self.data_output['df_network_energy_flows'].loc[time, 'central_battery_export'] = value
	
	def get_central_battery_export(self, time):
		return self.data_output['df_network_energy_flows'].loc[time, 'central_battery_export']
	
	# TODO I think this should be labelled import, as our convention is normally subject -> action with the action as positive. 
	def set_net_network_export(self, time, value):
		self.data_output['df_network_energy_flows'].loc[time, 'net_network_export'] = value

	def set_unallocated_local_solar(self, time, value):
		self.data_output["df_network_energy_flows"].loc[time, 'unallocated_local_solar'] = value
	
	def set_unallocated_central_battery_load(self, time, value):
		self.data_output["df_network_energy_flows"].loc[time, 'unallocated_central_battery_load'] = value        

	def set_gross_participant_grid_import(self, time, value):
		self.data_output["df_network_energy_flows"].loc[time, 'gross_participant_grid_import'] = value
	
	def get_gross_participant_grid_import(self, time):
		return self.data_output["df_network_energy_flows"].loc[time, 'gross_participant_grid_import']
	
	def set_gross_participant_local_solar_import(self, time, value):
		self.data_output["df_network_energy_flows"].loc[time, 'gross_participant_local_solar_import'] = value
	
	def get_gross_participant_local_solar_import(self, time):
		return self.data_output["df_network_energy_flows"].loc[time, 'gross_participant_local_solar_import']
	
	def set_gross_participant_central_battery_import(self, time, value):
		self.data_output["df_network_energy_flows"].loc[time, 'gross_participant_central_battery_import'] = value

	def get_gross_participant_central_battery_import(self, time):
		return self.data_output["df_network_energy_flows"].loc[time, 'gross_participant_central_battery_import']

