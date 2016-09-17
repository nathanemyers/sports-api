from nba.models import Ranking

class WeekData:

    self.rankings = []

    def add_rank(self, data):
        self.rankings.append(data)

    def to_json(self):
        return

    def load_from_json(self, json):
        return

    def save(self):
        verify_length()
        verify_ranks()
        return

    def verify_length(self):
        if self.rankings.__len__ != 30:
            return False
        return True

    def verify_ranks(self):
        return True

