# Code Cleaner

The `CodeCleaner` class is a tool for generating docstrings for Python code and creating a README markdown document using the OpenAI API. It also provides functionality to read and modify Python code files.

## Functionality

The `CodeCleaner` class offers the following functionality:
- Initializing the class with an API key for the OpenAI API
- Reading Python files and storing their contents
- Generating docstrings for the provided Python code and writing the modified code to a new file
- Creating a README markdown document for the provided code and writing it to a file
- Retrieving a list of files with specified extensions in a directory
- Reading the contents of the .gitignore file in a specified directory

## Prerequisites

In order to use the `CodeCleaner` class, you need:
- Python installed on your system
- OpenAI API key
- Required dependencies: `openai`, `os`, `pathlib`, `tiktoken`

## Usage

### Initialization
```python
openai_code_cleaner = CodeCleaner(api_key="your_openai_api_key")
```

### Reading Python File
```python
file_path = Path("/path/to/python/file.py")  # Specify the path to the Python file
openai_code_cleaner.read_python_file(file_path)
```

### Generate Docstrings
```python
# Provide the path to write the modified Python code with added docstrings
openai_code_cleaner.create_docstrings(python_output_file_path="/path/to/output/file.py")
```

### Create README Document
```python
# Provide the path to write the README markdown document
openai_code_cleaner.create_markdown_document(readme_path="/path/to/readme.md")
```

## Known Limitations and Future Improvements

- The code is tightly coupled with the OpenAI API, so changes to the API may require updates to the code.
- Improved error handling and validation can be added to enhance the robustness of the class.
- Additional customization options for generating docstrings and README documents may be beneficial.

---
The `CodeCleaner` class provides a convenient way to automate the generation of docstrings and README documents using the OpenAI API, offering potential time-saving benefits in code documentation and project management.