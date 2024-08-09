import requests
import json


def ask_ollama(user_prompt, model="llama3.1", format="text", temp="0"):
    """
    import the following for function to work:
    from helper883 import *
    """

    # Define the endpoint URL and headers
    url = "http://localhost:11434/api/generate"  # Update the URL to match your server's endpoint
    headers = {
        "Content-Type": "application/json",
    }

    # Define the payload with the prompt or input text
    payload = {
        "model": model,  # Replace with your model's name
        "prompt": f"{user_prompt}. <output_format>{format}</output_format>",
        "max_tokens": 0,  # Adjust as needed
        "stream": False,
        "temprature": temp,
    }

    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Check the response
    if response.status_code == 200:
        result = response.json()
        return result["response"]
    else:
        print("Error:", response.status_code, response.text)
        return False
