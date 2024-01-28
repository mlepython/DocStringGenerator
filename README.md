# Code Cleaner README

## Overview
The `CodeCleaner` is a Python class designed to clean and modify code files using OpenAI's GPT-3.5 language model. It reads code from specified files, processes it using the GPT-3.5 model, and writes the modified code back to the files. The class also provides functionality to generate docstrings and markdown documents for Python files.

## Dependencies
- `openai` (OpenAI's GPT-3.5 API)
- `tiktoken` (for tokenization)
- `prettytable` (for tabular display)

## Usage
1. Instantiate the `CodeCleaner` class, optionally passing the OpenAI API key as a parameter.
    ```python
    openai_code_cleaner = CodeCleaner(api_key="YOUR_OPENAI_API_KEY")
    ```

2. Call the `files_for_modifiction` method to get information about the files in a specified directory.
    ```python
    file_path = Path("/path/to/your/directory")
    openai_code_cleaner.files_for_modifiction(file_path)
    ```
    This method prints a table with information such as file names, token counts, and cost estimates.

3. Process a specific file using the `process_file` method.
    ```python
    file_path = Path("/path/to/your/file.py")
    output_file_path = Path("/path/to/your/output/file.py")

    openai_code_cleaner.process_file(file=file_path, ouput_file_path=output_file_path)
    ```
    This method reads the file, processes it using OpenAI, and writes the modified output to the specified output file. It also handles different file types such as Python and Markdown documents.

## Configuration Options
- The `model_name` attribute in the `__init__` method can be modified to use a different OpenAI model, such as "gpt-4-1106-preview".
- The `num_tokens_from_messages` method has the option to change the encoding name for tokenization.

## Important Design Decisions
- The class uses OpenAI's GPT-3.5 language model for code modification and generation.
- It provides a flexible way to process different file types and handle custom instructions.

## Known Issues and Future Improvements
- The code currently lacks complete implementation for the single file input scenario in the `files_for_modifiction` method, which can be improved upon.
- Future improvements may include enhancing user interaction and providing more customization options for code modification.