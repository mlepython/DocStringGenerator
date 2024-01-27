
from openai import ChatCompletion
import os
from pathlib import Path
import tiktoken


class CodeCleaner():
    def __init__(self, api_key=None) -> None:
        """
        Initialize the CodeCleaner class with an optional API key.
        
        Parameters:
        - api_key (str): The API key for accessing OpenAI services.
        """
        self.model_name = "gpt-3.5-turbo-1106"
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.code = ""

        if not self.api_key:
            raise ValueError("API key is required. Set the OPENAI_API_KEY environment variable.")

    def num_tokens_from_string(self, string: str, encoding_name="cl100k_base") -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def run_openai(self, messages: list) -> str:
        """Run the OpenAI chat completion model and return the response message."""
        max_tokens = self.num_tokens_from_string(str(messages))
        response = ChatCompletion.create(
            model=self.model_name,
            messages=messages,
            max_tokens=int(max_tokens*1.5)
        )
        return response.choices[0].message.content

    def openai_messages(self, system_message: str, user_message: str) -> list:
        """Create a prompt list for OpenAI chat completion model.

        Parameters:
        - system_message (str): A system message.
        - user_message (str): A user message.

        Returns:
        list: A list containing the system and user messages.
        """
        prompt = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message}
        ]
        return prompt

    def read_python_file(self, file_path: str) -> None:
        """Read the content of a python file and store it in the CodeCleaner class instance.

        Parameters:
        - file_path (str): The path to the python file.
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

    def create_docstrings(self, python_output_file_path: str) -> None:
        """Create docstrings for the provided python code and save the updated code to a new file.

        Parameters:
        - python_output_file_path (str): The path to save the updated python file.
        """
        self.docstring_generator_prompt()

        results = self.run_openai(messages=self.openai_messages(system_message=self.system_message, user_message=self.code))

        new_code = results.split("```python",1)[-1][::-1].split("```",1)[-1][::-1]
        with open(python_output_file_path, 'w', encoding='utf-8') as python_file:
            python_file.write(new_code)
        print(f'Python code successfully written to: {python_output_file_path}')

    def create_markdown_document(self, readme_path: str) -> None:
        """Create a Markdown document for the provided python code and save it to a file.

        Parameters:
        - readme_path (str): The path to save the Markdown document.
        """
        self.markdown_document_prompt()

        results = self.run_openai(messages=self.openai_messages(system_message=self.system_message, user_message=self.code))

        with open(readme_path, 'w', encoding='utf-8') as file:
            file.write(results)
        print(f'Readme successfully written to: {readme_path}')

    def markdown_document_prompt(self, custom_instructions: str = None) -> None:
        """Set the system message prompt for creating a Markdown document.

        Parameters:
        - custom_instructions (str): Custom instructions for creating the Markdown document.
        """
        if custom_instructions:
            self.system_message = custom_instructions
        else:
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

    def docstring_generator_prompt(self, custom_instructions: str = None) -> None:
        """Set the system message prompt for generating docstrings and comments.

        Parameters:
        - custom_instructions (str): Custom instructions for generating docstrings and comments.
        """
        if custom_instructions:
            self.system_message = custom_instructions
        else:
            self.system_message = """Your task will be to generate docstrings and add comments to a provided python code.
            You will also spcifiy in the define function statement for each input the desired type and the desired output type for all functions.
            Do not modify the code. It MUST stay in its current form. Insert the docstrings for each function and add some short comments if necessary.
            Remove any uncessary comments.
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
    openai_code_cleaner.create_docstrings(python_output_file_path="app-docstring.py")

    # Example: Create a readme document
    openai_code_cleaner.read_python_file(file_path="app-docstring.py")
    openai_code_cleaner.create_markdown_document(readme_path="README.md")
