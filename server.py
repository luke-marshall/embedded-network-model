
from flask import Flask 
app = Flask(__name__)
import main 
import json

# test
@app.route("/")
def hello():
    result = main.run_en()
    return str(json.dumps(result))