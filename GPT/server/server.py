from flask import Flask, request, jsonify
import json
import sys
sys.path.append('../privateGPT')

from cronjob import queryGPT

app = Flask(__name__)

@app.route('/api/query', methods=['POST'])
def query():
    query = request.json['query']
    result = queryGPT(query)
    response = app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run()