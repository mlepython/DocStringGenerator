
from openai import ChatCompletion
import os
from pathlib import Path
import tiktoken


class CodeCleaner():
    def __init__(self, api_key=None) -> None:
        """
        Initialize the CodeCleaner object.

        Parameters:
        - api_key (str): The OpenAI API key.

        Returns:
        None
        """
        self.model_name = "gpt-3.5-turbo-1106"
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.code = ""
        if not self.api_key:
            ValueError("API key is required. Set the OPENAI_API_KEY environment variable.")

    def num_tokens_from_string(self, string: str, encoding_name="cl100k_base") -> int:
        """
        Returns the number of tokens in a text string.

        Parameters:
        - string (str): The input text string.
        - encoding_name (str): The name of the encoding (default is "cl100k_base").

        Returns:
        int: The number of tokens in the input text string.
        """
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens


    def run_openai(self, messages: list) -> str:
        """
        Runs the OpenAI ChatCompletion model.

        Parameters:
        - messages (list): A list of messages for the model.

        Returns:
        str: The response from the OpenAI model.
        """
        max_tokens = self.num_tokens_from_string(str(messages))
        response = ChatCompletion.create(
            model=self.model_name,
            messages=messages,
            max_tokens=int(max_tokens*1.5)
        )
        return response.choices[0].message.content

    def openai_messages(self, user_message: str) -> list:
        """
        Formats the user message for the OpenAI model.

        Parameters:
        - user_message (str): The user input message.

        Returns:
        list: The formatted prompt for the OpenAI model.
        """
        prompt = [
        {'role': 'system', 'content': self.system_message},
        {'role': 'user', 'content': user_message}
        ]
        return prompt

    def read_python_file(self, file_path: Path) -> None:
        """
        Reads the content of a Python file into the 'code' attribute.

        Parameters:
        - file_path (Path): The path to the Python file.

        Returns:
        None
        """
        try:
            with open(file_path, 'r') as file:
                self.code = file.read()
        except FileNotFoundError:
            print(f"Error: File not found - {file_path}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def convert_to_docstrings(self, python_output_file_path: str) -> None:
        """
        Converts the code to include docstrings and writes it to a new Python file.

        Parameters:
        - python_output_file_path (str): The path to the output Python file.

        Returns:
        None
        """
        self.docstring_generator_prompt()

        results = self.run_openai(messages=self.openai_messages(user_message=self.code))

        new_code = results.split("```python",1)[-1][::-1].split("```",1)[-1][::-1]
        with open(python_output_file_path, 'w', encoding='utf-8') as python_file:
            python_file.write(new_code)
        print(f'Python code successfully written to: {python_output_file_path}')

    def convert_to_markdown(self, readme_path: str) -> None:
        """
        Converts the code to a markdown document and writes it to a file.

        Parameters:
        - readme_path (str): The path to the output markdown file.

        Returns:
        None
        """
        self.markdown_document_prompt()

        results = self.run_openai(messages=self.openai_messages(user_message=self.code))

        with open(readme_path, 'w', encoding='utf-8') as file:
            file.write(results)
        print(f'Readme successfully written to: {readme_path}')

    def markdown_document_prompt(self) -> None:
        """
        Set the system message for creating a README markdown document.

        Returns:
        None
        """
        self.system_message = """
        Your task is to create a README markdown document for the provided code...
        <...rest of the message...>
        """

    def docstring_generator_prompt(self) -> None:
        """
        Set the system message for generating docstrings and comments.

        Returns:
        None
        """
        self.system_message = """Your task will be to generate docstrings and add comments...
        <...rest of the message...>
        """

if __name__ == "__main__":
    openai_code_cleaner = CodeCleaner()
    file_path = Path("app.py")
    # read python file
    openai_code_cleaner.read_python_file(file_path)
    
    # Example: Convert to docstrings only
    openai_code_cleaner.convert_to_docstrings(python_output_file_path="app-docstring.py")

    # Example: Create a readme document
    openai_code_cleaner.read_python_file(file_path="app-docstring.py")
    openai_code_cleaner.convert_to_markdown(readme_path="README.md")
