
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
        """
        self.model_name = "gpt-3.5-turbo-1106"
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.code = ""

        if not self.api_key:
            raise ValueError("API key is required. Set the OPENAI_API_KEY environment variable.")

    def num_tokens_from_string(self, string: str, encoding_name="cl100k_base") -> int:
        """
        Returns the number of tokens in a text string.

        Parameters:
        - string (str): The input text string.
        - encoding_name (str): The name of the encoding. Default is "cl100k_base".

        Returns:
        int: The number of tokens in the text string.
        """
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def run_openai(self, messages: list) -> str:
        """
        Run OpenAI ChatCompletion and return the response message.

        Parameters:
        - messages (list): List of messages for the ChatCompletion.

        Returns:
        str: The response message from OpenAI ChatCompletion.
        """
        max_tokens = self.num_tokens_from_string(str(messages))
        response = ChatCompletion.create(
            model=self.model_name,
            messages=messages,
            max_tokens=int(max_tokens * 1.5)
        )
        return response.choices[0].message.content

    def openai_messages(self, system_message, user_message) -> list:
        """
        Create a prompt for OpenAI ChatCompletion.

        Parameters:
        - system_message (str): The system message for the prompt.
        - user_message (str): The user message for the prompt.

        Returns:
        list: The prompt list for OpenAI ChatCompletion.
        """
        prompt = [
            {'role': 'system', 'content': system_message},
            {'role': 'user', 'content': user_message}
        ]
        return prompt

    def read_python_file(self, file_path: Path) -> None:
        """
        Read the content of a Python file.

        Parameters:
        - file_path (Path): The path to the Python file.
        """
        try:
            with open(file_path, 'r') as file:
                self.code = file.read()
        except FileNotFoundError:
            print(f"Error: File not found - {file_path}")
        except Exception as e:
            print(f"Error: {e}")

    def convert_to_docstrings(self, python_output_file_path: str) -> None:
        """
        Convert the code to docstrings and write to a Python file.

        Parameters:
        - python_output_file_path (str): The output file path for the Python file with docstrings.
        """
        self.docstring_generator_prompt()
        results = self.run_openai(messages=self.openai_messages(system_message=self.system_message, user_message=self.code))
        new_code = results.split("```python", 1)[-1][::-1].split("```", 1)[-1][::-1]
        with open(python_output_file_path, 'w', encoding='utf-8') as python_file:
            python_file.write(new_code)
        print(f'Python code successfully written to: {python_output_file_path}')

    def convert_to_markdown(self, readme_path: str) -> None:
        """
        Convert the code to a markdown document and write to a file.

        Parameters:
        - readme_path (str): The output file path for the markdown document.
        """
        self.markdown_document_prompt()
        results = self.run_openai(messages=self.openai_messages(system_message=self.system_message, user_message=self.code))
        with open(readme_path, 'w', encoding='utf-8') as file:
            file.write(results)
        print(f'Readme successfully written to: {readme_path}')

    def markdown_document_prompt(self):
        self.system_message = """
        Your task is to create a README markdown document for the provided code. Here are some suggestions:
        Create a Markdown document describing the functionality, usage, and important details of the following code. Assume the target audience is developers who may need to understand, use, or contribute to the codebase.
        Instructions:

        Provide a title
        Provide a brief overview of the code's purpose and functionality.
        Include any dependencies or prerequisites needed to run the code successfully.
        Explain how to use the code, including relevant function/method calls or key parameters.
        If applicable, provide code examples or use cases to illustrate the code in action.
        Include information on any configuration options or settings that users may need to customize.
        Highlight important design decisions, algorithms, or patterns used in the code.
        Mention any known issues, limitations, or future improvements for the codebase.
        Use proper Markdown formatting for headings, code blocks, lists, and any other relevant elements.
        """

    def docstring_generator_prompt(self):
        self.system_message = """Your task will be to generate docstrings and add comments to a provided python code.
        You will also spcifiy in the define function statement for each input the desired type and the desired output type for all functions.
        Do not modify the code. It MUST stay in its current form. Insert the docstrings for each function and add some short comments if necessary.
        IF there are any parent classes that are inherited using super(), use ':meth:`MyBaseClass.some_method`' 
        For the output format, SHOW THE COMPLETE CODE with the added docstrings and comments:
        ```python
        <python code>
        ```
        Here is an example of a docstring for a function:
        def calculate_area_of_rectangle(length, width):
        '''
        Calculate the area of a rectangle.

        Parameters:
        - length (float): The length of the rectangle.
        - width (float): The width of the rectangle.

        Returns:
        float: The area of the rectangle.
        '''
        area = length * width
        return area
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
