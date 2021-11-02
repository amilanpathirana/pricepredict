from flask import Flask, render_template, request
import pandas as pd
import _pickle as pickle
from sklearn.preprocessing import LabelEncoder
import numpy as np
import joblib


MAKES = [
    'honda',
    'ford',
    'toyota',
    'nissan',
    'mazda']


MODELS = ['Civic', 'CRV', 'HRV', 'Escape', 'Fiesta', 'Edge', 'Cx3',
          'Cx5', 'Cx7', 'Cx9', 'Corolla', 'Rav4', 'Highlander', 'None']
YEARS = list(range(1995, 2021))
MILEAGE = list(range(100, 5000, 100))


app = Flask(__name__)


@app.route("/", methods=["GET", 'POST'])
def index():
    return render_template('index.html', makes=MAKES, models=MODELS, years=YEARS, mileage=MILEAGE)


@app.route('/calculate', methods=['POST'])
def calculate():
    name = request.form.get('name')
    email = request.form.get('email')
    make = request.form.get('make')
    model = request.form.get('model')
    year = request.form.get('year')
    km = request.form.get('km')
    data = [name, email, make, model, year, km]

    print(type(make))
    print(data)
    idf = pd.DataFrame({'make': [make], 'year': [year], 'highwaympg': [
        km], 'citympg': [km], 'enginehp': [year]})

    idf.make = idf.make.str.strip().str.replace(" ", "")

    pkl_file = open('label_encoder.pkl', 'rb')
    le_departure = pickle.load(pkl_file)
    pkl_file.close()
    idf['make'] = le_departure.transform(idf['make'])

    image1 = np.array(idf)

    '''
    preds = clf.predict(image1)
    print("Running local model")

    prediction = round(preds[0])

    print(prediction)'''

    return render_template('results.html', prediction=100000)



if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')