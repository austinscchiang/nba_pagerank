import csv
import numpy as np

class PageRank(object):
    def __init__(self, transition_matrix, ranks):
        assert len(M) > 0 and len(M[0]) == len(M)
        self.M = M
        self.num_teams = len(self.M) # M is a square matrix; N-by-N 2D numpy array.
        self.R_0 = np.full((self.N, 1), 1 / float(self.N))
        self.one_vector = np.ones((self.N, 1))

    # see https://en.wikipedia.org/wiki/PageRank#Iterative
    def run(self, iterations=100, damping_factor=0.85):
        R = self.R_0
        for i in range(iterations):
            R = np.add(d * np.matmul(self.M, R), (1 - d) / float(self.N) * self.one_vector)
        return R

class NbaPageRank(PageRank):
    CSV_REGULAR_SEASON = 'data/2018_2019/regular_season.csv'
    CSV_PLAYOFFS = 'data/2018_2019/playoffs.csv'

    def __init__(self, use_playoffs_data=False):
        self.use_playoffs_data = use_playoffs_data
        matches = self.matches_playoffs() if playoffs else self.matches_regular_season()
        self.team_record_graph = self.build_graph(matches)
        self.num_teams = len(self.team_record_graph)

        M = np.zeros((self.num_teams, self.num_teams))

        for i in range(self.num_teams):
            for j in range(self.num_teams):
                # edge j -> i means j has lost to i
                j_loss_list = self.team_record_graph[j].loss_list
                if i in j_loss_list:
                    M.itemset((i, j), 1 / float(len(j_loss_list)))

        M = M
        R_0 = np.full((self.num_teams, 1), 1 / float(self.num_teams))

        super().__init__(M, R_0)


    def print_graph(self):
        for _, team_record in self.team_record_graph.items():
            print(team_record)
        print(f"There are {self.num_teams} teams in total\n")

    def print_result(self, R, top=5):
        assert(top <= self.num_teams)
        flat = [score for score_list in R for score in score_list]
        team_id_score = [(self.team_id_to_name[team_id], score) for team_id, score in enumerate(flat)]
        score_sorted_desc = sorted(team_id_score, key=lambda x: x[1], reverse=True)
        print(f"Top {top} in {'playoffs' if self.playoffs else 'regular season'} (desc):")
        print(*score_sorted_desc[:top], sep='\n', end='\n'*2)

    def is_finished(self):
        pass

    def build_graph(self, matches):
        team_to_team_record = {}
        team_names = {match.loser for match in matches} | {match.winner for match in matches}
        self.team_name_to_id = {team_name: i for i, team_name in enumerate(team_names)}
        self.team_id_to_name = {i: team_name for i, team_name in enumerate(team_names)}

        for match in matches:
            loser_id = self.team_name_to_id[match.loser]
            winner_id = self.team_name_to_id[match.winner]
            if loser_id not in team_to_team_record:
                team_to_team_record[loser_id] = NbaTeamRecord(loser_id, match.loser)
            if winner_id not in team_to_team_record:
                team_to_team_record[winner_id] = NbaTeamRecord(winner_id, match.winner)
            team_to_team_record[winner_id].record_win(loser_id)
            team_to_team_record[loser_id].record_loss(winner_id)
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
    def __init__(self, team_id, team_name):
        self.team_id = team_id
        self.team_name = team_name
        self.wins_list = []
        self.loss_list = []

    def __repr__(self):
        wins_list_formatted = ", ".join(map(str, self.wins_list))
        loss_list_formatted = ", ".join(map(str, self.loss_list))
        wins_count = len(self.wins_list)
        loss_count = len(self.loss_list)
        return f"Team: {self.team_name} Win Count: {wins_count} Wins: {wins_list_formatted}\n Loss Count: {loss_count} Losses: {loss_list_formatted}\n"

    def record_win(self, team_id_loser):
        self.wins_list.append(team_id_loser)

    def record_loss(self, team_id_winner):
        self.loss_list.append(team_id_winner)

for use_playoffs_data in [False, True]:
    nba_pagerank = NbaPageRank(playoffs=use_playoffs_data)
    R = nba_pagerank.run(iterations=100, d=0.85)
    nba_pagerank.print_result(R)
