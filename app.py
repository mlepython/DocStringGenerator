from openai import ChatCompletion
import os
from pathlib import Path
import tiktoken


# MODEL_NAME = "gpt-4-0613"
MODEL_NAME = "gpt-3.5-turbo-1106"
MAX_TOKENS = 1500
api_key = os.getenv("OPENAI_API_KEY")

def num_tokens_from_string(string: str, encoding_name="cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def run_openai(messages: list):
        max_tokens = num_tokens_from_string(str(messages))
        print(max_tokens)
        response = ChatCompletion.create(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=int(max_tokens*1.5)
        )
        return response.choices[0].message.content

def openai_messages(system_message="", user_message=""):
     prompt = [
    {'role': 'system', 'content': system_message},
    {'role': 'user', 'content': user_message}
    ]
     return prompt

def read_python_file(file_path):
    try:
        with open(file_path, 'r') as file:
            file_contents = file.read()
        return file_contents
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def save_to_python_file(code, python_file_path):
    system_message = docstring_generator_prompt()
    user_message = f"""{code}"""
    results = run_openai(messages=openai_messages(system_message, user_message))

    code = results.split("```python",1)[-1][::-1].split("```",1)[-1][::-1]
    with open(python_file_path, 'w', encoding='utf-8') as python_file:
        python_file.write(code)
    print(results)
    print(f'Python code successfully written to: {python_file_path}')

def save_markdown_readme(code, readme_path):
    system_message = markdown_document_prompt()
    user_message = f"""{code}"""
    results = run_openai(messages=openai_messages(system_message, user_message))

    with open(readme_path, 'w', encoding='utf-8') as file:
        file.write(results)
    print(f'Readme successfully written to: {readme_path}')

def markdown_document_prompt():
    system_message = """
    Your task is to create a README markdown document for the provided code. Here are some suggestions:
    Create a Markdown document describing the functionality, usage, and important details of the following code. Assume the target audience is developers who may need to understand, use, or contribute to the codebase.
    Instructions:

    Provide a brief overview of the code's purpose and functionality.
    Include any dependencies or prerequisites needed to run the code successfully.
    Explain how to use the code, including relevant function/method calls or key parameters.
    If applicable, provide code examples or use cases to illustrate the code in action.
    Include information on any configuration options or settings that users may need to customize.
    Highlight important design decisions, algorithms, or patterns used in the code.
    Mention any known issues, limitations, or future improvements for the codebase.
    Use proper Markdown formatting for headings, code blocks, lists, and any other relevant elements.
    """
    return system_message

def docstring_generator_prompt():
    system_message = """Your task will be to generate docstrings and add comments to a provided python code.
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
    return system_message

if __name__ == "__main__":
    file_path = Path("app.py")
    code = read_python_file(file_path=file_path)
    save_to_python_file(code, file_path.parent/"app-docstring.py")
    # use the new code with docstrings for readme
    code = read_python_file(file_path=file_path.parent/"app-docstring.py")
    save_markdown_readme(code, file_path.parent/"README.md")