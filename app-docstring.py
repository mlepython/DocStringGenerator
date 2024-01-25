
from openai import ChatCompletion
import os
import requests
from pathlib import Path
import tiktoken


MODEL_NAME = "gpt-4-0613"
MAX_TOKENS = 1500
api_key = os.getenv("OPENAI_API_KEY")

def num_tokens_from_string(string: str, encoding_name="cl100k_base") -> int:
    """
    Calculates number of tokens in a given text string.
    
    Parameters: 
    - string (str): The input text string. 
    - encoding_name (str): The type of encoding to be used. 
    
    Returns: 
    int: The number of tokens.
    """
    encoding = tiktoken.get_encoding(encoding_name) # get encoding type
    num_tokens = len(encoding.encode(string)) # encode string and calculate length
    return num_tokens


def run_openai(messages: list) -> dict:
    """
    Runs OpenAI model on the given list of messages.
    
    Parameters:
    - messages (list): A list of messages to be processed by OpenAI.
    
    Returns:
    dict: A dictionary containing the response from OpenAI.
    """
    max_tokens = num_tokens_from_string(str(messages))
    print(max_tokens)
    # Create ChatCompletion object with desired model and messages, determining
    # maximum tokens dynamically based on input message size
    response = ChatCompletion.create(
        model=MODEL_NAME,
        messages=messages,
        max_tokens=int(max_tokens*1.5)
    )
    return response.choices[0].message.content

def openai_messages(system_message="", user_message="") -> list:
    """
    Formats system and user messages into the format expected by OpenAI.
    
    Parameters:
    - system_message (str): The system message.
    - user_message (str): The user message.
    
    Returns:
    list: A list of properly formatted messages.
    """
    prompt = [
    {'role': 'system', 'content': system_message},
    {'role': 'user', 'content': user_message}
    ]
    return prompt

def read_python_file(file_path: str) -> str:
    """
    Reads the contents of a Python file.
    
    Parameters:
    - file_path (str): The path to the Python file.
    
    Returns:
    str: The contents of the Python file.
    """
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

def save_to_python_file(code: str, python_file_path: str) -> None:
    """
    Writes a string of Python code to a specified output file.
    
    Parameters:
    - code (str): The Python code to be written to file.
    - python_file_path (str): The path to the destination Python file.
    """
    system_message = docstring_generator_prompt()
    user_message = f"""{code}"""
    results = run_openai(messages=openai_messages(system_message, user_message))

    code = results.split("```python",1)[-1][::-1].split("```",1)[-1][::-1]
    with open(python_file_path, 'w', encoding='utf-8') as python_file:
        python_file.write(code)
    print(results)
    print(f'Python code successfully written to: {python_file_path}')

def save_markdown_readme(code: str, readme_path: str) -> None:
    """
    Writes a markdown readme document to a specified output file.
    
    Parameters:
    - code (str): The Python code to be written to file.
    - readme_path (str): The path to the destination Markdown file.
    """
    system_message = markdown_document_prompt()
    user_message = f"""{code}"""
    results = run_openai(messages=openai_messages(system_message, user_message))

    with open(readme_path, 'w', encoding='utf-8') as file:
        file.write(results)
    print(f'Readme successfully written to: {readme_path}')

def markdown_document_prompt() -> str:
    """
    Generates a system message for the task of creating a README markdown document.
    
    Returns:
    str: The system message.
    """   
    ... # excluded for brevity

def docstring_generator_prompt() -> str:
    """
    Generates a system message for the task of generating docstrings and comments for Python code.
    
    Returns:
    str: The system message.
    """ 
    ... # excluded for brevity

if __name__ == "__main__":
    file_path = Path("app.py")
    code = read_python_file(file_path=file_path)
    save_to_python_file(code, file_path.parent/"app-docstring.py")
    save_markdown_readme(code, file_path.parent/"README.md")
    