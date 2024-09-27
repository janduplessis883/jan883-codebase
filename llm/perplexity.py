import os
from openai import OpenAI


def ask_perplexity(prompt):
    """
    Function to get a chat response from the Perplexity API using the provided prompt.

    Args:
    prompt (str): The prompt to send to the API.

    Returns:
    None: Displays the response content as Markdown.
    """
    # Get the API key from environment variables
    api_key = os.getenv("PERPLEXITY_API_KEY")

    if api_key is None:
        raise ValueError("API key not found in environment variables.")

    # Define the messages
    messages = [
        {
            "role": "system",
            "content": (
                "You are an artificial intelligence assistant and you need to "
                "engage in a helpful, detailed, polite conversation with a user."
            ),
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]

    # Initialize the OpenAI client
    client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")

    # Get the chat completion response
    response = client.chat.completions.create(
        model="llama-3.1-sonar-small-128k-online",
        messages=messages,
    )
    content = response.choices[0].message.content

    return content
