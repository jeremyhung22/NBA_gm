from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["nba_salaries"]
collection = db["players"]

@app.route('/api/players', methods=['GET'])
def get_players_by_last_name():
    last_name = request.args.get('name')  # The last name is already passed

    if not last_name:
        return jsonify({"error": "Please provide a last name"}), 400

    last_name = last_name.lower()  # Convert input to lowercase

    # MongoDB case-insensitive query using $toLower
    players = collection.find({
        "$expr": {
            "$eq": [
                {"$toLower": {"$arrayElemAt": [{"$split": ["$name", " "]}, -1]}}, 
                last_name
            ]
        }
    })

    # Convert MongoDB cursor to a list and remove `_id`
    players_list = [{key: value for key, value in player.items() if key != "_id"} for player in players]

    if players_list:
        return jsonify(players_list), 200
    else:
        return jsonify({"error": "No players found with the provided last name"}), 404
    



if __name__ == '__main__':
    app.run(debug=True)
