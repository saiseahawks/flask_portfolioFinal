from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource

# Import the updated FootballScoreModel class
from model.experimentmodel import FootballScoreModel

experiment_api = Blueprint('experiment_api', __name__, url_prefix='/api/experiment')
api = Api(experiment_api)

class Predict(Resource):
    def post(self):
        # Get the team data from the request
        data = request.get_json()

        # Get the team names from the data
        team1 = data.get('team1')
        team2 = data.get('team2')

        # Get the singleton instance of the updated FootballScoreModel
        football_model = FootballScoreModel.get_instance()

        # Predict the winner likelihood of the football game
        # Since the method `predict_winner_likelihood` is not implemented yet in the updated model,
        # you need to decide how you want to predict the winner likelihood using the new features and model.
        # For example, you could return the predicted scores for both teams and let the client calculate the likelihood.
        prediction = {}  # Placeholder for the prediction result

        return jsonify(prediction)

# Add the Predict resource to the API with the /predict endpoint
api.add_resource(Predict, '/predict')

