from flask import Flask, request, jsonify
from datetime import datetime
import contiguity
import os

contiguity_api_key = os.getenv("CONTIGUITY_API")
print(contiguity_api_key)

client = contiguity.login("your_token_here", True)


app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Webhook receiver that captures and processes the date field.
    """
    try:
        # Get the JSON data sent with the webhook
        data = request.get_json()

        # Log the entire webhook payload
        print("Webhook received:", data)

        # Capture the date field from the payload
        date_str = data.get('date')  # Example: "2024-12-06T14:30:00Z"

        if date_str:
            # Convert the date string to a Python datetime object
            webhook_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            print("Date captured from webhook:", webhook_date)
        else:
            print("Date field is missing in the webhook payload.")

        # Respond with a success message
        return jsonify({'status': 'success', 'message': 'Webhook received!', 'captured_date': date_str}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5020, debug=True)
