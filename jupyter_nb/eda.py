from IPython.display import HTML, Markdown, display


## Print Welcome Message
def display_message():
    message = "<b>😃 helper883</b> loaded! - run <code>import helper883</code> <code>list_functions(helper883)</code> for a list of functions."
    html_message = f"""
        <span style="color: #345a69; font-size: 12px;">{message}</span>
    """
    display(HTML(html_message))

# Call the function to display the message
display_message()
