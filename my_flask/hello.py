from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route('/<name>')
def index(name):
    return render_template('index.html', name=name)


@app.route('/add/<int:n1>/<int:n2>')
@app.route('/add/<float:n1>/<float:n2>')
@app.route('/add/<float:n1>/<int:n2>')
@app.route('/add/<int:n1>/<float:n2>')
def add(n1, n2):
    context = {'number1': n1, "number2":n2}
    return render_template('add.html', **context)


app.run(debug=True, port=8000, host='0.0.0.0')