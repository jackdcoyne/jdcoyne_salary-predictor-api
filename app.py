from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__)
app.config["SECRET_KEY"] = "seasdad(*2sffcra01^23sdet"

# Enable CORS
CORS(app)

# Load the model once when the application starts
model = joblib.load('salary_predict_model.ml')

# Main index page (root route)
@app.route('/')
def home():
    return "<h1>Salary Prediction API</h1><p>BAIS:3300 - Digital Product Development</p><p>Jack Coyne</p>"

# Predict route to handle POST requests for making predictions
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Retrieve data from JSON payload
        prediction_variables = request.get_json()
        
        # Correcting the column names to match training data
        columns = ['age', 'gender', 'country', 'highest_deg', 'code_experience', 'current_title', 'company_size']
        # Ensure the JSON keys are in the correct order and named correctly
        input_data = [
            [
                prediction_variables['age'],
                prediction_variables['gender'],
                prediction_variables['country'],
                prediction_variables['highest_deg'],
                prediction_variables['coding_exp'],  # Assuming the key in JSON is still 'coding_exp'
                prediction_variables['title'],       # Assuming the key in JSON is still 'title'
                prediction_variables['company_size']
            ]
        ]
        input_df = pd.DataFrame(input_data, columns=columns)
        
        # Make prediction
        salary_prediction = model.predict(input_df)
        
        # Convert prediction result to list (if necessary)
        salary_prediction = salary_prediction.tolist()[0]
        
        # Return the prediction as a JSON response
        return jsonify({'salary_prediction': salary_prediction})
    
    except KeyError as e:
        # Handle missing data in JSON input
        return jsonify({'error': f'Missing key in input data: {str(e)}'}), 400
    except Exception as e:
        # Handle general errors
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
