from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/logs/')
def get_logs():
    filename = request.args.get('filename')
    n = request.args.get('n')
    keywords = request.args.get('keywords')
    return jsonify("")
