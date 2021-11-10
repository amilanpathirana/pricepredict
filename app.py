from flask import Flask, render_template, request
import pandas as pd
import pickle as pickle
from sklearn.preprocessing import LabelEncoder
import numpy as np
import joblib
from flask_pymongo import PyMongo



model1 = joblib.load('model.pkl')


mongo=PyMongo()



MAKES = [
    'honda',
    'ford',
    'toyota',
    'nissan',
    'mazda']


MODELS = ['civic', 'cr-v', 'hr-v', 'escape', 'fiesta', 'edge', 'cx-3',
          'cx-5', 'cx-7', 'corolla', 'rav4', 'highlander']
YEARS = list(range(1995, 2021))
MILEAGE = list(range(100, 5000, 100))


app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://amila:amila123@cluster0.wpswh.mongodb.net/mydb?retryWrites=true&w=majority'

mongo.init_app(app)


@app.route("/", methods=["GET", 'POST'])
def index():
    return render_template('index.html', makes=MAKES, models=MODELS, years=YEARS, mileage=MILEAGE)


@app.route('/calculate', methods=['POST','GET'])
def calculate():
    name = request.form.get('name')
    email = request.form.get('email')
    make = request.form.get('make')
    model = request.form.get('model')
    year = request.form.get('year')
    km = request.form.get('km')
    data = [make, model,year, km]

   
    idf = pd.DataFrame({'make': [make], 'model': [model], 'year': [ year], 'citympg': [km]})

    idf.make = idf.make.str.strip().str.replace(" ", "")
    idf.model= idf.model.str.strip().str.replace(" ", "")

    pkl_file1 = open('label_encoder_make.pkl', 'rb')
    le_make = pickle.load(pkl_file1)
    pkl_file1.close()
    idf['make'] = le_make.transform(idf['make'])

    pkl_file2 = open('label_encoder_model.pkl', 'rb')
    le_model= pickle.load(pkl_file2)
    pkl_file2.close()
    idf['model'] = le_model.transform(idf['model'])

    print(type(make))
    print(idf)

    modelin = np.array(idf)

    preds = model1.predict(modelin)
    print("Running local model")

    prediction = round(preds[0])

    print(prediction)
    '''
    preds = clf.predict(image1)
    print("Running local model")

    prediction = round(preds[0])

    print(prediction)'''

    collection=mongo.db.userinputs
    input_item= data
    collection.insert_one({'name': name, 'email':email, "make" : make, 'model':model,'year':year,'mileage':km})



    return render_template('results.html', prediction=prediction)



if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')