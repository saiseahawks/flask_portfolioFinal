import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

class FootballScoreModel:
    """A class used to represent the Football Score Prediction Model.
    """
    _instance = None
    
    def __init__(self):
        self.model = None
        self.dt = None
        self.features = ['score_away', 'spread_favorite', 'over_under_line']
        self.target = 'score_home'
        self.football_data = None
    
    def _clean(self):
        self.football_data['score_difference'] = self.football_data['score_away'] - self.football_data['score_home']
        self.football_data['game_total'] = self.football_data['score_away'] + self.football_data['score_home']
        self.football_data.dropna(subset=['spread_favorite'])
        self.football_data.dropna(subset=['over_under_line'])
        self.football_data.dropna(subset=['team_favorite_id'])
        self.football_data.dropna(subset=['score_home', 'score_away', 'spread_favorite', 'over_under_line'], inplace=True)
        self.football_data['team_home'] = self.football_data.team_home.map(self.teams.set_index('team_name')['team_id'].to_dict())
        self.football_data['team_away'] = self.football_data.team_away.map(self.teams.set_index('team_name')['team_id'].to_dict())
        current_year = pd.Timestamp.now().year
        self.football_data = self.football_data[self.football_data['schedule_season'] >= current_year - 1]
    def _train(self):
        X = self.football_data[self.features]
        y = self.football_data[self.target]
        self.model = LinearRegression()
        self.model.fit(X, y)
        self.dt = DecisionTreeRegressor()
        self.dt.fit(X, y)
        
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
            cls._instance._load_data()
            cls._instance._clean()
            cls._instance._train()
        return cls._instance

    def _load_data(self):
        self.football_data = pd.read_csv('spreadspoke_scores.csv', header=0)
        self.teams = pd.read_csv('nfl_teams.csv', header = 0)
        
        
    def predict_winner_likelihood(self, team1, team2):
        winner = []
        for i, v in self.football_data['score_home'].items():
            if self.football_data['score_home'][i] > self.football_data['score_away'][i]:
                winner.append(self.football_data['team_home'][i])
            elif self.football_data['score_home'][i] < self.football_data['score_away'][i]:
                winner.append(self.football_data['team_away'][i])
            else:
                winner.append('Tie')

        self.football_data['winner'] = winner
        
        
        # Filter past data for matches involving the two teams
        team1_matches = self.football_data[(self.football_data['team_home'] == team1) | (self.football_data['team_away'] == team1)]
        team2_matches = self.football_data[(self.football_data['team_home'] == team2) | (self.football_data['team_away'] == team2)]

        # Concatenate the filtered data to get all matches involving both teams
        matches = pd.concat([team1_matches, team2_matches])

        # Calculate the average score of each team in past matches
        team1_avg_score = matches[matches['team_home'] == team1]['score_home'].mean() + matches[matches['team_away'] == team1]['score_away'].mean()
        team2_avg_score = matches[matches['team_home'] == team2]['score_home'].mean() + matches[matches['team_away'] == team2]['score_away'].mean()

        # Calculate the total points scored in past matches involving both teams
        total_score = team1_avg_score + team2_avg_score

        # Calculate the percentage likelihood for each team to win
        team1_likelihood = (team1_avg_score / total_score) * 100
        team2_likelihood = (team2_avg_score / total_score) * 100

        return {team1: team1_likelihood, team2: team2_likelihood}

    def feature_weights(self):
        return {feature: importance for feature, importance in zip(self.features, self.dt.feature_importances_)}