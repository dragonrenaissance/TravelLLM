from flask import Flask, render_template, request, jsonify
from src.llm import *

app = Flask(__name__)

@app.route('/greet', methods=['POST'])
def greet():
    data = request.get_json()

    if 'name' in data:

        return jsonify({'message': CruateGen(data["name"])})
        #return jsonify({'message': data["name"]})
    else:
        return jsonify({'error': 'URL not provided'}), 400

# Define a route to render the HTML form
@app.route('/form', methods=['GET'])
def form():
    return render_template('form.html')


@app.route('/')
def home():
    return 'All is well...'

@app.route('/hello/')
def hello():
    return "hello"


@app.route('/activity/<url>')
def activity(url):
    
    return CruateGen(url)



