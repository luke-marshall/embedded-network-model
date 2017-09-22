
from flask import Flask 
from flask import jsonify
app = Flask(__name__)
import main 
import json

# test
@app.route("/")
def hello():
    result = main.run_en_json()
    # return json.dumps(result)
    return jsonify(result)