import os
from dotenv import load_dotenv
from openai import OpenAI

""" Load environment variables from .env file """
load_dotenv()

""" Initialize OpenAI client """
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_ai_response(prompt: str, model: str = "gpt-4o-mini") -> str:
    """ 
    Send a prompt to OpenAI and return the response.
    This is a reusable function for future AI tasks.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error: {str(e)}"