import csv
import os
from participant import CSV_Participant
import random
import humanhash
import string
import base64

class Network:
    def __init__(self, name) :
        self.name = name
        self.participant_list = []
        self.battery_list = []
        

    def test(self) :
        print('hello world')
        print(self.name)

    def add_participant(self, participant):
        self.participant_list.append(participant)

    def get_participants(self):
        return self.participant_list
    
    def calc_total_participant_export(self, date_time, interval_min):
        """Calculates the total participant export after local solar is traded."""
        total = 0
        for p in self.participant_list :
            total += p.calc_net_export(date_time, interval_min)
        return total
    
    def add_central_battery(self, battery):
        self.battery_list.append(battery)
    
    def get_batteries(self):
        return self.battery_list

    def add_participants_from_csv(self, data_dir, participant_csv):
        with open(os.path.join(data_dir,participant_csv)) as f:
            reader = csv.DictReader(f, delimiter = ",")
            for line in reader: 
                # print line
                participant = CSV_Participant(
                    participant_id=line['participant_id'],
                    participant_type=line['participant_type'],
                    retail_tariff_type=line['retail_tariff_type'],
                    network_tariff_type=line['network_tariff_type'],
                    retailer=line['retailer'],
                    solar_path=os.path.join(data_dir,line['solar_path']),
                    load_path=os.path.join(data_dir,line['load_path']),
                    solar_capacity=float(line['solar_capacity'])
                )
                self.add_participant(participant)
    

    def add_participants_from_csv_randomise_has_solar(self, data_dir, participant_csv, solar_participant_fraction = 0.5, random_seed=1000):
        with open(os.path.join(data_dir,participant_csv)) as f:
            reader = csv.DictReader(f, delimiter = ",")
            participants = []
            for line in reader: 
                # print line
                participant = CSV_Participant(
                    participant_id=line['participant_id'],
                    participant_type=line['participant_type'],
                    retail_tariff_type=line['retail_tariff_type'],
                    network_tariff_type=line['network_tariff_type'],
                    retailer=line['retailer'],
                    solar_path=os.path.join(data_dir,line['solar_path']),
                    load_path=os.path.join(data_dir,line['load_path']),
                    solar_capacity=float(line['solar_capacity'])
                )
                participants.append(participant)

            # Make an array of true/false whether a participant has solar. 
            num_solar_participants = int(round(float(len(participants)) * solar_participant_fraction))
            has_solar = []
            counter = 0
            for participant in participants:
                if counter < num_solar_participants:
                    has_solar.append(True)
                else:
                    has_solar.append(False)
                counter += 1
            # Jumble the list
            local_random = random.Random()
            local_random.seed(random_seed)
            local_random.shuffle(has_solar)
            
            # set participant's solar cap to zero if need be. 
            counter = 0
            for participant in participants:
                if not has_solar[counter]:
                    participant.solar_capacity = 0
                    participant.participant_id = participant.participant_id+'_non_solar'
                else:
                    participant.participant_id = participant.participant_id+'_solar'
                counter += 1

            # Add to the list of participants
            for participant in participants:
                self.add_participant(participant)

            # Generate a unique identifier for this spread of solar / not solar.
            digest = string.join([str(chr(i+97)) if has_solar[i] else '0' for i in range(len(has_solar))],"")
            digest = base64.b16encode(digest)
            unique_id = humanhash.humanize(digest, words=2)
            return unique_id
    



    def add_participants_from_dictlist_randomise_has_solar(self, lock,  dictlist, data_dir, participant_csv, solar_participant_fraction = 0.5, random_seed=1000):
        
        participants = []
        for line in dictlist: 
            # print line
            print(line['participant_id'])
            participant = CSV_Participant(
                participant_id=line['participant_id'],
                participant_type=line['participant_type'],
                retail_tariff_type=line['retail_tariff_type'],
                network_tariff_type=line['network_tariff_type'],
                retailer=line['retailer'],
                solar_path=os.path.join(data_dir,line['solar_path']),
                load_path=os.path.join(data_dir,line['load_path']),
                solar_capacity=float(line['solar_capacity']),
                lock=lock,
            )
            participants.append(participant)

        # Make an array of true/false whether a participant has solar. 
        num_solar_participants = int(round(float(len(participants)) * solar_participant_fraction))
        has_solar = []
        counter = 0
        for participant in participants:
            if counter < num_solar_participants:
                has_solar.append(True)
            else:
                has_solar.append(False)
            counter += 1
        # Jumble the list
        local_random = random.Random()
        local_random.seed(random_seed)
        local_random.shuffle(has_solar)
        
        # set participant's solar cap to zero if need be. 
        counter = 0
        for participant in participants:
            if not has_solar[counter]:
                participant.solar_capacity = 0
            counter += 1

        # Add to the list of participants
        for participant in participants:
            self.add_participant(participant)

        # Generate a unique identifier for this spread of solar / not solar.
        digest = string.join([str(chr(i+97)) if has_solar[i] else '0' for i in range(len(has_solar))],"")
        digest = base64.b16encode(digest)
        unique_id = humanhash.humanize(digest, words=2)
        return unique_id
    
        