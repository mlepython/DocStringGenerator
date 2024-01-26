# CodeCleaner

The **CodeCleaner** class is designed to assist in modifying and documenting Python code using OpenAI's ChatCompletion for generating docstrings and creating a README markdown document.

## Functionality
The CodeCleaner class provides the following functionalities:
1. Cleaning and modifying Python code:
    - Reading the content of a Python file.
    - Generating docstrings for the provided Python code and writing the modified code to a new file.
2. Creating a README markdown document for the provided Python code.

## Dependencies
In order to run the code successfully, the following dependencies are required:
- `openai` library
- Environmental variable `OPENAI_API_KEY` set to provide the OpenAI API key

## Usage
1. **Reading Python File**:
    ```python
    openai_code_cleaner.read_python_file(file_path)
    ```
    This function reads the content of a Python file specified by `file_path`.

2. **Convert to Docstrings**:
    ```python
    openai_code_cleaner.convert_to_docstrings(python_output_file_path)
    ```
    This function generates docstrings for the provided Python code and writes the modified code to a new file specified by `python_output_file_path`.

3. **Convert to Markdown**:
    ```python
    openai_code_cleaner.convert_to_markdown(readme_path)
    ```
    This function generates a README markdown document for the provided Python code and writes it to a file specified by `readme_path`.

### Example:
```python
from CodeCleaner import CodeCleaner
from pathlib import Path

openai_code_cleaner = CodeCleaner()
file_path = Path("app.py")

# Read python file
openai_code_cleaner.read_python_file(file_path)

# Convert to docstrings only
openai_code_cleaner.convert_to_docstrings(python_output_file_path="app-docstring.py")

# Create a readme document
openai_code_cleaner.read_python_file(file_path="app-docstring.py")
openai_code_cleaner.convert_to_markdown(readme_path="README.md")
```

## Important Notes
- The OpenAI API key is required for using the `ChatCompletion` to generate responses.
- The system and user messages are used to prompt the ChatCompletion for generating docstrings and creating a readme document.

## Known Issues and Future Improvements
No known issues or future improvements have been mentioned for the codebase.