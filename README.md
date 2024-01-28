# OpenAI Code Cleaner README

## Overview

The `CodeCleaner` class provides a tool to clean and process code files using OpenAI's models such as GPT-4. It is designed to read code from files, interact with the OpenAI API to process the content, and write the results back to the filesystem. This tool can generate documentation such as docstrings for Python files or README documents in Markdown format.

Key features:
- Reads code files from disk.
- Sends content to the OpenAI API with customized system messages for different file types.
- Writes processed code or documentation back to specified output files.
- Filters files based on extensions and `.gitignore` entries.

## Dependencies

To run the `CodeCleaner`, the following dependencies are required:
- Python 3.x
- `openai` package: Official OpenAI Python client library.
- `tiktoken`: A library to calculate the cost of tokens.
- `prettytable`: A library to present tables in a visually appealing format.
- `default_prompts`: A module containing default system messages for OpenAI API calls (assumed to be provided as part of the codebase).

To install the required packages, you can use pip:

```bash
pip install openai tiktoken prettytable
```

Also, make sure you have an OpenAI API key and have it set as the `OPENAI_API_KEY` environment variable or pass it to the `CodeCleaner` constructor.

## Usage

First, import and instantiate the `CodeCleaner`:

```python
from pathlib import Path
from code_cleaner import CodeCleaner

# Instantiate with API key if not set in environment
api_key = "your_openai_api_key"  # Optional if OPENAI_API_KEY is set
code_cleaner = CodeCleaner(api_key=api_key)

# Specify the file paths
input_file_path = Path("path/to/code.py")
output_file_path = Path("path/to/output.md")  # or output.py for docstrings

# Use the `process_file` method to convert the file and write the output
code_cleaner.process_file(file=input_file_path, ouput_file_path=output_file_path)
```

The `process_file` method takes a file path to read from and an output file path to write the results to. It determines the type of processing based on the output file's suffix (e.g., `.py` for Python docstrings, `.md` for Markdown documents).

## Configuration

The `CodeCleaner` uses several configurations that you may want to customize:
- `system_message`: This message provides contextual information to the OpenAI model.
- `extensions`: A list of file extensions that `CodeCleaner` will consider for processing.
- The `.gitignore` file is respected to exclude files from being processed.

## Design Decisions

- Utilization of OpenAI's models: The `CodeCleaner` leverages powerful AI models to parse and generate documentation for code.
- Flexible design: Works by processing the content of files based on their extension, allowing future expansion to support more file types.
- Cost estimation: Calculates the number of tokens and their cost before making an API call, aiding in managing API usage.

## Limitations and Future Improvements

- **Known Issues**: Currently, there is limited error handling, especially for edge cases where file reading or writing may fail.
- **Performance**: Processing large files or directories may be slow as each file is handled serially; parallel processing could be implemented for better performance.
- **Future Improvements**:
  - Improved error handling and logging.
  - A command-line interface (CLI) to ease usage for users unfamiliar with Python scripts.
  - A configuration file to eliminate the need for hardcoding certain values like the model name and extensions.

## Contribution

Contributors are welcome to enhance the `CodeCleaner` by adding new features, improving the code structure, or fixing bugs. Please provide documentation for any new functionalities and make sure to follow the project's coding standards.