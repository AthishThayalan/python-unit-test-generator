from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key is None:
    print("Please set the OPENAI_API_KEY environment variable.")
else:
    print("OPENAI_API_KEY successfully loaded.")


# now to write a program that gives you unit tests for a given function.

def unit_test_generator(script):
    print(script)
