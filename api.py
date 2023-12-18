from flask import Flask, jsonify, request
from utils import get_log_events

app = Flask(__name__)

@app.route('/logs/')
def get_logs():
    filename = request.args.get('filename')
    n = request.args.get('n')
    keywords = request.args.get('keywords')
    return jsonify(get_log_events(filename))
