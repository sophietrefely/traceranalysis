import sys
import json
sys.stdout = sys.stderr

from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/sup')
def some_json():
    return json.dumps({'sup': 'lol'})

@app.route('/tracer', methods=['POST'])
def tracer():
    result = 'You gave me:' + str(request.form['asdf_dicks_lol'])
    result += 'You gave me:' + str(request.form['number_2_key_random_lol'])
    return result

if __name__ == '__main__':
    app.run()


