# import API libs
from flask import Flask, request
import json

# import supportive function
import util


app = Flask(__name__)

@app.route("/test1", methods=["POST"])
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
        result_list = []
        for g in getJS:
            # read input json and one-hot encoding it
            input_list = util.getJsonValues(g)
            onehot = util.onehotEncoding(input_list)

            # calculate the predicted value
            outp = util.calculateOutput(onehot)
            result_list.append(outp[0][0])
    return json.dumps({"result": result_list})


if __name__ == "__main__":
    app.run(debug=True)

