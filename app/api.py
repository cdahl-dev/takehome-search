from flask import Flask, jsonify, request
from app.utils import get_log_events

app = Flask(__name__)

@app.route('/logs/')
def get_logs():
    """Returns the most recent lines from a given log file.

    Parameters
    ----------
    filename : str
        The filename to search in.
    n : int
        Number of lines to return (optional)
    keywords : str
        One or more words to search for - only lines matching all will be returned (optional).
    """
    result = {}

    try:
        filename = request.args.get('filename')

        kwargs = {}

        if request.args.get('n') and request.args.get('n').isnumeric():
            kwargs['n'] = int(request.args.get('n'))

        if request.args.get('keywords'):
            kwargs['keywords'] = request.args.get('keywords')
        
        log_events = get_log_events(filename, **kwargs)
        result = {
            'success': True,
            'count': len(log_events),
            'log_events': log_events
        }
    except Exception as e:
        result = {
            'success': False,
            'error_message': str(e)
        }
    
    return jsonify(result)
