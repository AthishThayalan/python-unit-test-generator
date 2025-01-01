import gradio as gr
from .api_client import OpenAIClient


class UnitTestGeneratorUI:
    def __init__(self):
        self.client = OpenAIClient()
        self.interface = gr.Interface(
            fn=self._generate_tests,
            inputs="text",
            outputs="text",
            title="Python Unit Test Generator",
            description="Enter a Python script to generate unit tests."
        )

    def _generate_tests(self, python_script):
        return self.client.generate_unit_tests(python_script)

    def launch(self):
        self.interface.launch()
