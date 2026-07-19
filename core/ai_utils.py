import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

load_dotenv()

def get_ai_response(prompt: str, model: str = "gpt-4o-mini") -> str:
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def generate_task_summary(task):
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

def auto_categorize_task(title, description):
    prompt = f"""
    According to the title and description provided, recommend category for the user:  
    Title: {title}
    Description: {description}

    Rules:
    - return in a fixed format (example: Category: Work)
    - no extra sentenses or words. just in the fixed format
    """
    try:
        return get_ai_response(prompt)
    except Exception as e:
        print(f"Error generating category: {str(e)}")
        return ""

def get_vectorstore():
    """
    Hybrid Vector Store:
    - Render (has DATABASE_URL) → PGVector
    - Local → Chroma
    """
    from langchain_openai import OpenAIEmbeddings
    import os

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    connection_string = os.environ.get("DATABASE_URL")

    # ========== Production (Render) ==========
    if connection_string:
        from langchain_postgres import PGVector
        return PGVector(
            embeddings=embeddings,
            collection_name="task_embeddings",
            connection=connection_string,
            use_jsonb=True,
        )

    # ========== Local Development (Chroma) ==========
    from langchain_chroma import Chroma
    return Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings,
        collection_name="task_embeddings"
    )


def add_task_to_vectorstore(task):
    """
    Adds task to vector store only if PostgreSQL is available.
    """
    print(f">>> Embedding task ID: {task.id} | Title: {task.title}")
    vectorstore = get_vectorstore()

    if vectorstore is None:
        # Local SQLite mode → skip embedding
        return

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

    document = Document(page_content=page_content, metadata=metadata)
    vectorstore.add_documents([document])


def ask_ai_about_tasks(question: str) -> str:
    try:
        vectorstore = get_vectorstore()

        if vectorstore is None:
            return "AI search is only available in production (PostgreSQL + pgvector)."

        retriever = vectorstore.as_retriever(search_kwargs={"k": 15})
        relevant_docs = retriever.invoke(question)

        if not relevant_docs:
            return "I couldn't find any relevant tasks for your question."

        context = "\n\n".join([doc.page_content for doc in relevant_docs])

        prompt = f"""
        You are a helpful assistant that answers questions about the user's tasks.

        Important Rules:
        - You are given only a partial list of the user's tasks (not all of them).
        - Base your answer only on the tasks provided below.
        - If the user asks for a count and you don't have all tasks, say so clearly.
        - If no question given, say so politely.
        - Do not make up information.

        Relevant tasks:
        {context}

        User's Question: {question}

        Answer clearly and concisely.
        """
        return get_ai_response(prompt)

    except Exception as e:
        print("Error in ask_ai_about_tasks:", e)
        return f"Sorry, something went wrong. Error: {str(e)}"
    
def clear_vectorstore():
    """
    Completely clears all documents from the pgvector collection.
    Use this carefully.
    """
    vectorstore = get_vectorstore()

    if vectorstore is None:
        print("Vector store is not available (running on SQLite).")
        return False

    try:
        # This deletes the entire collection and recreates it empty
        vectorstore.delete_collection()
        print("Successfully cleared the vector store.")
        return True
    except Exception as e:
        print(f"Error while clearing vector store: {e}")
        return False