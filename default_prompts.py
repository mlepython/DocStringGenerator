def markdown_document_prompt(custom_instructions=None):
        return """
        Project Title
-------------
Overview
--------
Provide a brief overview of the code's purpose and functionality. Explain what problem the code solves and its main features.
Dependencies
------------
List any dependencies or prerequisites needed to run the code successfully. Include information on how to install or set up these dependencies.
Usage
-----
Explain how to use the code, including relevant function/method calls or key parameters. Provide examples of how to integrate the code into other projects if applicable.
Code Examples
-------------
If applicable, provide code examples or use cases to illustrate the code in action. Showcase common scenarios where the code can be beneficial.
Configuration
--------------
Include information on any configuration options or settings that users may need to customize. Explain how users can modify these settings to adapt the code to their specific needs.
Design Decisions
----------------
Highlight important design decisions, algorithms, or patterns used in the code. Explain the reasoning behind these decisions and how they contribute to the overall functionality.
Known Issues and Limitations
-----------------------------
Mention any known issues, limitations, or bugs in the codebase. Provide information on any workarounds if available and describe any ongoing efforts to address these issues.
Future Improvements
--------------------
Discuss potential future improvements for the codebase. Outline features, enhancements, or optimizations that could be added in future releases.
Contributing
------------
Provide guidelines for developers who wish to contribute to the project. Include information on how to submit bug reports, feature requests, or pull requests.
License
-------
Specify the project's license, if applicable. Include information on how others can use, modify, and distribute the code.
Markdown Formatting
---------------------
Ensure proper Markdown formatting for headings, code blocks, lists, and any other relevant elements. Use consistent formatting to enhance readability.
Additional Documentation
-------------------------
Include links to additional documentation, if available. This can include API documentation, user guides, or any external resources that developers may find helpful.
Contact Information
--------------------
Provide contact information for maintainers or contributors. This can include email addresses, GitHub profiles, or links to relevant communication channels.

        """

def docstring_generator_prompt(custom_instructions=None):
    return"""Your task will be to generate docstrings and add comments to a provided python code.
        You will also spcifiy in the define function statement for each input the desired type and the desired output type for all functions.
        Do not modify the code. It MUST stay in its current form. Insert the docstrings for each function and add some short comments if necessary.
        Remove all blocks of code that have been commented out.

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
# TODO need to create prompts for css, js and html files
def generic_prompt(self, custom_instructions=None):
    pass