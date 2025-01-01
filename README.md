# Python Unit Test Generator

A Gradio-based web application that automatically generates unit tests for Python code using OpenAI's GPT-4o-mini API.

## Features

- Web-based interface for submitting Python code
- Automated unit test generation using GPT-4o-mini
- Real-time test generation and display
- Simple and intuitive user interface

## Prerequisites

Before running this application, make sure you have:

- Python 3.8 or higher

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/python-unit-test-generator.git
cd python-unit-test-generator
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
python-unit-test-generator/
├── src/
│   ├── config.py           # Configuration and environment variables
│   ├── api_client.py       # OpenAI API interaction logic
│   ├── ui.py              # Gradio UI implementation
│   ├── main.py            # Application entry point
│   └── system_prompt.txt  # System prompt for GPT-4
├── requirements.txt        # Project dependencies
└── README.md              # Project documentation
```

## Usage

1. Start the application:
```bash
python main.py
```

2. Open your web browser and navigate to the URL displayed in the terminal

3. Enter your Python code in the text input field

4. Click "Submit" to generate unit tests

### Project Components

- `config.py`: Handles environment variables and configuration settings
- `api_client.py`: Manages communication with the OpenAI API
- `ui.py`: Contains the Gradio web interface implementation
- `main.py`: Application entry point and initialization


This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for providing the GPT-4 API
- Gradio team for the web interface framework
