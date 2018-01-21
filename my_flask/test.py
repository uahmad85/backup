from flask import Flask, json
from flask import render_template, make_response 


app = Flask(__name__)


@app.route('/<name>')
def index(name):
    return make_response(json.dumps({'hello': name}))


app.run(debug=True, port=8000, host='0.0.0.0')
