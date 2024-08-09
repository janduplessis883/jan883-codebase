import os
import sys

print("###### Model Selection Tool ##################################################")
# Hash out to use OpenAI GPT-40
openai_api_base = os.getenv("OPENAI_API_BASE")
openai_model_name = os.getenv("OPENAI_MODEL_NAME")
model = os.getenv("MODEL")
openai_api_key = os.getenv("OPENAI_API_KEY")
print("\n👍-Current MODEL-----------------")
print(f"openai api base: {openai_api_base}")
print(f"openai model name: {openai_model_name}")
print(f"openai api key: {openai_api_key}")
print(f"model: {model}")
print("-------------------------------")

proceed = input(
    "Are you happy to preceed with this model configuration? \nO -Ollama | C - Current Continue | X - exit [O|C|X] ? \n"
)
proceed = proceed.lower()
if proceed == "o":
    import os

    os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
    os.environ["OPENAI_MODEL_NAME"] = "llama3.1"  # Adjust based on available model
    os.environ["OPENAI_API_KEY"] = "ollama"
    os.environ["MODEL"] = "llama3.1"

    openai_api_base = os.getenv("OPENAI_API_BASE")
    openai_model_name = os.getenv("OPENAI_MODEL_NAME")
    model = os.getenv("MODEL")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    print("✅ Ollama Selected loading current Model Configuration for review.")
    print("\n-Current MODEL-----------------")
    print(f"openai api base: {openai_api_base}")
    print(f"openai model name: {openai_model_name}")
    print(f"openai api key: {openai_api_key}")
    print(f"model: {model}")
    print("-------------------------------\n")


elif proceed == "x":
    sys.exit(
        "❌ Exiting the script on your request: Update Model Configuration and re-rum!"
    )

print(
    "###### End of Model Selection ##################################################"
)
