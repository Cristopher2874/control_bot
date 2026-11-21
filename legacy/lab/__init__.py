# Install the package (if available via pip)
# pip install needle-llm

from needle import Needle

# Load the model (local file or downloaded from Cactus)
# This assumes you have 'needle2.bin' in the current directory
model_path = "needle2.bin"

try:
    # Initialize the model
    llm = Needle(model_path)

    # Run a simple prompt
    response = llm.run("Summarize: Python is a programming language.")
    print("Model output:", response)

except FileNotFoundError:
    print(f"Model file not found at {model_path}. Please download it from Cactus Compute.")
except Exception as e:
    print("Error running Needle model:", e)
