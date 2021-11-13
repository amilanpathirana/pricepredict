from flask import Flask, render_template,request
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





model1 = joblib.load('model.pkl')


mongo=PyMongo()




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
    

    
  
    if not name:
        return render_template('sell.html',form=form, message='Please Enter Your Name',makes=MAKES, models=MODELS, years=YEARS, mileage=MILEAGE)
    if not email:
        return render_template('sell.html',form=form, message='Please Enter Your Email',makes=MAKES, models=MODELS, years=YEARS, mileage=MILEAGE)
    if not file1:
        return render_template('sell.html',form=form, message='Please Submit Three Photos',makes=MAKES, models=MODELS, years=YEARS, mileage=MILEAGE)
    if not file2:
        return render_template('sell.html',form=form, message='Please Submit Three Photos',makes=MAKES, models=MODELS, years=YEARS, mileage=MILEAGE)
    if not file3:
        return render_template('sell.html',form=form, message='Please Submit Three Photos',makes=MAKES, models=MODELS, years=YEARS, mileage=MILEAGE)
    if not make:
        return render_template('sell.html',form=form,message='Please Enter Vehicle Make',makes=MAKES, models=MODELS, years=YEARS, mileage=MILEAGE)
    if not model:
        return render_template('sell.html',form=form,message='Please Enter Vehicle Model',makes=MAKES, models=MODELS, years=YEARS, mileage=MILEAGE)
    if not year:
        return render_template('sell.html',form=form,message='Please Enter Year of Manufacture',makes=MAKES, models=MODELS, years=YEARS, mileage=MILEAGE)
    if not km:
        return render_template('sell.html',form=form,message='Please Enter Vehicle Mileage',makes=MAKES, models=MODELS, years=YEARS, mileage=MILEAGE)

    collection=mongo.db.useruploads 
    
    mongo.save_file(file1.filename,file1)
    mongo.save_file(file2.filename,file2)
    mongo.save_file(file3.filename,file3)
    
    collection.insert({'show': False ,'name': name, 'email':email, "make" : make, 'model':model,'year':year,'mileage':km,'image1_name':file1.filename,'image2_name':file2.filename,'image3_name':file3.filename})

    return render_template('uploaded.html')





@app.route('/calculate', methods=['POST','GET'])
def calculate():
    name = request.form.get('name')
    email = request.form.get('email')
    make = request.form.get('make')
    model = request.form.get('model')
    year = request.form.get('year')
    km = request.form.get('km')




    if not name:
        return render_template('index.html',message='Please Enter Name',makes=MAKES, models=MODELS, years=YEARS, mileage=MILEAGE)
    
    if not email:
        return render_template('index.html',message='Please Enter Email',makes=MAKES, models=MODELS, years=YEARS, mileage=MILEAGE)

    if not make:
        return render_template('index.html',message='Please Enter Make',makes=MAKES, models=MODELS, years=YEARS, mileage=MILEAGE)

    if not model:
        return render_template('index.html',message='Please Enter Model',makes=MAKES, models=MODELS, years=YEARS, mileage=MILEAGE)

    if not year:
        return render_template('index.html',message='Please Enter Year',makes=MAKES, models=MODELS, years=YEARS, mileage=MILEAGE)

    if not km:
        return render_template('index.html',message='Please Enter Mileage',makes=MAKES, models=MODELS, years=YEARS, mileage=MILEAGE)


    


   
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
    
   
    prediction_h =int(math.ceil(prediction / 1000.0)) * 1000 + price_range


    prediction_l =int(math.floor(prediction / 1000.0)) * 1000 - price_range


    #Save To the Mongo Database

    collection=mongo.db.userinputs
    collection.insert_one({'name': name, 'email':email, "make" : make, 'model':model,'year':year,'mileage':km})




    return render_template('results.html', predictionh=prediction_h, predictionl=prediction_l)



if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')