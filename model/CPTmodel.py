from __init__ import db
class NFL(db.Model):
    __tablename__ = 'nfl_games'

    # Define the NFL games schema
    id = db.Column(db.Integer, primary_key=True)
    home_team = db.Column(db.Text, nullable=False)
    away_team = db.Column(db.Text, nullable=False)
    home_team_win_percentage = db.Column(db.Float, nullable=False)
    away_team_win_percentage = db.Column(db.Float, nullable=False)

def initNFL():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        
        """Sample data for NFL games"""
        games_data = [
            {'home_team': 'Seattle Seahawks', 'away_team': 'San Francisco 49ers', 'home_team_win_percentage': 60, 'away_team_win_percentage': 40},
            {'home_team': 'New England Patriots', 'away_team': 'Kansas City Chiefs', 'home_team_win_percentage': 45, 'away_team_win_percentage': 55},
        ]

        """Build sample NFL game data"""
        for game in games_data:
            try:
                # Create NFL game objects
                nfl_game = NFL(
                    home_team=game['home_team'],
                    away_team=game['away_team'],
                    home_team_win_percentage=game['home_team_win_percentage'],
                    away_team_win_percentage=game['away_team_win_percentage']
                )

                # Add NFL game data to the database
                db.session.add(nfl_game)
                db.session.commit()
            except IntegrityError:
                """Fails with bad or duplicate data"""
                db.session.rollback()
                print(f"Failed to add NFL game: {game}")

