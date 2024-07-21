import os
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import bz2

application = Flask(__name__)
app=application

def decompress_pickle(file):
    data = bz2.BZ2File(file, 'rb')
    data = pickle.load(data)
    return data

# Debugging: Print current working directory
print("Current working directory:", os.getcwd())

# Debugging: Check if file exists
file_path ='Notebooks\ccdp.pbz2'
if os.path.exists(file_path):
    print(f"File '{file_path}' exists.")
    model = decompress_pickle(file_path)
else:
    print(f"File '{file_path}' does not exist.")
    model = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        age = [int(request.form['age'])]
        bal_limit = [int(request.form['limit_bal'])]
        rs_6 = [int(request.form['april_rs'])]
        rs_5 = [int(request.form['may_rs'])]
        rs_4 = [int(request.form['june_rs'])]
        rs_3 = [int(request.form['july_rs'])]
        rs_2 = [int(request.form['august_rs'])]
        rs_1 = [int(request.form['september_rs'])]
        bill_6 = [int(request.form['bill_amt6'])]
        bill_5 = [int(request.form['bill_amt5'])]
        bill_4 = [int(request.form['bill_amt4'])]
        bill_3 = [int(request.form['bill_amt3'])]
        bill_2 = [int(request.form['bill_amt2'])]
        bill_1 = [int(request.form['bill_amt1'])]
        pay_6 = [int(request.form['pay_amt6'])]
        pay_5 = [int(request.form['pay_amt5'])]
        pay_4 = [int(request.form['pay_amt4'])]
        pay_3 = [int(request.form['pay_amt3'])]
        pay_2 = [int(request.form['pay_amt2'])]
        pay_1 = [int(request.form['pay_amt1'])]

    bill_amt_avg = [round(np.mean([bill_6, bill_5, bill_4, bill_3, bill_2, bill_1]), 2)]
    features = rs_1 + rs_2 + pay_1 + bill_1
    features = features + bal_limit + age + pay_2 + bill_2
    features = features + pay_3 + bill_3 + bill_4 + pay_4
    features = features + pay_6 + bill_5 + bill_6 + bill_amt_avg
    
    features_arr = [np.array(features)]

    if model:
        prediction = model.predict(features_arr)
    else:
        prediction = "Model not loaded due to missing file."

    return render_template('index.html',prediction=prediction)

if __name__ == "__main__":
    app.run