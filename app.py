from openai import ChatCompletion
import os
import requests
from pathlib import Path


MODEL_NAME = "gpt-4-0613"
MAX_TOKENS = 1500
api_url = 'https://api.openai.com/v1/chat/completions'
api_key = os.getenv("OPENAI_API_KEY")
# client = OpenAI()
def run_openai(messages: list):
        response = ChatCompletion.create(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=MAX_TOKENS
        )
        return response.choices[0].message.content

def call_openai_api(messages):
    data = {
        'messages': messages,
        'max_tokens': MAX_TOKENS,
        'model': MODEL_NAME
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    try:
        response = requests.post(api_url, json=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            print('OpenAI Response:', result)
            openai_result = result['choices'][0].get('message', {}).get('content')
            return openai_result
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"Exception: {e}")
        return None


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

def save_to_python_file(text, python_file_path):
    code = text.split("```python")[-1].split("```")[0]
    with open(python_file_path, 'w', encoding='utf-8') as python_file:
        python_file.write(code)
    print(f'Python code successfully written to: {python_file_path}')


if __name__ == "__main__":
    code = read_python_file(file_path=r"C:\Users\mike_\OneDrive\Documents\OpenAI and Python\ImageAnalysisOPENAI\app.py")
    system_message = """Your task will be to generate docstrings and add comments to a provided python code.
    You will also spcifiy in the define function statement for each input the desired type and the desired output type for all functions.
    Do not modify the code. It MUST stay in its current form. Insert the docstrings for each function and add some short comments if necessary.
    IF there are any parent classes that are inherited using super(), use ':meth:`MyBaseClass.some_method`' 
    For the output format, SHOW THE COMPLETE CODE with the added docstrings and comments:
    ```python
    <python code>
    ```
    Here is an example output:
    ```python
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
    ```
    """
    user_message = f"""{code}"""
    # results = call_openai_api(messages=openai_messages(system_message, user_message))
    results = run_openai(messages=openai_messages(system_message, user_message))
    print(results)
    save_to_python_file(results, "./output/new_app.py")