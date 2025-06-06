
from flask import Flask, request, jsonify
from twilio.rest import Client
from bidding_ml import get_best_bid  # Import the get_best_bid function from ML module

app = Flask(__name__)

TWILIO_ACCOUNT_SID = 'AC48e040efe4ad48686f4337385b8b355c'
TWILIO_AUTH_TOKEN = 'dddc33d9122b26e0be1b5e79f1adc6eb'
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

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

        return jsonify({'message': 'Bid sent successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
