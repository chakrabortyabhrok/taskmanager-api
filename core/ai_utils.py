import os
from dotenv import load_dotenv
from openai import OpenAI

""" Load environment variables from .env file """
load_dotenv()


#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_ai_response(prompt: str, model: str = "gpt-4o-mini") -> str:
    """ 
    Send a prompt to OpenAI and return the response.
    This is a reusable function for future AI tasks.
    """
    try:
        """ Initialize OpenAI client """
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
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
    
def generate_task_summary(task):
    """Generate a short AI summary for a task."""
    prompt = f"""
    Summarize this task in 1-2 short sentences:
    Title: {task.title}
    Description: {task.description or 'No description'}
    Status: {task.status}
    """

    try:
        return get_ai_response(prompt)
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        return ""