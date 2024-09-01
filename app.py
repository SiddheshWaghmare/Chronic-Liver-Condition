from flask import Flask, render_template, request, jsonify
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
import joblib

app = Flask(__name__)

# Load the trained model
model = joblib.load('liver_patient_model.pkl')

# Function to preprocess input data
def preprocess_input(age, gender, tot_bilirubin, direct_bilirubin, alkphos, sgpt, sgot, tot_proteins, albumin, ag_ratio):
    # Encoding gender
    gender_encoder = LabelEncoder()
    gender_encoded = gender_encoder.fit_transform([gender])[0]

    # Handling missing values
    imputer = SimpleImputer(strategy='mean')
    input_data = [[age, gender_encoded, tot_bilirubin, direct_bilirubin, alkphos, sgpt, sgot, tot_proteins, albumin, ag_ratio]]
    input_data_imputed = imputer.fit_transform(input_data)

    return input_data_imputed

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get user input
        age = float(request.form['age'])
        gender = request.form['gender']
        tot_bilirubin = float(request.form['tot_bilirubin'])
        direct_bilirubin = float(request.form['direct_bilirubin'])
        alkphos = float(request.form['alkphos'])
        sgpt = float(request.form['sgpt'])
        sgot = float(request.form['sgot'])
        tot_proteins = float(request.form['tot_proteins'])
        albumin = float(request.form['albumin'])
        ag_ratio = float(request.form['ag_ratio'])

        # Preprocess input data
        input_data = preprocess_input(age, gender, tot_bilirubin, direct_bilirubin, alkphos, sgpt, sgot, tot_proteins, albumin, ag_ratio)

        # Make prediction
        prediction = model.predict(input_data)[0]

        # Return prediction result
        if prediction == 1:
            result = 'The patient is likely to have liver disease.'
        else:
            result = 'The patient is likely to be healthy.'

        return jsonify({'result': result})

    except ValueError:
        return jsonify({'error': 'Invalid input! Please enter numerical values for all fields.'})

if __name__ == '__main__':
    app.run(debug=True,port=961)
