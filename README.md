# AI-Powered HIS Customer Service (RAG System)

This project is an **AI-powered Retrieval-Augmented Generation (RAG) system** for **Pain & Go Hospital Information System (HIS)**. It allows users to:
- **Query hospital data** (doctor schedules, specialties, pricing)
- **Insert new records dynamically by Admin** and update the **FAISS vector store**
- **Retrieve relevant documents** using FAISS & Gemini AI

## 🚀 Features
- **Query API**: Ask questions like _“What is the degree of Dr. Mohamed?”_
- **Data Insertion API**: Insert new doctors, schedules, policies & automatically update FAISS
- **Vector Search**: Uses **FAISS** to store and retrieve relevant hospital information
- **RAG Pipeline**: Combines retrieved data with **Gemini AI** for a meaningful response
- **User-Friendly UI**: Streamlit interface for easy interaction

---

## 📌 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/his-rag-system.git
cd his-rag-system
```

### 2️⃣ Create a Virtual Environment
```bash
conda create -n his-rag python=3.10
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Create Gemini API-Key

Gemini API-Key='Gemini API key or other LLM provider'

### 4️⃣ Set Up the Database
```bash
python app/database.py
```
This **loads hospital data from Excel into SQLite**.

### 5️⃣ Generate Embeddings & Initialize FAISS
```bash
python app/vector_store.py
```
This **converts database text into embeddings** and **stores them in FAISS**.

---

## 📌 Running the Application
### 1️⃣ Start FastAPI Backend
```bash
uvicorn app.main:app --reload
```
- FastAPI runs at **http://127.0.0.1:8000**
- Open **http://127.0.0.1:8000/docs** to view API documentation

### 2️⃣ Start the Streamlit UI
```bash
streamlit run ui/app.py
```
- This opens the **AI-powered hospital chatbot UI**

---

## 📌 API Endpoints

### 🔹 Insert Data API
**Insert a new doctor into the database and update FAISS.**  
📌 **Endpoint:** `POST /insert/{table_name}`  

#### Example Request
```python
import requests

BASE_URL = "http://127.0.0.1:8000"
url = f"{BASE_URL}/insert/Physicians"

data = [
    {
        "name": "Dr. Mohamed",
        "specialty": "Cardiology",
        "degree": "MD, PhD in Cardiology"
    }
]

response = requests.post(url, json=data)
print(response.json())
```
#### Expected Response
```json
{"message": "Inserted 1 record(s) into Physicians and updated FAISS."}
```
---

```bash
python test_insert_api.py
```
This **for test insert API endpoint for Admin**.

---

## 📌 Project Structure
```
HIS_RAG_Project/
├── app/
│   ├── main.py               # FastAPI backend
│   ├── database.py           # Loads data into SQLite
│   ├── vector_store.py       # Creates FAISS vector database
├── data/
│   ├── HIS_data.xlsx         # Hospital data
├── ui/
│   ├── app.py                # Streamlit UI
├── test_insert_api.py               # API testing script
├── requirements.txt          # Dependencies
├── README.md                 # Project documentation
```
---