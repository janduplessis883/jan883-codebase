import requests
from bs4 import BeautifulSoup

def scrape_website(url_list, display_text=False):
    """
    Scrape a list of websites and return their cleaned text content.

    Args:
        url_list (list): A list of URLs to scrape.
        display_text (bool, optional): Whether to print the scraped text. Defaults to False.

    Returns:
        list: A list of cleaned text from each website.

    Raises:
        requests.exceptions.RequestException: If an error occurs while requesting a webpage.
        Exception: If any other error occurs while processing a webpage.
    """
    cleaned_texts = []

    for url in url_list:
        try:
            # Send a GET request to the webpage
            response = requests.get(url)
            response.raise_for_status()  # Check for request errors

            # Parse the content of the response with BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract all text from the webpage
            page_text = soup.get_text()
            text_len = len(page_text.split())
            # Remove all whitespace
            cleaned_text = " ".join(page_text.split())
            cleaned_texts.append(cleaned_text)

            if display_text and cleaned_text:
                print(f"✅ ➔ word count: {text_len}")
                print(cleaned_text)

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while requesting {url}: {e}")
        except Exception as e:
            print(f"An error occurred while processing {url}: {e}")

    return cleaned_texts
