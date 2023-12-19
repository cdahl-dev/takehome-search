from flask import Flask, jsonify, request
from app.utils import get_log_events

app = Flask(__name__)

@app.route('/logs/')
def get_logs():
    result = {}

    try:
        filename = request.args.get('filename')

        kwargs = {}

        if request.args.get('n') and request.args.get('n').isnumeric():
            kwargs['n'] = int(request.args.get('n'))

        if request.args.get('keyword'):
            kwargs['keyword'] = request.args.get('keyword')
        
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

#if __name__ == '__main__':
#    app.run(threaded=True)