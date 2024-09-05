import streamlit as st
from automation import *
from loguru import logger
import sys
import time

st.title("🧔🏻 jan883-codebase App")


class StreamlitLogger:
    def __init__(self):
        self.logs = []
        self.log_placeholder = st.empty()  # Create a placeholder for log messages

    def log_sink(self, message):
        self.logs.append(message)
        # Update the placeholder with all log entries
        self.log_placeholder.text("\n".join(self.logs))

def configure_streamlit_logger():
    """
    Configure the loguru logger to use the custom Streamlit logger.
    """
    # Clear existing loggers
    logger.remove()

    # Initialize StreamlitLogger
    streamlit_logger = StreamlitLogger()

    # Add the custom Streamlit sink to loguru
    logger.add(streamlit_logger.log_sink, format="{time} - {message}", level="INFO")

def main():
    # Configure the Streamlit logger
    configure_streamlit_logger()
    st.write("Logs are streaming below:")


    # Example usage
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")



    # Simulate a long-running process
    for i in range(5):
        logger.info(f"Processing step {i + 1}")
        time.sleep(1)  # Simulate time delay between log entries

if __name__ == "__main__":
    main()
    logger.info("Main function completed")
