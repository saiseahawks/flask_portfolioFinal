from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from random import randrange

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nfl_teams.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Team class to manage actions in the 'teams' table
class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    abbreviation = db.Column(db.String(3), unique=True, nullable=False)
    city = db.Column(db.String(255), nullable=False)

    def __init__(self, name, abbreviation, city):
        self.name = name
        self.abbreviation = abbreviation
        self.city = city

    def __repr__(self):
        return f"Team('{self.name}', '{self.abbreviation}', '{self.city}')"

# Create the database and tables
db.create_all()

# Add test data for teams
def init_teams():
    teams_data = [
        {"name": "Arizona Cardinals", "abbreviation": "ARI", "city": "Arizona"},
        {"name": "Atlanta Falcons", "abbreviation": "ATL", "city": "Atlanta"},
        {"name": "Baltimore Ravens", "abbreviation": "BAL", "city": "Baltimore"},
        {"name": "Buffalo Bills", "abbreviation": "BUF", "city": "Buffalo"},
        {"name": "Carolina Panthers", "abbreviation": "CAR", "city": "Carolina"},
        {"name": "Chicago Bears", "abbreviation": "CHI", "city": "Chicago"},
        {"name": "Cincinnati Bengals", "abbreviation": "CIN", "city": "Cincinnati"},
        {"name": "Cleveland Browns", "abbreviation": "CLE", "city": "Cleveland"},
        {"name": "Dallas Cowboys", "abbreviation": "DAL", "city": "Dallas"},
        {"name": "Denver Broncos", "abbreviation": "DEN", "city": "Denver"},
        {"name": "Detroit Lions", "abbreviation": "DET", "city": "Detroit"},
        {"name": "Green Bay Packers", "abbreviation": "GB", "city": "Green Bay"},
        {"name": "Houston Texans", "abbreviation": "HOU", "city": "Houston"},
        {"name": "Indianapolis Colts", "abbreviation": "IND", "city": "Indianapolis"},
        {"name": "Jacksonville Jaguars", "abbreviation": "JAX", "city": "Jacksonville"},
        {"name": "Kansas City Chiefs", "abbreviation": "KC", "city": "Kansas City"},
        {"name": "Las Vegas Raiders", "abbreviation": "LV", "city": "Las Vegas"},
        {"name": "Los Angeles Chargers", "abbreviation": "LAC", "city": "Los Angeles"},
        {"name": "Los Angeles Rams", "abbreviation": "LAR", "city": "Los Angeles"},
        {"name": "Miami Dolphins", "abbreviation": "MIA", "city": "Miami"},
        {"name": "Minnesota Vikings", "abbreviation": "MIN", "city": "Minnesota"},
        {"name": "New England Patriots", "abbreviation": "NE", "city": "New England"},
        {"name": "New Orleans Saints", "abbreviation": "NO", "city": "New Orleans"},
        {"name": "New York Giants", "abbreviation": "NYG", "city": "New York"},
        {"name": "New York Jets", "abbreviation": "NYJ", "city": "New York"},
        {"name": "Philadelphia Eagles", "abbreviation": "PHI", "city": "Philadelphia"},
        {"name": "Pittsburgh Steelers", "abbreviation": "PIT", "city": "Pittsburgh"},
        {"name": "San Francisco 49ers", "abbreviation": "SF", "city": "San Francisco"},
        {"name": "Seattle Seahawks", "abbreviation": "SEA", "city": "Seattle"},
        {"name": "Tampa Bay Buccaneers", "abbreviation": "TB", "city": "Tampa Bay"},
        {"name": "Tennessee Titans", "abbreviation": "TEN", "city": "Tennessee"},
        {"name": "Washington Football Team", "abbreviation": "WAS", "city": "Washington"}
    ]


    for team_data in teams_data:
        team = Team(**team_data)
        db.session.add(team)

    db.session.commit()
