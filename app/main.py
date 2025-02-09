import os
import pandas as pd
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="Gemini-api-key")

app = FastAPI()

# Database setup
DB_URL = "sqlite:///his_database.db"
engine = create_engine(DB_URL)

# Load FAISS
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def load_faiss():
    """Reload FAISS vector store to include newly inserted data."""
    return FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

# Initialize FAISS globally
vector_store = load_faiss()
retriever = vector_store.as_retriever(search_kwargs={"k": 10})

@app.post("/insert/{table_name}")
async def insert_record(table_name: str, data: list[dict]):
    """
    Insert new records into a specified table and update FAISS vector store.
    """
    try:
        global vector_store, retriever  # Declare globals before modifying

        df = pd.DataFrame(data)
        df.to_sql(table_name, engine, if_exists="append", index=False)

        # Ensure all details (degree, specialty, experience) are vectorized
        texts = df.apply(lambda row: " ".join(row.astype(str)), axis=1).tolist()
        new_embeddings = [embeddings.embed_query(text) for text in texts]

        # Add new records to FAISS
        for i, text in enumerate(texts):
            vector_store.add_texts([text], embeddings=[new_embeddings[i]])

        # Save updated FAISS index
        vector_store.save_local("faiss_index")

        # 🔄 Reload FAISS to include new data
        vector_store = load_faiss()
        retriever = vector_store.as_retriever(search_kwargs={"k": 10})

        return {"message": f"Inserted {len(data)} record(s) into {table_name} and updated FAISS."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query")
async def query(data: dict):
    """
    Search FAISS vector database and generate an AI-powered response.
    """
    query_text = data["question"]
    
    # Retrieve relevant documents from FAISS
    docs = retriever.get_relevant_documents(query_text)
    context = " ".join([doc.page_content for doc in docs])

    # Debug: Print retrieved documents
    print("🔍 Retrieved Context from FAISS:", context)

    # Ensure Gemini gets proper context
    if not context.strip():
        return {"answer": "I couldn't find relevant information. Please rephrase your question."}

    # Generate AI response
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([{"role": "user", "parts": [f"Context: {context}. Question: {query_text}"]}])

    return {"answer": response.text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
