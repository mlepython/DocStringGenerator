# Python Code Formatting using OpenAI

This is a Python script which uses OpenAI's GPT-4 model to generate docstrings and README markdown documents for Python scripts. The docstrings are automatically added to the Python script and a README markdown document is created for the given Python script. 

The major functionalities of this script are:
  - Reading a Python file
  - Using OpenAI's GPT-4 model to generate docstrings and add comments for the Python script
  - Saving the updated Python script with the generated docstrings and comments
  - Using OpenAI's GPT-4 model to generate a README markdown document for the Python script
  - Saving the generated README markdown document

## Installation

To run this script, you’ll need to install the following Python packages using pip:

- openai
- os
- requests
- tiktoken

## Usage

The script needs to be run with a Python version equal to 3.6 or higher. The script uses an environment variable for the OpenAI API key which needs to be set in your environment.

## Functions

The script contains the following functions which perform specific tasks:

- `num_tokens_from_string()`: Returns the number of tokens in a text string
- `run_openai()`: Runs the OpenAI's GPT-4 model and returns the generated docstring or markdown document
- `openai_messages()`: Returns the messages required by OpenAI model
- `read_python_file()`: Reads a Python file and returns its contents
- `save_to_python_file()`: Saves the generated docstring and comments to a Python file
- `save_markdown_readme()`: Saves the generated markdown document to a README file
- `markdown_document_prompt()`: Returns the system message used by OpenAI model for generating a markdown document
- `docstring_generator_prompt()`: Returns the system message used by OpenAI model for generating docstrings

When you run the script, it reads a Python file named `app.py`, uses OpenAI's GPT-4 model to generate docstrings and comments, saves the updated Python script to `app-docstring.py`, and creates a README markdown document which is then saved to `README.md`.

Happy Coding!