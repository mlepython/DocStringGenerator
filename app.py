from openai import ChatCompletion
import os
import requests
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
        ## Objective

    Create a Markdown document with the following elements:

    1. Heading: Use a main heading with the document title.
    2. Subheadings: Include at least two subheadings with relevant titles.
    3. Lists: Create an ordered list and an unordered list.
    4. Links: Insert a hyperlink to an external website.
    5. Images: Embed an image in the document.
    6. Emphasis: Apply emphasis to specific words using bold and italic formatting.

    ## Instructions

    1. Start with a main heading at the beginning of your document. Use `#` to denote a heading.
    2. Add two subheadings beneath the main heading. Use `##` for subheadings.
    3. Create an ordered list with steps for a simple task using numbers.
    4. Below the ordered list, create an unordered list with items related to your interests or hobbies.
    5. Insert a hyperlink to your favorite website. Use the following syntax: `[Link Text](URL)`.
    6. Embed an image into the document. Use the following syntax: `![Alt Text](Image URL)`.
    7. Apply bold formatting to a word or phrase using `**double asterisks**`.
    8. Apply italic formatting to another word or phrase using `*single asterisks*`.

    Feel free to add additional elements or customize the content as you like. Once you've completed the document, save it with a `.md` file extension.

    Output format should be:
    ```README
    <text>
    ```
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
    save_markdown_readme(code, file_path.parent/"README.md")