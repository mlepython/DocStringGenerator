
from openai import OpenAI
import os
from pathlib import Path
import tiktoken
from prettytable import PrettyTable

table = PrettyTable()
client = OpenAI()

class CodeCleaner():
    def __init__(self, api_key=None) -> None:
        '''
        Initialize the CodeCleaner class.

        Parameters:
        - api_key (str, optional): The API key for OpenAI. Defaults to None.
        '''
        self.model_name = "gpt-3.5-turbo-1106"
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.file_contents = ""
        self.js = ""
        self.html = ""
        self.md = ""
        self.css = ""

        if not self.api_key:
            raise ValueError("API key is required. Set the OPENAI_API_KEY environment variable.")

    def num_tokens_from_messages(self, string: str, encoding_name="cl100k_base") -> int:
        '''
        Returns the number of tokens in a text string.

        Parameters:
        - string (str): The input text string.
        - encoding_name (str, optional): The name of the encoding. Defaults to "cl100k_base".

        Returns:
        int: The number of tokens in the text string.
        '''
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        if "gpt-4" in self.model_name:
            cost = num_tokens/1000*0.01
        else:
            cost = num_tokens/1000*0.001
        return num_tokens, cost

    def run_openai(self, messages: list) -> str:
        '''
        Calls the OpenAI API to generate completion messages.

        Parameters:
        - messages (list): List of messages for OpenAI API.

        Returns:
        str: The generated completion message from OpenAI.
        '''
        max_tokens, _ = self.num_tokens_from_messages(str(messages))
        response = client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            max_tokens=int(max_tokens*1.5)
        )
        return response.choices[0].message.content

    def openai_messages(self, system_message, user_message):
        '''
        Prepare the messages for communication with OpenAI.

        Parameters:
        - system_message (str): The system message.
        - user_message (str): The user message.

        Returns:
        list: List of messages for OpenAI API.
        '''
        prompt = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message}
        ]
        return prompt

    def read_file(self, file_path):
        '''
        Read the contents of a file.

        Parameters:
        - file_path (str): The path to the file to be read.

        Returns:
        str: The contents of the file.
        '''
        try:
            with open(file_path, 'r') as file:
                self.file_contents = file.read()
        except FileNotFoundError:
            print(f"Error: File not found - {file_path}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
        
    def write_file(self, file_path, content):
        '''
        Write content to a file.

        Parameters:
        - file_path (str): The path to the file to be written.
        - content (str): The content to be written to the file.
        '''
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

    def create_docstrings(self, python_output_file_path):
        '''
        Generate docstrings for a Python code file.

        Parameters:
        - python_output_file_path (str): The path to the Python output file with generated docstrings.
        '''
        self.docstring_generator_prompt()

        results = self.run_openai(messages=self.openai_messages(system_message=self.system_message, user_message=self.file_contents))

        new_code = results.split("```python",1)[-1][::-1].split("```",1)[-1][::-1]
        self.write_file(file_path=python_output_file_path, content=new_code)
        print(f'Python code successfully written to: {python_output_file_path}')

    def create_markdown_document(self, readme_path):
        '''
        Generate a readme markdown document.

        Parameters:
        - readme_path (str): The path to the readme markdown document.
        '''
        self.markdown_document_prompt()

        results = self.run_openai(messages=self.openai_messages(system_message=self.system_message, user_message=self.file_contents))
        self.write_file(file_path=readme_path, content=results)

        print(f'Readme successfully written to: {readme_path}')

    def markdown_document_prompt(self, custom_instructions=None):
        '''
        Generate a prompt for creating a readme markdown document.
        '''
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

    def docstring_generator_prompt(self, custom_instructions=None):
        '''
        Generate a prompt for generating docstrings and adding comments.
        '''
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

    def generic_prompt(self, custom_instructions=None):
        pass

    def get_files(self, directory_path, extensions=[".py", ".html", ".js", ".css", ".md"]):
        '''
        Get the list of files with specified extensions within a directory.

        Parameters:
        - directory_path (str): The path to the directory.
        - extensions (list, optional): List of file extensions to search for. Defaults to [".py", ".html", ".js", ".css", ".md"].

        Returns:
        list: List of files with specified extensions within the directory.
        '''
        gitignore_contents, gitignore_contents_path = read_contents_from_gitignore(directory_path)
        files = []
        for extension in extensions:
            files.extend(directory_path.glob(f'*{extension}'))
        subdirectories = [subdir for subdir in directory_path.iterdir() if subdir.is_dir()]
        for subdir in subdirectories:
            if str(subdir.name) not in gitignore_contents:
                for extension in extensions:
                    for file in subdir.glob(f'*{extension}'):
                        if all(str(file) not in str(gitignore) for gitignore in gitignore_contents_path):
                            files.append(file)

        return files

    def files_for_modifiction(self, file_dir):
        '''
        Get the list of files in a directory for modification.

        Parameters:
        - file_dir (str): The directory path or file.

        Returns:
        list: List of files in the directory for modification.
        '''
        if file_dir.is_dir():
            table.field_names = ["index", "File Name", "Token Count", "Cost Estimate"]
            files = self.get_files(directory_path=file_dir)
            print("Files in directory", file_dir)
            for index, file in enumerate(files):
                if file.suffix == ".py":
                    self.docstring_generator_prompt()
                    self.read_file(file_path=file)
                    tokens, cost = self.num_tokens_from_messages(self.system_message+self.file_contents)
                elif file.suffix == ".md":
                    self.markdown_document_prompt()
                    self.read_file(file_path=file)
                    tokens, cost = self.num_tokens_from_messages(self.system_message+self.file_contents)
                else:
                    tokens, cost = 0, 0
                table.add_row([index, file.name, tokens, round(cost,4)])
            print(table)
        else:
            file = file_dir
        pass

def read_contents_from_gitignore(directory):
    '''
    Read the contents from the .gitignore file.

    Parameters:
    - directory (str): The directory containing the .gitignore file.

    Returns:
    list: List of contents from the .gitignore file.
    list: List of absolute paths to the contents from the .gitignore file.
    '''
    try:
        with open(directory/".gitignore", 'r') as file:
            contents = file.readlines()
            contents_abs_path = []
            for index, line in enumerate(contents):
                contents[index] = line.strip()
                contents_abs_path.append(directory/contents[index])
        return contents, contents_abs_path
    except FileNotFoundError:
        print(f"The file {directory} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    openai_code_cleaner = CodeCleaner()
    file_path = Path(r"C:\Users\mike_\OneDrive\Documents\OpenAI and Python\DocStringGenerator\app.py")
    openai_code_cleaner.files_for_modifiction(file_path.parent)
    openai_code_cleaner.read_file(file_path)
    
    # Example: Convert to docstrings only
    openai_code_cleaner.create_docstrings(python_output_file_path=file_path.parent/"app-docstring.py")
