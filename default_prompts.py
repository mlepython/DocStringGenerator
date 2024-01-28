def markdown_document_prompt(custom_instructions=None):
        return """
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

def docstring_generator_prompt(custom_instructions=None):
    return"""Your task will be to generate docstrings and add comments to a provided python code.
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
# TODO need to create prompts for css, js and html files
def generic_prompt(self, custom_instructions=None):
    pass