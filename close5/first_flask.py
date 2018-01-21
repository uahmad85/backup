from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello world"

app.run(debug=True, port=8000, host='0.0.0.0')
