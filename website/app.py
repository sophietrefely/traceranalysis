import sys
import json
sys.stdout = sys.stderr

from flask import Flask, request
app = Flask(__name__)
app.debug = True

from tracerutils import (
    do_tracer_analysis,
    prepare_data_for_analysis,
    prepare_unlabeled_for_analysis
)
    
@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/sup')
def some_json():
    return json.dumps({'sup': 'lol'})

@app.route('/tracer', methods=['POST'])
def tracer():
    # TODO don't fix newline escaping like this!!!
    
    the_data = prepare_data_for_analysis(
        request.form['labeledData'].replace('\\n', '\n')
    )
    the_unlabeled_data = prepare_unlabeled_for_analysis(
        request.form['unlabeledData'].replace('\\n', '\n')
    )
    
    # TODO is calling list here really necessary
    # Was added because do_tracer_analysis returns numpy
    return json.dumps(do_tracer_analysis(the_data, the_unlabeled_data).tolist())

if __name__ == '__main__':
    app.run()


