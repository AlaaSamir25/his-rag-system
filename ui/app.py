import streamlit as st
import requests

st.title("AI-Powered HIS Customer Service")

# User input for query
query = st.text_input("Ask a question about the hospital:")

if st.button("Submit"):
    response = requests.post("http://127.0.0.1:8000/query", json={"question": query})
    if response.status_code == 200:
        st.write("**Answer:**", response.json()["answer"])
    else:
        st.write("Error in fetching response")
