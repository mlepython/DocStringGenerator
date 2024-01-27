# CodeCleaner

The `CodeCleaner` class provides functionality to read, modify, and create documentation for Python code using OpenAI's ChatCompletion API.

## Purpose and Functionality
The `CodeCleaner` class is designed to:
- Read the content of a Python file and store it within the class object.
- Generate docstrings for the provided Python code and write the updated code to a new file.
- Create a README markdown document for the provided code.

## Dependencies and Prerequisites
To run the code successfully, the following dependencies are required:
- `openai` package
- `tiktoken` package
- OpenAI API key set in the environment variable OPENAI_API_KEY

## Usage
1. Initialize the `CodeCleaner` class by providing the OpenAI API key or ensuring it is available in the environment variable OPENAI_API_KEY
    ```python
    openai_code_cleaner = CodeCleaner(api_key="your_openai_api_key")
    ```

2. Read the content of a Python file and store it within the class object
    ```python
    file_path = Path("path_to_python_file")
    openai_code_cleaner.read_python_file(file_path)
    ```

3. Generate docstrings for the provided Python code and write the updated code to a new file
    ```python
    python_output_file_path = Path("output_file_path")
    openai_code_cleaner.create_docstrings(python_output_file_path)
    ```

4. Create a README markdown document for the provided code
    ```python
    readme_path = Path("readme_file_path")
    openai_code_cleaner.create_markdown_document(readme_path)
    ```

## Important Details
- The `CodeCleaner` class utilizes the OpenAI ChatCompletion API to generate responses based on input messages.
- Custom instructions can be provided for generating README markdown documents or docstrings and comments for Python code.
- The class provides functions to retrieve files with specific extensions within a directory and read the contents of a .gitignore file.

## Known Issues and Future Improvements
- The code currently does not handle exceptions related to the OpenAI API responses.
- Future improvements could include enhancing error handling and adding more customization options for generating documentation.

By using the `CodeCleaner` class, developers can efficiently generate docstrings, comments, and README markdown documents for their Python code.