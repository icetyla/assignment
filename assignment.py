import numpy as np
import json
import re
# import redis
from flask import Flask, request
from json import JSONEncoder

# encode all numpy types correctly into json
class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyArrayEncoder, self).default(obj)


app = Flask(__name__)
# cache = redis.Redis(host='redis', port=6379)


@app.route("/", methods = ['POST', 'GET'])
def shape():
    if request.method == 'POST':
        # organize corner points and build a 2d array
        cleanup = request.form['corner_points'].strip("[()]")
        splice = re.sub("[^0-9,.]","", cleanup).split(sep=',')
        data = np.array(splice)
        data = data.astype(float)
        data = np.resize(data, (4,2))

        # shape details
        xdistance = abs(data.min(axis=0)-data.max(axis=0))[0] 
        ydistance = abs(data.min(axis=0)-data.max(axis=0))[1]
        xstep = xdistance/(int(request.form['num_cols'])-1)
        ystep = ydistance/(int(request.form['num_rows'])-1)
        
        # coordinates for top left corner
        min_x = abs(data.min(axis=0))[0]   
        max_y = abs(data.max(axis=0))[1]
        adj_x = min_x
        adj_y = max_y


        # a triple list comprehension to create a 3 dimensional matrix
        solution = np.array([[[0 for k in range(2)] 
                            for j in range(int(request.form['num_cols']))] 
                            for i in range(int(request.form['num_rows']))], dtype = float)

        
        # double for loop to input each value into a node in the ndarray
        for o, row in enumerate(solution): 
            for p, pair in enumerate(row):      
                solution[o, p] = [adj_x, adj_y]
                adj_x += xstep
            adj_x = min_x
            adj_y -= ystep                      


        # serialization of the ndarray
        encodedSolution = json.dumps(solution, cls=NumpyArrayEncoder)
        return encodedSolution
    return '''<form method = "post">
    <p>Enter number of rows:</p>
    <p><input type = "text" name = "num_rows" /></p>
    <p>Enter number of columns:</p>
    <p><input type = "text" name = "num_cols" /></p>
    <p>Enter the corner points as a python list:</p>
    <p><input type = "text" name = "corner_points" /></p>
    <p><input type = "submit" value = "submit" /></p>
    </form>'''

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)