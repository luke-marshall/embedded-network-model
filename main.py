import numpy as np



class Network:
    def __init__(self, name) :
        self.name = name
        self.participant_list = []

    def test(self) :
        print('hello world')
        print(self.name)

    def add_participant(self, participant):
        self.participant_list.append(participant)

    def get_paricipants(self):
        return self.participant_list
    
    def calc_excess_energy(self, date_time, interval_min):
        total = 0
        for p in self.participant_list :
            total += p.calc_net_export(date_time, interval_min)
        return total

mynetwork = Network('Byron')
mynetwork.test()

class Participant: 
    def __init__(self, participant_type, tariff_type, retailer):
        self.participant_type = participant_type
        self.tariff_type = tariff_type
        self.retailer = retailer
    
    def print_attributes(self):
        print(self.participant_type, self.tariff_type, self.retailer)

    # TODO - make this work
    def calc_net_export(self, date_time, interval_min):
        return np.random.uniform(0,10) 

class Battery:
    def __init__(self, cap_kWh, cap_kW, cycle_eff):
        """Make note: cycle efficiency must be between zero and one."""
        self.cap_kWh = cap_kWh
        self.cap_kW = cap_kW
        self.cycle_eff = cycle_eff
        self.charge_level_kWh = 0  
        self.num_cycles = 0      

    def charge(self, kWh):
        # Increase battery charge level by the input kWh
        amount_to_charge = min(self.cap_kWh - self.charge_level_kWh, kWh)
        self.charge_level_kWh += amount_to_charge * self.cycle_eff
        return kWh - amount_to_charge

    def discharge(self, kWh_request):
        discharge_amount = min(kWh_request, self.charge_level_kWh)
        self.charge_level_kWh -= discharge_amount
        self.num_cycles += float(discharge_amount) / float(self.cap_kWh)
        return discharge_amount

    def get_num_cycles(self):
        return self.num_cycles


participant_1 = Participant('solar', 'A', 'ENOVA')
participant_2 = Participant('load', 'B', 'ENOVA')

mynetwork.add_participant(participant_1)
mynetwork.add_participant(participant_2)

participant_list = mynetwork.get_paricipants()
print(participant_list)

for p in participant_list:
    print(p.calc_net_export(''))

print(mynetwork.calc_excess_energy(''))

