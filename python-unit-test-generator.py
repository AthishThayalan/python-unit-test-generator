from dotenv import load_dotenv
from openai import OpenAI
import os
import gradio as gr

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

if openai_api_key is None:
    print("Please set the OPENAI_API_KEY environment variable.")
else:
    print("OPENAI_API_KEY successfully loaded.")

# Load system_prompt from external file
with open('system_prompt.txt', 'r') as file:
    system_prompt = file.read()


def unit_test_generator(python_script):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": python_script}
        ]
    )
    return completion.choices[0].message.content


def gradio_interface(python_script):
    return unit_test_generator(python_script)


iface = gr.Interface(
    fn=gradio_interface,
    inputs="text",
    outputs="text",
    title="Python Unit Test Generator",
    description="Enter a Python script to generate unit tests."
)

if __name__ == "__main__":
    iface.launch()
