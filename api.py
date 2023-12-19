from flask import Flask, jsonify, request
from utils import get_log_events

app = Flask(__name__)

@app.route('/logs/')
def get_logs():
    filename = request.args.get('filename')
    keywords = request.args.get('keywords')

    kwargs = {}

    if request.args.get('n'):
        kwargs['n'] = int(request.args.get('n'))
    
    result = {
        'log_events': get_log_events(filename, **kwargs)
    }
    
    return jsonify(result)
