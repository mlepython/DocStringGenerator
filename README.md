# OpenAI Code Cleaner

This code provides a `CodeCleaner` class that uses OpenAI's language model to generate docstrings for Python code and create a Markdown document for the provided code. It uses the GPT-3.5 language model to interact with the OpenAI chat completion API to perform these tasks.

## Prerequisites
- Python environment
- `openai` package
- `tiktoken` package
- OpenAI API key set as `OPENAI_API_KEY` environment variable

## Usage

1. Initialize the `CodeCleaner` class with an optional API key:
    ```python
    openai_code_cleaner = CodeCleaner(api_key="YOUR_OPENAI_API_KEY")
    ```

2. Read the content of a Python file and store it in the `CodeCleaner` instance:
    ```python
    file_path = Path("app.py")
    openai_code_cleaner.read_python_file(file_path)
    ```

3. Generate docstrings for the provided Python code and save the updated code to a new file:
    ```python
    openai_code_cleaner.create_docstrings(python_output_file_path="app-docstring.py")
    ```

4. Create a Markdown document for the provided Python code and save it to a file:
    ```python
    openai_code_cleaner.read_python_file(file_path="app-docstring.py")
    openai_code_cleaner.create_markdown_document(readme_path="README.md")
    ```

## Configuration Options
- The `CodeCleaner` class can be initialized with a custom OpenAI API key.
- Custom instructions for creating a Markdown document or generating docstrings and comments can be specified using the `markdown_document_prompt` or `docstring_generator_prompt` methods, respectively.

## Important Design Decisions
- The class uses OpenAI's GPT-3.5 language model to interact with the OpenAI chat completion API to generate docstrings and create Markdown documents.
- It determines the number of tokens in a text string using the `tiktoken` package to configure the chat completion model's `max_tokens` parameter appropriately.

## Known Issues and Future Improvements
- The current implementation may have limitations in handling complex code structures or specific programming language features.
- Future improvements may include handling different programming languages, improving code understanding, and providing more customization options for docstring generation.

By following the instructions and using the provided examples, developers can effectively utilize the `CodeCleaner` class to generate docstrings and create Markdown documents for Python code.