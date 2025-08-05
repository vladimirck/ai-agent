import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import get_files_info


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

    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    res = client.models.generate_content(
        model = "gemini-2.0-flash-001",
        contents=messages,
    )
    
    if verbose_flag:
        print(f"{verb_user_prompt}{user_prompt}\n")
    
    print(f"Gemini: {res.text}")
    
    if verbose_flag:
        print(f"{verb_prompt_tokens_count}{res.usage_metadata.prompt_token_count}\n{verb_response_tokens_count}{res.usage_metadata.candidates_token_count}\n")
    
    sys.exit(None)

if __name__ == "__main__":
    main()
