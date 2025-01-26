from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

# Path to the JSON file in the 'api' folder
JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), 'api', 'channels.json')

# Load channels data
def load_channels():
    try:
        with open(JSON_FILE_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save channels data
def save_channels(channels):
    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(channels, file, indent=4)

@app.route('/channels', methods=['GET'])
def get_channels():
    """
    Endpoint to retrieve all channels.
    """
    channels = load_channels()
    return jsonify(channels)

@app.route('/channels/<int:channel_id>', methods=['GET'])
def get_channel(channel_id):
    """
    Endpoint to retrieve a single channel by ID.
    """
    channels = load_channels()
    channel = next((ch for ch in channels if ch['id'] == channel_id), None)
    if channel:
        return jsonify(channel)
    return jsonify({"error": "Channel not found"}), 404

@app.route('/channels', methods=['POST'])
def add_channel():
    """
    Endpoint to add a new channel.
    """
    channels = load_channels()
    new_channel = request.json
    if not new_channel.get('id') or not new_channel.get('name') or not new_channel.get('category'):
        return jsonify({"error": "Invalid data"}), 400
    channels.append(new_channel)
    save_channels(channels)
    return jsonify(new_channel), 201

@app.route('/channels/<int:channel_id>', methods=['DELETE'])
def delete_channel(channel_id):
    """
    Endpoint to delete a channel by ID.
    """
    channels = load_channels()
    channel = next((ch for ch in channels if ch['id'] == channel_id), None)
    if channel:
        channels.remove(channel)
        save_channels(channels)
        return jsonify({"message": "Channel deleted successfully"}), 200
    return jsonify({"error": "Channel not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
