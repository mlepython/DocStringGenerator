# OpenAI Code Cleaner

The provided code is a Python script for cleaning and processing code files using the OpenAI GPT-3.5-Turbo and GPT-4 language models. It leverages the OpenAI API to generate docstrings for Python files and create markdown documentation. The script also estimates the cost of processing based on the number of tokens in the input text.

## Functionality Overview

The code provides a `CodeCleaner` class with methods for reading, processing, and writing code files using the OpenAI GPT models. It supports generating Python docstrings and creating markdown documentation for given input files. It also includes methods for extracting file information such as token count and cost estimates.

## Dependencies and Prerequisites

- `openai`: The `OpenAI` library is required to interact with the OpenAI GPT models.
- `Path` from `pathlib`: Used for working with file paths.
- `tiktoken`: Used to get encoding details for tokenization.
- `PrettyTable`: Used for creating tabular output for displaying file details.

## Usage and Key Method Calls

1. **Instantiating the `CodeCleaner` Class**

```python
openai_code_cleaner = CodeCleaner()
```

2. **Processing Files in a Directory**

The `files_for_modification` method retrieves files from a directory, generates system messages based on file types, and displays a table of token count and cost estimates.

```python
file_dir = Path("path_to_directory")
openai_code_cleaner.files_for_modification(file_dir)
```

3. **Processing a Single File**

The `process_file` method reads a file, calls the OpenAI model, and writes the processed content to a specified output file.

```python
file_path = Path("path_to_input_file")
output_file_path = Path("path_to_output_file")
openai_code_cleaner.process_file(file_path, output_file_path)
```

## Design Decisions and Considerations

- The code uses the `tiktoken` library to tokenize input text and estimate the cost based on the number of tokens. It also handles requirements for different model variations such as GPT-3.5-Turbo and GPT-4.
- A `PrettyTable` is utilized to present file details in a tabular format, improving the user experience.

## Future Improvements and Limitations

### Future Improvements
- Additional error handling and user input validation can be incorporated to enhance robustness.
- Supporting more file formats for processing, such as JSON, YAML, and others.

### Limitations
- The code currently has limited support for custom instructions during the OpenAI model call, which could limit flexibility for certain use cases. This could be improved by allowing users to provide custom instructions for processing.