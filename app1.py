from flask import Flask, request, jsonify

app = Flask(__name__)

def find_best_bidding(data):
    best_bidding = data.loc[data['contractAmount'].idxmax()]
    return best_bidding

def send_email(recipient_email, subject, body):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    sender_email = "vishwa.patel2061@gmail.com"
    sender_password = "Vishwapatel@2061"
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        return "Email sent successfully"
    except Exception as e:
        return f"Failed to send email: {str(e)}"

@app.route('/recommend-bid', methods=['POST'])
def recommend_bid():
    recipient_email = request.json.get('email')
    
    if not recipient_email:
        return jsonify({'error': 'Email is required'}), 400

    import pandas as pd
    data = pd.read_csv('cleaned_dataset_new_3.csv')
    
    best_bidding = find_best_bidding(data)
    
    subject = "Best Suitable Bidding Recommendation"
    body = f"""
    Title: {best_bidding['title']}
    Procurement Number: {best_bidding['procurementNumber']}
    Contract Amount: {best_bidding['contractAmount']}
    Start Date: {best_bidding['contractStartDate']}
    End Date: {best_bidding['contractEndDate']}
    Contact Info: {best_bidding['contactInfoEmail']}
    """
    
    email_status = send_email(recipient_email, subject, body)
    
    if "successfully" in email_status:
        return jsonify({'message': 'Recommendation sent successfully'}), 200
    else:
        return jsonify({'error': email_status}), 500

if __name__ == '__main__':
    app.run(debug=True)
