import os
from dotenv import load_dotenv
from openai import OpenAI

""" Load environment variables from .env file """
load_dotenv()


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
    Summarize this task in 1-2 very short sentences:
    Title: {task.title}
    Description: {task.description or 'No description'}
    Status: {task.status}
    """

    try:
        return get_ai_response(prompt)
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        return ""
    
def ask_ai_about_tasks(question: str, tasks: list):
    """
    Takes a user's question and a list of tasks,
    then asks OpenAI to answer based on the task data
    """
    #Convert tasks into a readable format for OpenAI
    task_list = "\n".join(
        [f"- {task.title} | Status: {task.status} | Category: {task.category or None} | Description: {task.description or 'No description'}" for task in tasks]
    )
    prompt = f"""
    You are helpful assistant that answers questions about a user's tasks.
    Here are the list of tasks:

    {task_list}

    User's question: {question}

    Answer the question clearly and concisely based on the tasks provided.
    CRITICAL FORMATTING RULES:
    1. Output your response strictly as a numbered or bulleted list.
    2. If the answer is not clear from the tasks, reply exactly with: "I'm sorry, but the answer cannot be found in the provided tasks."

    """

    try:
        return get_ai_response(prompt)
    except Exception as e:
        return f"Sorry, I couldn't process your question right now. Error: {str(e)}"