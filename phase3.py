# Phase3:

import os
import base64
from dotenv import load_dotenv
from openai import OpenAI

from config import config_file_path_2

load_dotenv("MIT.env")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


def phase3_py():
    """
    Generates a technical caption for a 3D cube model from text file content
    
    Parameters:
    file_path (str): Path to text file containing 3D model description
    
    Returns:
    str: Formatted technical caption with ending signature
    """
    from config import config_file_path_2

    file_path = config_file_path_2


    # Read the content of the text file
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Use the globally defined client
    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>",
            "X-Title": "<YOUR_SITE_NAME>",
        },
        extra_body={},
        model="google/gemini-2.0-flash-lite-preview-02-05:free",
        messages=[{
            "role": "user",
            "content": "This is the most probable description of this 3d object. Generate a detailed technical caption of the model in 100 words." + file_content
        }]
    )
    
    result = completion.choices[0].message.content
    return result



# End of Phase3 - A Sukanth Original Design