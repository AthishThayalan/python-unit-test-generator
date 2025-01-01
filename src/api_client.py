from openai import OpenAI
from .config import OPENAI_API_KEY


class OpenAIClient:
    def __init__(self):
        self.client = OpenAI()
        self.system_prompt = (
            "You are a Python code generator specialized in writing unit tests. "
            "For a given Python function, you will perform the following tasks: "
            "1. Analyze the function's purpose, arguments, return type, and potential edge cases. "
            "2. Generate a set of meaningful and concise unit tests to thoroughly test the function's behavior. "
            "3. Use Python's 'unittest' framework to structure the tests. "
            "4. Ensure the tests cover normal, edge, invalid, and boundary cases without redundancy. "
            "5. Include clear, non-redundant test cases with descriptive method names. "
            "6. If a function is not entered in its correct format, prompt the user to re-submit the function. "
            "Output only the code for the test cases, without any additional explanation."
        )

    def generate_unit_tests(self, python_script):
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": python_script}
            ]
        )
        return completion.choices[0].message.content
