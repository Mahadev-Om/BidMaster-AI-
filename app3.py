import pandas as pd
from flask import Flask, request, jsonify
import joblib
from twilio.rest import Client
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

model = joblib.load('bidding_model.pkl')
df = pd.read_csv('cleaned_dataset_new_3.csv', low_memory=False)

app = Flask(__name__)

TWILIO_ACCOUNT_SID = 'AC48e040efe4ad48686f4337385b8b355c' 
TWILIO_AUTH_TOKEN = 'dddc33d9122b26e0be1b5e79f1adc6eb'
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

numeric_features = df.select_dtypes(include=['int64', 'float64']).columns
categorical_features = df.select_dtypes(include=['object']).columns

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean'))
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

df_processed = preprocessor.fit_transform(df)

feature_columns = df.drop(columns=['totalContractValue']).columns

def get_best_bid():
    features = df_processed[0].reshape(1, -1)
    best_bid_value = model.predict(features)[0]
    best_bid_supplier = df.iloc[0]['supplierLegalName']
    return best_bid_value, best_bid_supplier

@app.route('/send_best_bid', methods=['POST'])
def send_best_bid():
    phone_number = request.json.get('phone_number')
    if not phone_number:
        return jsonify({'error': 'Phone number is required'}), 400

    try:
        best_bid_value, best_bid_supplier = get_best_bid()
        message_body = f"The best bid is {best_bid_value} by {best_bid_supplier}."

        message = client.messages.create(
            body=message_body,
            from_='+19389465140',  
            to=phone_number
        )
        return jsonify({'message': 'Message sent successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
