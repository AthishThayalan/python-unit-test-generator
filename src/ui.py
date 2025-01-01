import gradio as gr
from .api_client import OpenAIClient
from .test_runner import TestRunner


class UnitTestGeneratorUI:
    def __init__(self):
        self.client = OpenAIClient()
        self.test_runner = TestRunner()
        self.interface = gr.Interface(
            fn=self._process_code,
            inputs=[
                gr.Textbox(label="Source Code", lines=10),
                gr.Checkbox(label="Run tests after generation")
            ],
            outputs=[
                gr.Textbox(label="Generated Tests", lines=10),
                gr.Textbox(label="Test Results", lines=5)
            ],
            title="Python Unit Test Generator",
            description="Enter Python code to generate and optionally run unit tests."
        )

    def _process_code(self, python_script, run_tests):
        # Generate tests
        generated_tests = self.client.generate_unit_tests(python_script)

        test_results = ""
        if run_tests:
            results = self.test_runner.run_tests(
                python_script, generated_tests)
            test_results = results["detailed_output"]

        return generated_tests, test_results

    def launch(self):
        self.interface.launch()
