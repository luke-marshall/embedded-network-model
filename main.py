
from network import Network
from participant import Participant
from battery import Battery, Central_Battery




mynetwork = Network('Byron')
mynetwork.test()

participant_1 = Participant('solar', 'A', 'ENOVA')
participant_2 = Participant('load', 'B', 'ENOVA')

mynetwork.add_participant(participant_1)
mynetwork.add_participant(participant_2)

participant_list = mynetwork.get_paricipants()
print(participant_list)

for p in participant_list:
    print(p.calc_net_export('', 30))

print(mynetwork.calc_total_participant_export('', 30))

