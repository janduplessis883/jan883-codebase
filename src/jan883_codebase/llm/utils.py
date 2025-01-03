from IPython.display import HTML, Markdown, display


def to_markdown(text):
    """
    Displays the given markdown text using IPython.display.Markdown.

    Parameters:
    text (str): The markdown text to display.
    """
    display(Markdown(text))


def to_html(text):
    """
    Displays the given HTML text using IPython.display.HTML.

    Parameters:
    text (str): The markdown text to display.
    """
    display(HTML(text))
