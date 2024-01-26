# Code Cleaner

The `CodeCleaner` class provides functionality to clean and enhance Python code. It uses the OpenAI ChatCompletion model to generate docstrings for Python code and to create README markdown documents. The code makes use of the OpenAI API and the `tiktoken` library for tokenization.

## Dependencies
- OpenAI API key
- `openai` library
- `tiktoken` library
- Python 3.6 or higher

## How to Use
1. Initialize the `CodeCleaner` object with the OpenAI API key.
```python
openai_code_cleaner = CodeCleaner(api_key="YOUR_OPENAI_API_KEY")
```

2. Read a Python file into the `code` attribute.
```python
file_path = Path("app.py")
openai_code_cleaner.read_python_file(file_path)
```

3. Convert the code to include docstrings and write it to a new Python file.
```python
openai_code_cleaner.convert_to_docstrings(python_output_file_path="app-docstring.py")
```

4. Create a README markdown document from the code.
```python
openai_code_cleaner.read_python_file(file_path="app-docstring.py")
openai_code_cleaner.convert_to_markdown(readme_path="README.md")
```

## Configuration Options
- The encoding name can be customized in the `num_tokens_from_string` method.
- The system message for creating readme and docstring generation can be modified in the respective prompt methods.

## Important Design Decisions
- The code uses the OpenAI ChatCompletion model to enhance and clean Python code by generating docstrings and creating README markdown documents.
- It leverages the `tiktoken` library for tokenization and the `pathlib` library for file path handling.

## Known Limitations
- The code assumes that the input Python file and the output file paths are valid.
- It may not handle complex Python code structures or formatting.

## Future Improvements
- Error handling and robust file handling for different edge cases could be improved.
- Additional options for customization, such as specifying the ChatCompletion model, could be added.

By following the provided steps, you can use the `CodeCleaner` to enhance and clean Python code while creating corresponding documentation effortlessly.