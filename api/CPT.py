from flask import Blueprint, request, jsonify
from model.CPTmodel import NFL, db

CPT_api = Blueprint('CPT_api', __name__)

@CPT_api.route('/nfl_games', methods=['POST'])
def create_nfl_game():
    try:
        data = request.get_json()
        required_fields = ['home_team', 'away_team', 'home_team_win_percentage', 'away_team_win_percentage']
        
        # Validate the presence of required data
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Missing data, {field} field must be provided'}), 400
        
        # Create a new NFL game object
        new_game = NFL()
        
        # Update attributes based on the provided data
        for field, value in data.items():
            setattr(new_game, field, value)

        # Add the game to the database
        db.session.add(new_game)
        db.session.commit()
        
        return jsonify({'message': 'NFL game created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create NFL game', 'details': str(e)}), 500


@CPT_api.route('/nfl_games', methods=['GET'])
def get_nfl_games():
    try:
        games = NFL.query.all()
        return jsonify([{
            'home_team': game.home_team,
            'away_team': game.away_team,
            'home_team_win_percentage': game.home_team_win_percentage,
            'away_team_win_percentage': game.away_team_win_percentage
        } for game in games]), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve NFL games', 'details': str(e)}), 500
