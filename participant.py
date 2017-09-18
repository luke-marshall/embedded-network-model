import numpy as np

class Participant: 
    def __init__(self, participant_id, participant_type, tariff_type, retailer):
        self.participant_id = participant_id
        self.participant_type = participant_type
        self.tariff_type = tariff_type
        self.retailer = retailer
    
    def print_attributes(self):
        print(self.participant_type, self.tariff_type, self.retailer)

    # TODO - make this work
    def calc_net_export(self, date_time, interval_min):
        return np.random.uniform(-10,10) 

    def get_id(self):
        return self.participant_id