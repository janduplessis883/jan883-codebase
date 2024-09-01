import requests
import os

telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

def telegram_send(bot_message):
    send_text = "https://api.telegram.org/bot" + telegram_bot_token + "/sendMessage"
    response = requests.get(
        send_text,
        params={
            "chat_id": chat_id,
            "parse_mode": "Markdown",
            "text": bot_message,
        },
    )
    return response.json()


def telegram_send_image(image_path, caption=None):
    send_photo_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendPhoto"

    with open(image_path, 'rb') as image_file:
        files = {'photo': image_file}
        data = {
            'chat_id': chat_id,
            'caption': caption
        }
        response = requests.post(send_photo_url, files=files, data=data)

    return response.json()

# Example usage:
# response = telegram_send_image("path_to_your_image.jpg", caption="Here is your image!")
# print(response)
