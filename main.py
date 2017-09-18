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

    

participant_1 = Participant('solar', 'A', 'ENOVA')
participant_2 = Participant('load', 'B', 'ENOVA')

mynetwork.add_participant(participant_1)
mynetwork.add_participant(participant_2)

participant_list = mynetwork.get_paricipants()
print(participant_list)

for p in participant_list:
    print(p.calc_net_export(''))

print(mynetwork.calc_excess_energy(''))

