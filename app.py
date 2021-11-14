from flask import Flask, render_template,request,url_for
from flask_wtf import FlaskForm
from wtforms import FileField

import pandas as pd
import pickle as pickle
from sklearn.preprocessing import LabelEncoder
import numpy as np
import joblib
from flask_pymongo import PyMongo
import math
from werkzeug.utils import secure_filename
import os

from savedvariables import *


# download the model

model1 = joblib.load('model.pkl')

# initializa MongoDB
mongo=PyMongo()

#Initialize Flask
app = Flask(__name__)


app.config['SECRET_KEY']='secretkey'

class MyForm(FlaskForm):
    image1=FileField('image1')
    image2=FileField('image2')
    image3=FileField('image3')

app.config['MONGO_URI'] = 'mongodb+srv://amila:amila123@cluster0.wpswh.mongodb.net/mydb?retryWrites=true&w=majority'

mongo.init_app(app)


@app.route("/", methods=["GET", 'POST'])
def index():
    return render_template('index.html', makes=MAKES, models=MODELS, years=YEARS, mileage=MILEAGE)


@app.route('/sell',methods=["GET","POST"])
def sell():
    form=MyForm()
    return render_template('sell.html',form=form,  makes=MAKES, models=MODELS, years=YEARS, mileage=MILEAGE)




@app.route('/upload',methods=['GET','POST'])
def upload():
    
    name= request.form.get('name')
    email = request.form.get('email')
    make = request.form.get('make')
    model = request.form.get('model')
    year = request.form.get('year')
    km = request.form.get('km')
    form=MyForm()

    file1=request.files['image1']
    file2=request.files['image2']
    file3=request.files['image3']
    

    
    if not name or not email or not make or not model or not year or not km or not file1 or not file2 or not file3:
        return render_template('sell.html',message='Please Enter All Feilds',makes=MAKES, models=MODELS, years=YEARS, mileage=MILEAGE) 


    collection=mongo.db.useruploads 
    
    mongo.save_file(file1.filename,file1)
    mongo.save_file(file2.filename,file2)
    mongo.save_file(file3.filename,file3)
    
    collection.insert({'show': False ,'name': name, 'email':email, "make" : make, 'model':model,'year':year,'mileage':km,'image1_name':file1.filename,'image2_name':file2.filename,'image3_name':file3.filename})

    return render_template('uploaded.html')

@app.route('/getimage1/<filename>')
def getimage1(filename):
    return mongo.send_file(filename)


@app.route('/advert/<username>')
def addvert(username):
    user=mongo.db.useruploads.find_one_or_404({'name':username})
    filename=user['image1_name']

    return f'''
     <h1>{user}</h1>
     <h1>{filename}</h1>
     <img src ="{url_for('index',filename=filename)}">
    '''





@app.route('/calculate', methods=['POST','GET'])
def calculate():
    name = request.form.get('name')
    email = request.form.get('email')
    make = request.form.get('make')
    model = request.form.get('model')
    year = request.form.get('year')
    km = request.form.get('km')


    if not name or not email or not make or not model or not year or not km:
        return render_template('index.html',message='Please Enter All Feilds',makes=MAKES, models=MODELS, years=YEARS, mileage=MILEAGE)

   
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

    modelin = np.array(idf)

    preds = model1.predict(modelin)
    print("Running local model")
    prediction = round(preds[0])
    print(prediction)
    
   
    prediction_h =int(math.ceil(prediction / 1000.0)) * 1000 + price_range
    prediction_l =int(math.floor(prediction / 1000.0)) * 1000 - price_range


    #Save To the Mongo Database
    collection=mongo.db.userinputs
    collection.insert_one({'name': name, 'email':email, "make" : make, 'model':model,'year':year,'mileage':km})

    return render_template('results.html', predictionh=prediction_h, predictionl=prediction_l)



if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')