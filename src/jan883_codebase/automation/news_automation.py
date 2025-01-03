from webscraping.scrape_website import *
from llm.utils import *
from llm.ollama import ask_ollama
from telegram_api.bot import *
from datetime import datetime

# Get the current time
now = datetime.now()

# Format the time in a human-readable way
human_readable_time = now.strftime("%d-%b-%Y %H:%M:%S")

title = ["GADGETS", "TECHNICA NEWS", "INFORMATION TECHNOLOGY"]

# Scrape the websites
news = scrape_website(
    [
        "https://arstechnica.com/gadgets/",
        "https://arstechnica.com",
        "https://arstechnica.com/information-technology/",
    ],
    display_text=False,
)

# Zip the titles and news content together
news_stream = zip(title, news)

# Send the image with a caption
response = telegram_send_image(
    "images/ARS.png", caption=f"Arstechnica {human_readable_time}"
)

# Iterate over the zipped titles and news content
for t, n in news_stream:
    # Summarize the content using ask_ollama
    my_message = ask_ollama(
        f"Summarize this website content for me in bullet points: {n}",
        format="plain text",
    )

    # Send the summary via Telegram
    response = telegram_send(f"*{t}:* \n{my_message}")

    # Print the response for debugging or logging
    print(response)
    print()
