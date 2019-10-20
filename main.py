# import API libs
from flask import Flask, request
import json
import numpy as np
# import supportive function
import util
from equations.Equations import Equations

app = Flask(__name__)
equations = Equations()

@app.route("/test", methods=["POST"])
def api():
    """This function read API as json format, calculate and return
    the result as a list"""

    # convert json input into list of dictionary, each dict is one
    # set of input data
    if request.headers['Content-Type'] == 'application/json':
        req_data = request.get_json(force=True)
        dict = json.dumps(req_data)
        getJS = json.loads(str(dict))

        # for each input data, calculate the predicted value
        results = equations.get_results(getJS)

    return json.dumps({"result": results})
    # return ""

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)

