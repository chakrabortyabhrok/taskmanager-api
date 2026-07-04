import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

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

def ask_ai_about_tasks(question: str) -> str:
    try:
        print("=== DEBUG: Function called ===")
        print("Question received:", question)

        vectorstore = get_vectorstore()
        retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

        relevant_docs = retriever.invoke(question)
        print("Number of documents retrieved:", len(relevant_docs))

        if not relevant_docs:
            return "I couldn't find any relevant tasks for your question."

        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        prompt = f"""
        You are a helpful assistant that answers questions about the user's tasks.
        
        Important Rules:
        - You are given only a **partial list** of the user's tasks (not all of them).
        - Base your answer **only** on the tasks provided in the context below.
        - If the user asks for a count (e.g., "How many tasks...?"), and you don't have all the tasks, clearly mention that your answer is based on the available information only.
        - Do not make up or guess information.
        - If you cannot answer the question using the given tasks, politely say so.

        Here is the relevant task information:
        {context}

        User's Question: {question}

        Answer the question clearly and concisely.
        """

        return get_ai_response(prompt)

    except Exception as e:
        print("Error occurred:", e)
        return f"Sorry, something went wrong. Error: {str(e)}"

def get_vectorstore():
    """
    Reurns a persistent Chroma vvector store.
    It will create a folder called 'chroma_db' to store the data.
    """
    persist_directory = "chroma_db"

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )
    return vectorstore


def add_task_to_vectorstore(task):
    """
    Converts a Task into a well-formatted Document and stores it in Chroma.
    """
    # Create natural language content (better for embeddings)
    page_content = (
        f"Task Title: {task.title}. "
        f"Description: {task.description or 'No description provided'}. "
        f"Current Status: {task.status}. "
        f"Category: {task.category.name if task.category else 'No category'}."
    )

    metadata = {
        "task_id": task.id,
        "title": task.title,
        "status": task.status,
        "category": task.category.name if task.category else "None"
    }
    #Create a Document
    document = Document(page_content=page_content, metadata=metadata)
    #Get vectore store and add the document 
    vectorstore = get_vectorstore()
    vectorstore.add_documents([document])

def backfill_tasks_to_chroma():
    """
    Add all existing tasks from database to Chroma.
    """
    from core.models import Task

    tasks = Task.objects.all()
    count = 0

    for task in tasks:
        add_task_to_vectorstore(task)
        count += 1

    print(f"Successfully added {count} tasks to Chroma.")