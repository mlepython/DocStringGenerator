# OpenAI Code Cleaner

The OpenAI Code Cleaner is a Python class that utilizes the OpenAI ChatCompletion API to process and modify Python code. It provides functionality to generate docstrings for Python code and create a Markdown document based on the code's content.

## Prerequisites

1. OpenAI API Key: An environment variable `OPENAI_API_KEY` containing the OpenAI API key is required for authentication.

2. Dependencies:
   - `openai` library
   - `tiktoken` library
   - `os` library
   - `pathlib` library

## Usage

1. **Initializing the CodeCleaner Class**:
   To initialize the `CodeCleaner` class, create an instance of the class, which sets the model name, API key, and code attributes.

   ```python
   openai_code_cleaner = CodeCleaner()
   ```

2. **Converting Python Code to Docstrings**:
   Use the `convert_to_docstrings` method to generate docstrings for the provided python code and write the modified code to a new file.

   ```python
   openai_code_cleaner.read_python_file(file_path)
   openai_code_cleaner.convert_to_docstrings(python_output_file_path="app-docstring.py")
   ```

3. **Creating a Readme Document**:
   The `convert_to_markdown` method generates a readme markdown document for the provided python code.

   ```python
   openai_code_cleaner.read_python_file(file_path="app-docstring.py")
   openai_code_cleaner.convert_to_markdown(readme_path="README.md")
   ```

## Example Use Cases

### Converting to Docstrings

```python
openai_code_cleaner.read_python_file(Path("app.py"))
openai_code_cleaner.convert_to_docstrings(python_output_file_path="app-docstring.py")
```

### Creating a Readme Document

```python
openai_code_cleaner.read_python_file(file_path="app-docstring.py")
openai_code_cleaner.convert_to_markdown(readme_path="README.md")
```

## Important Note

The code relies on the OpenAI ChatCompletion API and the `tiktoken` library for tokenization, which is utilized for obtaining the number of tokens in a text string.

## Design Decisions

The `CodeCleaner` class encapsulates the functionality to interact with the OpenAI ChatCompletion API and perform operations on Python code. It uses a prompt-based approach to generate docstrings and markdown documents, providing clear instructions and examples for the desired outcomes.

## Known Issues and Future Improvements

- The code currently assumes the availability of the OpenAI API Key as an environment variable. A more flexible approach to providing the API key could be considered.
- Improved handling of errors and exception scenarios could be added to enhance the robustness of the class.