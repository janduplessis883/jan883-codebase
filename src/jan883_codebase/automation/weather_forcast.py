from datetime import datetime

import openmeteo_requests
import pandas as pd
import requests
import requests_cache
from loguru import logger
from retry_requests import retry

logger.add("log/weather.log", rotation="5000 KB")

current_time = datetime.now()


def main():
    # Setup Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Weather API parameters
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 51.5085,
        "longitude": -0.1257,
        "hourly": [
            "temperature_2m",
            "apparent_temperature",
            "rain",
            "cloud_cover",
            "cloud_cover_low",
            "cloud_cover_mid",
            "cloud_cover_high",
        ],
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location
    response = responses[0]
    logger.info(f"API Response: {response}")
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process hourly data
    hourly = response.Hourly()
    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        ),
        "temperature_2m": hourly.Variables(0).ValuesAsNumpy(),
        "apparent_temperature": hourly.Variables(1).ValuesAsNumpy(),
        "rain": hourly.Variables(2).ValuesAsNumpy(),
        "cloud_cover": hourly.Variables(3).ValuesAsNumpy(),
    }
    hourly_dataframe = pd.DataFrame(hourly_data)

    # Clean data before plotting
    hourly_dataframe.replace([float("inf"), float("-inf")], pd.NA, inplace=True)
    hourly_dataframe.dropna(inplace=True)

    # Plotting
    import matplotlib.pyplot as plt
    import seaborn as sns

    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=hourly_dataframe, x="date", y="temperature_2m", color="#d95442")
    sns.lineplot(
        data=hourly_dataframe, x="date", y="apparent_temperature", color="#d7d8d7"
    )
    sns.lineplot(data=hourly_dataframe, x="date", y="rain", color="#50b2d4")
    ax.yaxis.grid(True, linestyle="--", linewidth=0.5, color="#888888")
    ax.xaxis.grid(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    plt.savefig(
        "/Users/janduplessis/code/janduplessis883/jan883-codebase/log/7dayforecast.png"
    )
    logger.info("Saved Image File. -  TEMP")

    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(
        data=hourly_dataframe, x="date", y="cloud_cover", color="#7c7c7c", linewidth=1
    )
    plt.fill_between(
        hourly_dataframe["date"],
        hourly_dataframe["cloud_cover"],
        color="#4088c9",
        linewidth=2,
    )
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.yaxis.grid(True, linestyle="--", linewidth=0.5, color="#888888")
    ax.xaxis.grid(False)
    plt.title(f"7-Day Forcast London - Cloud Cover - {current_time}")
    plt.savefig(
        "/Users/janduplessis/code/janduplessis883/jan883-codebase/log/7dayforcast - Cloud Cover.png"
    )
    logger.info("Saved Image File. - CLOUD")


def send_webhook(image):
    # URL of the webhook

    webhook_url = "https://hook.eu1.make.com/xgh9mvt0c2nayzi3a3rxgajmptr9jk74"

    # Open the file in binary mode and send it via the webhook
    with open(image, "rb") as file:
        # Define the payload with the image file
        files = {"file": (image, file, "image/png")}

        # Send the POST request with the file
        response = requests.post(webhook_url, files=files)

    # Check the response status
    if response.status_code == 200:
        print("Image successfully sent!")
    else:
        print(
            f"Failed to send image. Status code: {response.status_code}, Response: {response.text}"
        )


if __name__ in "__main__":
    main()
    logger.info("API called.")
    send_webhook("log/7dayforecast.png")
    logger.info("👍 Webhook 1 sent")
    send_webhook("log/7dayforcast - Cloud Cover.png")
    logger.info("👍 Webhook 2 sent")
