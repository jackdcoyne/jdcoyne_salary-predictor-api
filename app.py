from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Salary Prediction API</h1><p>BAIS:3300 - Digital Product Development</p><p>Jack Coyne</p>"

@app.route("/predict", methods=["POST"])
def predict():
    print("Received a POST request to /predict.")
    # Capture data from the form
    form = request.form  # Form data captured
    print("Form data extracted:", form)

    # Extract user data from the form and save it in a dictionary
    salary_predict_variables = {
        "age": form["age"],
        "gender": form["gender"],
        "country": form["country"],
        "highest_deg": form["highest_deg"],
        "coding_exp": form["coding_exp"],
        "title": form["title"],
        "company_size": form["company_size"],
    }

    print("Prepared data for API:", salary_predict_variables)

    # Endpoint where the API is expected to be available
    api_url = "http://localhost:5000/api/predict"  # Adjust this URL based on your API deployment
    headers = {"Content-Type": "application/json"}

    try:
        # Send data to the API as JSON and receive the response
        response = requests.post(api_url, json=salary_predict_variables, headers=headers)
        
        if response.status_code == 200:
            prediction = response.json()  # Parsing the JSON response
            print("API response:", prediction)
            return render_template("index.html", prediction=prediction)
        else:
            print(f"API error: Status code {response.status_code}")
            error_message = f"API Error: Server responded with status code {response.status_code}"
            return render_template("index.html", error=error_message)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return render_template("index.html", error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
