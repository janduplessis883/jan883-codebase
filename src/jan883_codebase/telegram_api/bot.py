import requests
import os

telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")


def telegram_send(bot_message, chat_id=chat_id):
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


def telegram_send_image(image_path, chat_id=chat_id, caption=None):
    send_photo_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendPhoto"

    with open(image_path, "rb") as image_file:
        files = {"photo": image_file}
        data = {"chat_id": chat_id, "caption": caption}
        response = requests.post(send_photo_url, files=files, data=data)

    return response.json()


# Example usage:
# response = telegram_send_image("path_to_your_image.jpg", caption="Here is your image!")
# print(response)


def telegram_send_video(video_path, chat_id=chat_id, caption=None, timeout=10):
    """
    Sends a video to a Telegram chat using the Telegram Bot API.

    :param video_path: Path to the video to be sent.
    :param caption: Optional caption for the video.
    :param timeout: Timeout for the request in seconds (default is 10).
    :return: JSON response from the Telegram API.
    """
    send_video_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendVideo"

    try:
        with open(video_path, "rb") as video_file:
            files = {"video": video_file}
            data = {"chat_id": chat_id, "caption": caption}
            response = requests.post(
                send_video_url, files=files, data=data, timeout=timeout
            )
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    except FileNotFoundError:
        print(f"The file at {video_path} was not found.")
        return None


def telegram_send_document(document_path, chat_id=chat_id, caption=None, timeout=10):
    """
    Sends a document to a Telegram chat using the Telegram Bot API.

    :param document_path: Path to the document to be sent.
    :param caption: Optional caption for the document.
    :param timeout: Timeout for the request in seconds (default is 10).
    :return: JSON response from the Telegram API.
    """
    send_document_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendDocument"

    try:
        with open(document_path, "rb") as document_file:
            files = {"document": document_file}
            data = {"chat_id": chat_id, "caption": caption}
            response = requests.post(
                send_document_url, files=files, data=data, timeout=timeout
            )
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    except FileNotFoundError:
        print(f"The file at {document_path} was not found.")
        return None
