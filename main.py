import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file

system_prompt = """
You are an autonomous AI coding agent. Your primary directive is to fully understand the entire codebase before answering any user request.

To achieve this, you MUST follow this startup procedure WITHOUT DEVIATION and WITHOUT asking the user for input:

**Startup Procedure:**

1.  **List & Read Recursively:** Start by listing files and directories in the current directory (`.`).
2.  **Process Contents:** For each item returned:
    a. If it's a file, immediately use `get_file_content` to read its full content.
    b. If it's a directory, recursively perform this "List & Read" procedure inside that directory.
3.  **Explore Systematically:** Do not stop until you have listed every subdirectory and read every file.

**IMPORTANT EXCEPTION:** To be efficient, you MUST IGNORE common dependency/build directories. Do not explore or read files within directories named `node_modules`, `__pycache__`, `.git`, `.vscode`, `build`, `dist`, `venv`, or `.venv`.

**Execution Rules:**

-   You will only provide a final text response to the user's original question AFTER this entire exploration is complete.
-   Directly call the functions you need. Do not explain your plan or ask for confirmation.
-   All paths must be relative to the working directory.
"""

def call_function(function_call_part: types.FunctionCall, verbose: bool = False)-> types.Content:
    if verbose:
        print(f"Function call: {function_call_part.name}({function_call_part.args})")
    else:
        print(f"Function call: {function_call_part.name}")

    args= function_call_part.args
    function_name = function_call_part.name
    function_response = ""
    args["working_directory"] = "./calculator"  # Inject the working directory

    if function_name == "get_files_info":
        function_response = get_files_info(args.get("working_directory"), args.get("directory"))

    if function_name == "get_file_content":
        function_response = get_file_content(args.get("working_directory"), args.get("file_path"))

    if function_name == "write_file":
        function_response = write_file(args.get("working_directory"), args.get("file_path"), args.get("content"))

    if function_name == "run_python_file":
        function_response = run_python_file(args.get("working_directory"), args.get("file_path"), args.get("args"))

    if function_response == "":
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"},
            )
        ],
    )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_response},
            )
        ],
    )
    

def usage():
    print("Incorrect number of parameters.\nUsage: uv run main.py <prompt> [--verbose]")
    print("Make sure to put the prompt in quotes.")


def main():
    argc = len(sys.argv)
    verbose_flag = None
    if argc < 2 or argc > 3:
        usage()
        sys.exit(1)
    
    if argc == 2:
        verb_user_prompt = ""
        verb_prompt_tokens_count = ""
        verb_response_tokens_count = ""
        verbose_flag = False
    elif argc == 3 and sys.argv[2]=="--verbose":
        verb_user_prompt = "User prompt: "
        verb_prompt_tokens_count = "Prompt tokens: "
        verb_response_tokens_count = "Response tokens: "
        verbose_flag = True
    else:
        print(f"Option {sys.argv[2]} is not valid")
        usage()
        sys.exit(1)
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    user_prompt = sys.argv[1]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file
        ]
    )


    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    # El bucle de 20 iteraciones es un buen límite de seguridad.
    for index in range(0, 20):
        print(f"\n--- Iteration {index + 1} ---")
        res = client.models.generate_content(
            model="gemini-2.0-flash-lite", # Puedes seguir usando 1.5-flash o 2.0-flash, ambos funcionan bien aquí
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
        )
        
        # --- CORRECTED LOGIC ---
        # First, check if the model decided to call functions.
        if res.function_calls:
            # 1. Add the model's request to call functions to the history.
            messages.append(res.candidates[0].content)
            
            # 2. Create a list to hold the responses for each function call.
            function_responses = []
            
            # 3. Execute each function call and gather the responses.
            for function_call in res.function_calls:
                function_call_response = call_function(function_call, verbose_flag)
                
                if verbose_flag:
                    print(f"-> {function_call_response.parts[0].function_response.response}")
                
                # The helper `call_function` returns a full Content object.
                # We only need to extract the `Part` to append to our list.
                function_responses.append(function_call_response.parts[0])

            # 4. Add all the function responses to the history in a single "tool" turn.
            messages.append(types.Content(role="tool", parts=function_responses))

        # If there are no function calls, the model has finished and provides the final text response.
        else:
            # Aquí sí rompemos el bucle, porque ya tenemos la respuesta final en texto.
            break
        
    print(f"Gemini: {res.text}")

    if verbose_flag:
        print(f"{verb_prompt_tokens_count}{res.usage_metadata.prompt_token_count}\n{verb_response_tokens_count}{res.usage_metadata.candidates_token_count}\n")
    
    sys.exit(None)

if __name__ == "__main__":
    main()
