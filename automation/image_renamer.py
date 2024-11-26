import requests
import base64
from PIL import Image
import io
import os

# Define the directory to search for images
# directory = '/Volumes/JanBackupDrive/Pictures/ScreenShots'
directory = "/Volumes/JanBackupDrive/Pictures/ScreenShots"

# Define the image file extensions
image_extensions = [".jpg", ".jpeg", ".png"]

# Initialize an empty list to hold the files
list_of_files = []

# Iterate through each file in the directory
for filename in os.listdir(directory):
    # Check if the file exists, has an image extension, and starts with the prefix "CleanShot"
    if (
        os.path.exists(os.path.join(directory, filename))
        and filename.lower().endswith(tuple(image_extensions))
        and filename.startswith("CleanShot")
    ):
        list_of_files.append(filename)

print(f"\nList of files: {list_of_files}\n")

proceed = input("Continue? [Y/N]: ")

if proceed == "y" or proceed == "Y":

    for file in list_of_files:

        file_extention = file.split(".")[-1]

        # Open the image file you want to upload (replace with your actual image)
        image_path = f"/Volumes/JanBackupDrive/Pictures/ScreenShots/{file}"
        img = Image.open(image_path)

        # Convert the image to a bytes buffer in memory
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        image_bytes = buf.getvalue()

        # Convert the image bytes to Base64 string

        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        # Define your API endpoint URL
        api_url = "http://localhost:11434/api/generate"

        # Define the data payload as a JSON object
        data_payload = {
            "model": "llava-llama3",
            "prompt": "based on the content of the image suggest an appropriate file name for the image, only return the file name, without the file extention",
            "images": [base64_image],
            "stream": False,
        }

        # Set the API method (POST, GET, PUT, DELETE)
        method = "POST"

        # Make the API call with the data payload
        response = requests.request(method, api_url, json=data_payload)

        # Check if the response was successful
        if response.status_code == 200:
            print("API call successful!")
        else:
            print("Error:", response.text)

        # Print the response details for debugging purposes

        json_response = response.json()
        new_filename = json_response["response"]
        new_filename = new_filename.strip()  # Remove leading and trailing whitespace
        new_filename = new_filename.replace(" ", "_")  # Replace spaces with underscores
        new_filename = (
            new_filename.strip()
        )  # Make sure to strip the resulting filename again
        new_filename = new_filename.replace('"', "")
        new_filename = new_filename.split(".")[0]

        new_name = f"/Volumes/JanBackupDrive/Pictures/ScreenShots/{new_filename}.{file_extention}"
        print(f"✅ - {new_name}")
        try:
            os.replace(image_path, new_name)
            print("Renamed")
        except OSError as e:
            print(f"Failed to rename '{image_path}' to '{new_name}': {e}")

else:
    print("Exit Image_renamer")
