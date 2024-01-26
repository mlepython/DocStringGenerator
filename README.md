# OpenAI Code Cleaner

The provided code is a Python class `CodeCleaner` designed to utilize OpenAI's ChatCompletion model for two main functionalities:
1. Converting Python code to docstrings with the ability to add comments.
2. Generating a README markdown document based on the provided Python code.

## Dependencies
- `openai` library: This code relies on the `openai` library to interact with OpenAI's ChatCompletion model.
- `os`: Used for environment variable retrieval.
- `pathlib`: Utilized for handling file paths.
- `tiktoken`: Dependency for token encoding used by the `num_tokens_from_string` method.

## Usage
To use the `CodeCleaner` class, the user needs to instantiate an object and then call the relevant methods. Below are the main methods available:

### 1. Convert Python Code to Docstrings
1. Initialize the `CodeCleaner` object.
    ```python
    openai_code_cleaner = CodeCleaner(api_key="YOUR_OPENAI_API_KEY")
    ```
2. Read the content of a Python file using `read_python_file` method.
    ```python
    file_path = Path("app.py")
    openai_code_cleaner.read_python_file(file_path)
    ```
3. Convert the code to docstrings and write to a Python file using `convert_to_docstrings` method.
    ```python
    openai_code_cleaner.convert_to_docstrings(python_output_file_path="app-docstring.py")
    ```

### 2. Generate README Markdown Document
1. Read the content of the Python file previously modified with docstrings.
    ```python
    openai_code_cleaner.read_python_file(file_path="app-docstring.py")
    ```
2. Convert the code to a markdown document and write to a file using `convert_to_markdown` method.
    ```python
    openai_code_cleaner.convert_to_markdown(readme_path="README.md")
    ```

## Configuration Options
Users can customize the behavior of the `CodeCleaner` class by modifying the following aspects:
- OpenAI API Key: This can be provided directly as a parameter when instantiating the `CodeCleaner` object or set as an environment variable `OPENAI_API_KEY`.

## Design Choices
The code utilizes the `openai` library to interact with OpenAI's ChatCompletion model, allowing for the conversion of Python code to docstrings and the generation of a README markdown document.

## Known Limitations and Future Improvements
- Known Issues: The code currently assumes the presence of an OpenAI API key and does not handle cases when the API key is invalid or not provided.
- Future Improvements: It would be beneficial to incorporate error handling and improve the user experience by providing clearer feedback regarding any issues encountered during the code conversion process.

By following the provided examples and guidelines, developers can efficiently utilize the `CodeCleaner` class to enhance the documentation and readability of Python code, as well as automate the creation of README markdown documents.