import requests
import json


# %%
def ask_ollama(
    user_prompt,
    system_prompt="You are a helpful AI assistant.",
    model="llama3.1",
    format="plain text",
    temp=0,
    max_tokens=0,
):
    """
    import the following for function to work:
    from helper883 import *
    """

    output_format = (
        f"PLEASE MAKE SURE YOUR OUTPUT IS IN THE FOLLOWING FORMAT: {format}."
    )
    # Define the endpoint URL and headers
    url = "http://localhost:11434/api/generate"  # Update the URL to match your server's endpoint
    headers = {
        "Content-Type": "application/json",
    }

    # Define the payload with the prompt or input text
    payload = {
        "model": model,
        "system": f"system_prompt {output_format}",
        "prompt": user_prompt,
        "max_tokens": max_tokens,
        "stream": False,
        "options": {
            "temperature": temp,
        },
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


def mini_check_ollama(
    document=None, claim=None, model="bespoke-minicheck:latest", format="text", temp="0"
):
    """
    Miniature fact-checking tool using Hugging Face's Transformers.

    Args:
        document (str, optional): The text to examine. Defaults to user input if not provided.
        claim (str, optional): The sentence to check against the document. Defaults to user input if not provided.
        model (str, optional): Name of the pre-trained language model to use. Defaults to "bespoke-minicheck:latest".
        format (str, optional): Output format. Currently only supports "text". Defaults to "text".
        temp (int or str, optional): Temperature value for the model's randomness. Defaults to 0.

    Returns:
        str: The result of the fact-checking ("Yes", "No", or explanation).

    Notes:
        This function is designed to be used in a sequential manner: pass in a document and claim, then use the output as input to another instance.
        If no document or claim are provided, the user will be prompted to enter them.
        The model takes as input a document (text) and a sentence and determines whether the sentence is supported by the document.

    Raises:
        Exception: If there is an error with the API request.
    """
    print(
        "Bespoke-MiniCheck\nThe model takes as input a document (text) and a sentence and determines whether the sentence is supported by the document. In order to fact-check a multi-sentence claim, the claim should first be broken up into sentences. The document does not need to be chunked unless it exceeds 32K tokens.\n"
    )

    if document == None and claim == None:
        document = input("📑 Document: (The text to examine) ")
        claim = input(
            "😥 Claim: (Determines if the sentence is supported by the document) "
        )

    # Define the endpoint URL and headers
    url = "http://localhost:11434/api/generate"  # Update the URL to match your server's endpoint
    headers = {
        "Content-Type": "application/json",
    }

    # Define the payload with the prompt or input text
    payload = {
        "model": model,  # Replace with your model's name
        "prompt": f"Document: {document}\nClaim: {claim} - Give a 'Yes' or 'No' answer and explain how you came to this conclution.",
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


# USING THE BESPOKE API
# import os
# from bespokelabs import BespokeLabs

# bl = BespokeLabs(
#     # This is the default and can be omitted
#     auth_token=os.environ.get("BESPOKE_API_KEY"),
# )

# response = bl.minicheck.factcheck.create(
#     claim="I like scrambled eggs.",
#     context="Eggs are my favourite food.",
# )
# print(response.support_prob)

# %%
