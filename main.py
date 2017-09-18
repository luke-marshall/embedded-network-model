
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

mynetwork = Network('Byron')
mynetwork.test()

class Participant: 
    def __init__(self, participant_type, tariff_type, retailer):
        self.participant_type = participant_type
        self.tariff_type = tariff_type
        self.retailer = retailer
    
    def print_attributes(self):
        print(self.participant_type, self.tariff_type, self.retailer)

    def calc_net_export(self, time_stamp)

participant_1 = Participant('solar', 'A', 'ENOVA')
participant_2 = Participant('load', 'B', 'ENOVA')

mynetwork.add_participant(participant_1)
mynetwork.add_participant(participant_2)

participant_list = mynetwork.get_paricipants()
print(participant_list)

for p in participant_list:
    p.print_attributes()