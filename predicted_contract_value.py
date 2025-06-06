from flask import Flask, request, jsonify
import joblib
import pandas as pd

# Load the trained model
model = joblib.load('C:/Users/Vishwa/Downloads/bidding_model.pkl')

app = Flask(__name__)

# Function to preprocess date columns
def preprocess_dates(data, date_columns):
    for col in date_columns:
        data[col] = pd.to_datetime(data[col], format='%d/%m/%Y', dayfirst=True, errors='coerce')
        # Convert datetime to Unix timestamp
        data[col] = data[col].astype('int64') / 10**9
    return data

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get the input data from the request
    data = request.json

    # Convert the input data to a DataFrame
    df = pd.DataFrame([data])

    # Preprocess the date columns
    date_columns = ['contractAwardDate', 'contractStartDate', 'contractEndDate']
    df = preprocess_dates(df, date_columns)

    # Define the features to be used
    features = ['contractAwardDate', 'contractStartDate', 'contractEndDate', 
                'procurementMethod', 'selectionCriteria', 'supplierLegalName', 
                'contractStatus']
    X = df[features]

    # Predict using the trained model
    y_pred = model.predict(X)

    # Return the prediction
    return jsonify({'predicted_contract_value': y_pred[0]})

if __name__ == '__main__':
    app.run(debug=True)
