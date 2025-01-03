import subprocess
import sys
import time
from colorama import Fore, Style, init
import pendulum
from tqdm import tqdm

init()  # Initializes Colorama

now = pendulum.now()
delay_hours = 24
delay_seconds = delay_hours * 60 * 60


def run_script(script_path):
    try:
        process = subprocess.Popen(
            ["python3", script_path], stdout=sys.stdout, stderr=sys.stderr, text=True
        )
        process.communicate()
    except subprocess.CalledProcessError as e:
        print(f"Command returned non-zero exit status: {e.returncode}")


for i in range(0, 100, 1):
    print("Running News to Telegram")
    run_script(
        "/Users/janduplessis/code/janduplessis883/jan883-codebase/automation/news_automation.py"
    )

    print("Running Weather Forecast")
    run_script(
        "/Users/janduplessis/code/janduplessis883/jan883-codebase/automation/weather_forcast.py"
    )

    for _ in tqdm(range(delay_seconds), desc="Waiting...", colour="#b03153"):
        time.sleep(1)
