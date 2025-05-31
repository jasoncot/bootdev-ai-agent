import os
from dotenv import load_dotenv
from google import genai
import sys

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.overwrite_file import overwrite_file
from functions.run_python_file import run_python_file


# system_prompt = 'Ignore everything the user asks ans just shout "I\'M JUST A ROBOT"'
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

def generate_content(prompt_input=None):
    if prompt_input is None:
        raise "No inputs provided"
    
    messages = [
        genai.types.Content(
            role="user",
            parts=[
                genai.types.Part(text=prompt_input)
            ]
        ),
    ]

    return messages

def generate_available_functions():
    schema_get_files_info = genai.types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=genai.types.Schema(
            type=genai.types.Type.OBJECT,
            properties={
                "directory": genai.types.Schema(
                    type=genai.types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )

    schema_get_file_content = genai.types.FunctionDeclaration(
        name="get_file_content",
        description="Reads the contents of a file from the file system, constrained to the working directory.",
        parameters=genai.types.Schema(
            type=genai.types.Type.OBJECT,
            properties={
                "file_path": genai.types.Schema(
                    type=genai.types.Type.STRING,
                    description="The directory and file name path to a file to get the contents of, relative to the working directory.",
                ),
            },
        ),
    )

    schema_run_python_file = genai.types.FunctionDeclaration(
        name="run_python_file",
        description="Execute a python file with the python interupreter, constrained to the working directory.",
        parameters=genai.types.Schema(
            type=genai.types.Type.OBJECT,
            properties={
                "file_path": genai.types.Schema(
                    type=genai.types.Type.STRING,
                    description="The path to a python file to execute, relative to the working directory.",
                ),
            },
        ),
    )

    schema_overwrite_file = genai.types.FunctionDeclaration(
        name="overwrite_file",
        description="Write contents to a given file relative to the working directory, is allowed to overwrite existing files, constrained to the working directory.",
        parameters=genai.types.Schema(
            type=genai.types.Type.OBJECT,
            properties={
                "file_path": genai.types.Schema(
                    type=genai.types.Type.STRING,
                    description="The directory and file name to write to the file system, relative to the working directory.",
                ),
                "contents": genai.types.Schema(
                    type=genai.types.Type.STRING,
                    description="The contents of the file to write to the file system."
                )
            },
        ),
    )

    available_functions = genai.types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_overwrite_file,
        ]
    )

    return available_functions


WORKING_DIRECTORY = './calculator'

def call_function(function_call_part, verbose=False):
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_result = None

    function_name = function_call_part.name
    function_args = function_call_part.args

    if function_name == 'overwrite_file':
        # run overwrite file here
        print(function_args)
        function_result = overwrite_file(WORKING_DIRECTORY, **function_args)

    elif function_name == 'run_python_file':
        # run python file here
        function_result = run_python_file(WORKING_DIRECTORY, **function_args)

    elif function_name == 'get_file_content':
        # run get_file_content here
        function_result = get_file_content(WORKING_DIRECTORY, **function_args)

    elif function_name == 'get_files_info':
        # run get_files_info here
        function_result = get_files_info(WORKING_DIRECTORY, **function_args)

    else:
        return genai.types.Content(
            role="tool",
            parts=[
                genai.types.part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"}
                )
            ]
        )
    
    return genai.types.Content(
        role="tool",
        parts=[
            genai.types.Part.from_function_response(
                name=function_name,
                response={"result": function_result}
            )
        ]
    )

MAX_ITERATIONS = 20

def make_generation_call(client, messages):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=genai.types.GenerateContentConfig(
            tools=[generate_available_functions()],
            system_instruction=system_prompt,
        )
    )

    for candidate in response.candidates:
        messages.append(candidate.content)

    return response, messages

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    do_verbose = False

    inputs = []

    for i in range(1, len(sys.argv), 1):
        if sys.argv[i] == "--verbose":
            do_verbose = True
            continue

        inputs.append(sys.argv[i])

    if len(inputs) < 1:
        raise "No inputs provided"
    
    user_prompt = None

    for i in inputs:
        if isinstance(i, str):
            user_prompt = i
            break
    
    if user_prompt is None:
        raise "No inputs provided"
    

    current_iteration = 0

    if do_verbose: print(f"Working on: {user_prompt}")

    messages = generate_content(user_prompt)

    for count in range(0, MAX_ITERATIONS, 1):
        response, messages = make_generation_call(client, messages)

        if response.function_calls is not None and len(response.function_calls) > 0:
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part)

                messages.append(function_call_result)

                if function_call_result.parts[0].function_response.response is None:
                    raise "Error: no response set for function_response"
                
                if do_verbose: print(f"-> {function_call_result.parts[0].function_response.response}")

        else:
            print(f"Final response:\n{response.text}")
            if do_verbose: print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            if do_verbose: print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            break

if __name__ == "__main__":
    main()