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
    """
    Takes a user's question, retrieves relevant tasks from Chroma,
    and returns an AI-generated answer.
    """
    try:
        #Get the vector store
        vectorstore = get_vectorstore()

        #Retrieve most relevant tasks
        retriever = vectorstore.as_retriever(search_kwargs={
            "k": 8,
            "score_threshold": 0.3
            }
        )
        relevant_docs = retriever.invoke(question)

        if not relevant_docs:
            return "I couldn't find any relevant tasks for your question"
        
        #Combining the content of relevant documents
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        
        prompt = f"""
        You are helpful assistant that answers questions about a user's tasks.
        Here are some relevant tasks:

        {context}

        User's question: {question}

        Answer the question clearly and concisely based on the tasks above.
        (Dont Give in normal paragraph style, should be in a structure with points or numbers)
        If the answer is not clear from the tasks, say so politely.
      
        """

        return get_ai_response(prompt)

    except Exception as e:
        return f"Sorry, something went wrong while processing your question. Error: {str(e)}"
    
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
    Converts a Task object into a Document and adds it to Chroma
    """
    #Combine title,status,description to create content for embedding
    page_content = f"Title: {task.title}\nDescription: {task.description or 'No description'}\nStatus: {task.status}"

    #Add metadata
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