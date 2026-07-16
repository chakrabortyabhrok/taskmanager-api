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
            temperature=0.7
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


def get_vectorstore():
    """
    Smart vectorstore:
    - On Render (has DATABASE_URL) → uses PGVector (PostgreSQL)
    - Locally (SQLite) → returns None (embedding is skipped)
    """
    connection_string = os.environ.get("DATABASE_URL")

    if not connection_string:
        # Running locally with SQLite → no pgvector available
        print("⚠️  Running on SQLite. Vector store is disabled (pgvector needs PostgreSQL).")
        return None

    from langchain_postgres import PGVector

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vectorstore = PGVector(
        embeddings=embeddings,
        collection_name="task_embeddings",
        connection=connection_string,
        use_jsonb=True,
    )
    return vectorstore


def add_task_to_vectorstore(task):
    """
    Adds task to vector store only if PostgreSQL is available.
    """
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
    
