import os
from sentence_transformers import SentenceTransformer
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from sqlalchemy import create_engine

# Define Database Connection
DB_URL = "sqlite:///his_database.db"
engine = create_engine(DB_URL)

# Load Sentence Transformer Model
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def get_embedding(text):
    """Generate text embedding using Sentence Transformers."""
    return embedding_model.encode(text).tolist()

def ingest_data():
    """Ingest data from database, generate embeddings, and store in FAISS."""
    sheets = ["Physicians", "Schedules", "Specialities", "Pricelist", "Policy"]
    all_texts, embeddings = [], []

    for sheet in sheets:
        df = pd.read_sql(f"SELECT * FROM {sheet}", engine)
        texts = df.apply(lambda row: " ".join(row.values.astype(str)), axis=1).tolist()
        all_texts.extend(texts)

    # Generate embeddings
    embeddings = [get_embedding(text) for text in all_texts]

    # Store embeddings in FAISS
    vector_store = FAISS.from_texts(all_texts, HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"))
    vector_store.save_local("faiss_index")

if __name__ == "__main__":
    ingest_data()
