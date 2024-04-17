from flask import request
from flask_cors import CORS
import json
import joblib
import flask

app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "seasdad(*2sffcra01^23sdet"

CORS(app)

# main index page (root route)
@app.route('/')
def home():
    return "<h1>Salary Prediction API</h1><p>BAIS:3300 - Digital Product Development</p><p>Jack Coyne</p>"

# predict route
@app.route('/predict', methods=['POST'])
def predict():
    model = joblib.load('salary_predict_model.ml')

    # Corrected: get values from json
    prediction_variables = request.get_json()
    print(prediction_variables)

    # store the json values into python variables
    age = prediction_variables['age']
    gender = prediction_variables['gender']
    country = prediction_variables['country']
    highest_deg = prediction_variables['highest_deg']
    coding_exp = prediction_variables['coding_exp']
    title = prediction_variables['title']
    company_size = prediction_variables['company_size']

    print(age, gender, country, highest_deg, coding_exp, title, company_size)

    # make prediction using the python variables

    salary_prediction = model.predict(
        [
            [
                int(age),
                int(gender),
                int(country),
                int(highest_deg),
                int(coding_exp),
                int(title),
                int(company_size)
            ]
        ]
    )

    print(salary_prediction)

    # convert NumPy array to Python list
    salary_prediction = salary_prediction.tolist()[0]

    # return the prediction as a JSON response
    return json.dumps({'salary_prediction': salary_prediction})