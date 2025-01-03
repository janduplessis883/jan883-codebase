import os
import webbrowser


def get_pwd():
    """
    Returns the present working directory.

    Returns:
    str: The present working directory.
    """
    return os.getcwd()


def open_links_from_file(file_path):
    """
    Opens each URL listed in the specified file in the default web browser.

    Args:
    file_path (str): The path to the file containing URLs.
    """
    with open(file_path) as file:
        links = file.readlines()
        for link in links:
            # Strip any newline characters or extra spaces
            clean_link = link.strip()
            webbrowser.open(clean_link)


# Example usage:
# open_links_from_file('../data/links.txt')

if __name__ == "__main__":
    open_links_from_file("streamlit_apps_links.txt")
