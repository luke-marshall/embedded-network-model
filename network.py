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