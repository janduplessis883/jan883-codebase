import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import os
from tqdm import tqdm
from collections import Counter
from datetime import datetime
from simhash import Simhash


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
        print(f"Scraping URL: {url}", end='\r', flush=True)
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract text from paragraphs, headers (h1, h2, h3)
            text_elements = []
            text_elements.extend([h.get_text() for h in soup.find_all(["h1", "h2", "h3"])] )
            text_elements.extend([p.get_text() for p in soup.find_all("p")])

            text = " ".join(text_elements)
            print(f"Finished scraping URL: {url}", end='\r', flush=True)
            return text
        except requests.RequestException as e:
            print(f"Request failed for URL {url}: {e}", end='\r', flush=True)
            return ""

    def get_links_from_url(url):
        """
        Fetches all valid links from the given URL.

        Args:
        url (str): The URL to scrape links from.

        Returns:
        list: A list of valid URLs found on the page.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            links = []
            for a_tag in soup.find_all("a", href=True):
                link = urljoin(url, a_tag['href'])
                if scrape_external or urlparse(link).netloc == urlparse(start_url).netloc:
                    links.append(link)
            return links
        except requests.RequestException as e:
            print(f"Failed to retrieve links from URL {url}: {e}", end='\r', flush=True)
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

    print(f"\n🇾️ Starting scraping for the initial URL: {start_url} with depth {depth}")

    for current_depth in range(depth):
        print(f"\n🔗 Depth {current_depth + 1}/{depth} - URLs to scrape: {len(urls_to_scrape)}")
        new_urls = []  # Store new URLs to scrape at the next depth level

        for idx, url in enumerate(urls_to_scrape):
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

                # Update the output to show progress
                print(f"   Scraped {idx + 1}/{len(urls_to_scrape)} URLs at depth {current_depth + 1}")

        # Update the list of URLs to scrape with the new URLs for the next depth level
        print(f"\n💥 URLs found for next depth ({current_depth + 2}): {len(new_urls)}")
        urls_to_scrape = new_urls

    print(f"\n📜 Saved combined text content to '{file_name}'")
    print(f"\n📁 You can find the output file at: {file_name}")

    # Read the combined text content from the file and return it
    with open(file_name, 'r', encoding='utf-8') as file:
        combined_text = file.read()

    return combined_text

# Example usage in Jupyter Notebook
# start_url = "https://docs.crewai.com"  # Replace with the URL you want to scrape
# depth = 2  # Specify how many levels deep you want to scrape
# scrape_external = False  # Set to True to scrape external links, False to only scrape internal links
# combined_text = scrape_website(start_url, depth, scrape_external)


def remove_repeated_blocks_using_simhash(blocks):
    """
    Removes repeated blocks of text based on Simhash, keeping only one instance of repeated blocks.

    Args:
    blocks (list): List of text blocks to be deduplicated.

    Returns:
    list: Cleaned list of blocks with duplicates removed.
    """
    seen_hashes = set()
    cleaned_blocks = []

    for block in blocks:
        block_hash = Simhash(block).value
        print(block_hash)
        if block_hash not in seen_hashes:
            cleaned_blocks.append(block)
            seen_hashes.add(block_hash)

    return cleaned_blocks


def remove_repeated_blocks_from_file(file_path, output_path, block_type="sentence"):
    """
    Removes repeated blocks of text (either sentences or paragraphs) from a file, but keeps one instance
    of repeated blocks using Simhash.

    Args:
    file_path (str): Path to the input text file.
    output_path (str): Path to save the cleaned text file.
    block_type (str): The type of block to consider for repetition ('sentence' or 'paragraph').
    """

    # Get the file size before processing
    initial_file_size = os.path.getsize(file_path)
    print(f"📄 Initial file size: {initial_file_size / 1024:.2f} KB")

    # Read the content of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Split content into sentences or paragraphs based on the block type
    if block_type == "sentence":
        blocks = re.split(r'(?<=[.!?])\s+', content)  # Split by sentences
    elif block_type == "paragraph":
        blocks = content.split('\n\n')  # Split by paragraphs
    else:
        raise ValueError("Invalid block_type. Choose 'sentence' or 'paragraph'.")

    # Initialize tqdm progress bar
    with tqdm(total=len(blocks), desc="Removing duplicates") as progress_bar:
        # Remove repeated blocks using Simhash
        cleaned_blocks = []
        seen_hashes = set()
        for block in blocks:
            block_hash = Simhash(block).value
            if block_hash not in seen_hashes:
                cleaned_blocks.append(block)
                seen_hashes.add(block_hash)
            progress_bar.update(1)

    # Join the cleaned blocks back into text
    cleaned_text = '\n\n'.join(cleaned_blocks) if block_type == "paragraph" else ' '.join(cleaned_blocks)

    # Save the cleaned content to a new file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)

    # Get the file size after processing
    final_file_size = os.path.getsize(output_path)
    print(f"📄 Final file size: {final_file_size / 1024:.2f} KB")

    print(f"✅ Cleaned text saved to: {output_path}")


def remove_repeated_blocks(text, output_dir=None, block_type="sentence"):
    """
    Removes repeated blocks of text (either sentences or paragraphs) from the input text, but keeps one instance
    of repeated blocks using Simhash. The cleaned text is also saved to a file with a timestamped filename.

    Args:
    text (str): The input text content.
    output_dir (str): Directory to save the cleaned text file. If None, the default directory will be used.
    block_type (str): The type of block to consider for repetition ('sentence' or 'paragraph').

    Returns:
    str: Cleaned text with repeated blocks removed.
    """

    # Split content into sentences or paragraphs based on the block type
    if block_type == "sentence":
        blocks = re.split(r'(?<=[.!?])\s+', text)  # Split by sentences
    elif block_type == "paragraph":
        blocks = text.split('\n\n')  # Split by paragraphs
    else:
        raise ValueError("Invalid block_type. Choose 'sentence' or 'paragraph'.")

    # Remove repeated blocks using Simhash
    cleaned_blocks = remove_repeated_blocks_using_simhash(blocks)

    # Join the cleaned blocks back into text
    cleaned_text = '\n\n'.join(cleaned_blocks) if block_type == "paragraph" else ' '.join(cleaned_blocks)

    # Get the current datetime and format it
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Set the default output directory if not provided
    if output_dir is None:
        output_dir = os.path.expanduser('')

    # Ensure the directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Create the output filename
    output_filename = f"cleaned_text_{current_datetime}.txt"
    output_path = os.path.join(output_dir, output_filename)

    # Save the cleaned text to the output file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)

    print(f"✅ Cleaned text saved to: {output_path}")

    return cleaned_text
