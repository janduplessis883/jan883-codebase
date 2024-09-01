import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import os

def scrape_website(start_url, depth, scrape_external=False):
    """
    Scrapes the text content from the start URL and each link up to the specified depth,
    then saves the combined text content to a file named after the start URL in a specified directory.

    Args:
    start_url (str): The initial URL to start scraping.
    depth (int): The depth level to scrape links. A depth of 1 means scrape the start_url and its direct links.
    scrape_external (bool): Whether to scrape external links (default is False).

    Returns:
    str: The combined text content from the start URL and each link up to the specified depth.
    """

    def get_text_from_url(url):
        """
        Fetches and returns the combined text content from a given URL.

        Args:
        url (str): The URL to scrape.

        Returns:
        str: The combined text content from the URL.
        """
        print(f"Scraping URL: {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            text = " ".join([p.get_text() for p in soup.find_all("p")])
            print(f"Finished scraping URL: {url}")
            return text
        except requests.RequestException as e:
            print(f"Request failed for URL {url}: {e}")
            return ""

    def get_links_from_url(url):
        """
        Fetches and returns all links from a given URL, filtered by whether they are internal or external.

        Args:
        url (str): The URL to scrape for links.

        Returns:
        list: A list of absolute URLs found on the given page.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("a", href=True)
            absolute_links = [urljoin(url, link["href"]) for link in links]

            # Filter links based on whether they are internal or external
            if not scrape_external:
                # Get the base domain of the start_url for comparison
                base_domain = urlparse(start_url).netloc
                absolute_links = [link for link in absolute_links if urlparse(link).netloc == base_domain]

            return absolute_links
        except requests.RequestException as e:
            print(f"Request failed for URL {url}: {e}")
            return []

    # Sanitize the start_url to create a safe filename
    sanitized_url = re.sub(r'[^a-zA-Z0-9]', '_', start_url)
    # Define the directory where the file will be saved
    output_dir = os.path.expanduser('~/code/janduplessis883/jan883-codebase/webscraping/')
    # Ensure the directory exists
    os.makedirs(output_dir, exist_ok=True)
    # Create the full path for the output file
    file_name = os.path.join(output_dir, f'website_content_{sanitized_url}.txt')

    # Initialize the set of URLs to scrape, starting with the initial URL
    urls_to_scrape = [start_url]
    scraped_urls = set()  # To keep track of already scraped URLs

    print(f"\n🅾️ Starting scraping for the initial URL: {start_url} with depth {depth}")

    for current_depth in range(depth):
        print(f"\n➡️ Scraping at depth {current_depth + 1}")
        new_urls = []  # Store new URLs to scrape at the next depth level

        for url in urls_to_scrape:
            if url not in scraped_urls:
                # Scrape the current URL's content
                page_text = get_text_from_url(url)
                # Append the scraped text to the file
                with open(file_name, 'a', encoding='utf-8') as file:
                    file.write(page_text + "\n")

                # Get all links from the current URL and add them to new_urls
                new_urls.extend(get_links_from_url(url))
                # Mark this URL as scraped
                scraped_urls.add(url)


        # Update the list of URLs to scrape with the new URLs for the next depth level
        print(f"\n💥 URL's to scrape: {len(new_urls)}")
        urls_to_scrape = new_urls

    print(f"Saved combined text content to '{file_name}'")
    print(f"You can find the output file at: {file_name}")

    return file_name

# Example usage in Jupyter Notebook
# start_url = "https://docs.crewai.com"  # Replace with the URL you want to scrape
# depth = 2  # Specify how many levels deep you want to scrape
# scrape_external = False  # Set to True to scrape external links, False to only scrape internal links
# combined_text = scrape_website(start_url, depth, scrape_external)
