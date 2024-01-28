from openai import OpenAI
import os
from pathlib import Path
import tiktoken
from prettytable import PrettyTable
import default_prompts

table = PrettyTable()
client = OpenAI()

class CodeCleaner():
    def __init__(self, api_key=None) -> None:
        # self.model_name = "gpt-3.5-turbo-1106"
        self.model_name = "gpt-4-1106-preview"
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.custom_instructions = None
        self.file_contents = ""
        self.js = ""
        self.html = ""
        self.md = ""
        self.css = ""

        if not self.api_key:
            raise ValueError("API key is required. Set the OPENAI_API_KEY environment variable.")

    def num_tokens_from_messages(self, string: str, encoding_name="cl100k_base") -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        if "gpt-4" in self.model_name:
            cost = num_tokens/1000*0.01
        else:
            cost = num_tokens/1000*0.001
        return num_tokens, cost

    def call_openai(self, user_message):
        messages = [{'role': 'system', 'content': self.system_message}, {'role': 'user', 'content': user_message}]
        max_tokens, _ = self.num_tokens_from_messages(str(messages))
        response = client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            max_tokens=int(max_tokens*1.3)
        )
        return response.choices[0].message.content

    # def openai_messages(self, system_message, user_message):
    #     prompt = [
    #     {'role': 'system', 'content': system_message},
    #     {'role': 'user', 'content': user_message}
    #     ]
    #     return prompt

    def read_file(self, file_path):
        print(f"Reading file {file_path}")
        try:
            with open(file_path, 'r') as file:
                self.file_contents = file.read()
        except FileNotFoundError:
            print(f"Error: File not found - {file_path}")
            self.file_contents = None
        except Exception as e:
            print(f"Error: {e}")
            self.file_contents = None
        
    def write_file(self, file_path, content):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

    def process_file(self, file, ouput_file_path):
        # creates system message
        self.system_message_prompt(ouput_file_path)
        # read in file
        self.read_file(file_path=file)
        # call openai and set user message to file contents
        # TODO add some more usability for user_message to allow for custom instruction
        results = self.call_openai(user_message=self.file_contents)
        if ouput_file_path.suffix == ".py":
            new_code = results.split("```python",1)[-1][::-1].split("```",1)[-1][::-1]
            self.write_file(file_path=ouput_file_path, content=new_code)
            print(f'Python code successfully written to: {ouput_file_path}')
        elif ouput_file_path.suffix == ".md":
            self.write_file(file_path=ouput_file_path, content=results)
            print(f'Readme successfully written to: {ouput_file_path}')
        else:
            pass
    
    def system_message_prompt(self, file_path):
        if not self.custom_instructions:
            if file_path.suffix == ".py":
                print('Python File')
                self.system_message = default_prompts.docstring_generator_prompt()
            elif file_path.suffix == ".md":
                print("Markdown Document")
                self.system_message = default_prompts.markdown_document_prompt()
            else:
                self.system_message = ""

    def get_files(self, directory_path, extensions=[".py", ".html", ".js", ".css", ".md"]):
        # get the contents from the gitigore file
        gitignore_contents, gitignore_contents_path = read_contents_from_gitignore(directory_path)
        files = []
        for extension in extensions:
            files.extend(directory_path.glob(f'*{extension}'))
        subdirectories = [subdir for subdir in directory_path.iterdir() if subdir.is_dir()]
        # make a list of all files to be updated/cleaned with openai unless the file/directory is listed in the .gitignore
        for subdir in subdirectories:
            if str(subdir.name) not in gitignore_contents:
                for extension in extensions:
                    for file in subdir.glob(f'*{extension}'):
                        if all(str(file) not in str(gitignore) for gitignore in gitignore_contents_path):
                            files.append(file)

        return files
    def files_for_modifiction(self, file_dir):
        if file_dir.is_dir():
            table.field_names = ["index", "File Name", "Token Count", "Cost Estimate"]
            files = self.get_files(directory_path=file_dir)
            print("Files in directory: ", file_dir)
            for index, file in enumerate(files):
                self.system_message_prompt(file)
                if file.suffix == ".py":
                    self.read_file(file_path=file)
                    tokens, cost = self.num_tokens_from_messages(self.system_message+self.file_contents)
                elif file.suffix == ".md":
                    self.read_file(file_path=file)
                    tokens, cost = self.num_tokens_from_messages(self.system_message+self.file_contents)
                else:
                    tokens, cost = 0, 0
                table.add_row([index, file.name, tokens, round(cost,4)])
            print(table)
        else:
            file = file_dir
            # TODO if a single file is inputted 
        pass

def read_contents_from_gitignore(directory):
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
    # openai_code_cleaner.get_files(file_path.parent)
    openai_code_cleaner.files_for_modifiction(file_path.parent)
    # openai_code_cleaner.get_files_with_suffixes(file_path.parent)
    
    
    # read python file
    # openai_code_cleaner.read_file(file_path)
    
    # Example: Convert to docstrings only
    # openai_code_cleaner.create_docstrings(python_output_file_path=file_path.parent/"app-docstring.py")
    # openai_code_cleaner.process_file(file=file_path, ouput_file_path=file_path.parent/"app-docstring.py")
    # Example: Create a readme document
    # openai_code_cleaner.read_file(file_path=file_path.parent/"app-docstring.py")
    # openai_code_cleaner.create_markdown_document(readme_path=file_path.parent/"README.md")
    openai_code_cleaner.process_file(file=file_path, ouput_file_path=file_path.parent/"README.md")
