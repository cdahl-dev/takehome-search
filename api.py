from flask import Flask, jsonify, request
from utils import get_log_events

app = Flask(__name__)

@app.route('/logs/')
def get_logs():
    filename = request.args.get('filename')

    kwargs = {}

    if request.args.get('n'):
        kwargs['n'] = int(request.args.get('n'))

    if request.args.get('keyword'):
        kwargs['keyword'] = request.args.get('keyword')
    
    log_events = get_log_events(filename, **kwargs)
    result = {
        'count': len(log_events),
        'log_events': log_events
    }
    
    return jsonify(result)
