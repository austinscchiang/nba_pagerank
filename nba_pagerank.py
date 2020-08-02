import csv


class NbaPagerank(object):
    CSV_REGULAR_SEASON = 'data/2018_2019/regular_season.csv'
    CSV_PLAYOFFS = 'data/2018_2019/playoffs.csv'


    def run(self):
        matches_regular_season = self.matches_regular_season()
        team_record_graph = self.build_graph(matches_regular_season)
        for _, team_record in team_record_graph.items():
            print(team_record)
        pass

    def run_iteration(self):
        pass

    def is_finished(self):
        pass

    def build_graph(self, matches):
        team_to_team_record = {}
        for match in matches:
            if match.loser not in team_to_team_record:
                team_to_team_record[match.loser] = NbaTeamRecord(match.loser)
            if match.winner not in team_to_team_record:
                team_to_team_record[match.winner] = NbaTeamRecord(match.winner)
            team_to_team_record[match.winner].record_win(match.loser)
        return team_to_team_record

    def matches_regular_season(self):
        return self._matches(self.CSV_REGULAR_SEASON)

    def matches_playoffs(self):
        return self._matches(self.CSV_PLAYOFFS)

    def _matches(self, matches_filename):
        with open(matches_filename) as matches_csv:
            matches_reader = csv.reader(matches_csv)
            return [
                NbaMatch(match[2], match[4])
                if int(match[3]) > int(match[5])
                else NbaMatch(match[4], match[2])
                for match in matches_reader
            ]

class NbaMatch(object):
    def __init__(self, winner, loser):
        self.winner = winner
        self.loser = loser

    def __repr__(self):
        return f"Winner: {self.winner} Loser: {self.loser}\n"
    


class NbaTeamRecord(object):
    def __init__(self, team_id):
        self.team_id = team_id
        self.wins_list = []

    def __repr__(self):
        wins_list_formatted = ", ".join(self.wins_list)
        wins_count = len(self.wins_list)
        return f"Team: {self.team_id} Win Count: {wins_count} Wins: {wins_list_formatted}\n"

    def record_win(self, team_id_loser):
        self.wins_list.append(team_id_loser)


NbaPagerank().run()

