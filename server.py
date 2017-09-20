
from flask import Flask 
app = Flask(__name__)
import main 

# test
@app.route("/")
def hello():
    return str(main.run_en())