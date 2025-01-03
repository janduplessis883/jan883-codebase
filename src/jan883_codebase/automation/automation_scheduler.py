import schedule
import subprocess
import sys
import time
from colorama import Fore, Style, init
import pendulum
from tqdm import tqdm

init()  # Initializes Colorama

now = pendulum.now()
delay_hours = 4
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
    print("Running AI MedReview")
    run_script(
        "/Users/janduplessis/code/janduplessis883/ai-medreview/ai_medreview/data.py"
    )

    print("Running iCloud Email")
    run_script(
        "/Users/janduplessis/code/janduplessis883/jan883-codebase/automation/icloud_email.py"
    )

    for _ in tqdm(range(delay_seconds), desc="Waiting...", colour="#d7bd5b"):
        time.sleep(1)
