import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from pinecone import Pinecone, ServerlessSpec

# Initialize Pinecone client
pc = Pinecone(api_key="pcsk_4FW6nc_KCvYDUXeMCUT6Cb3YCfANmRnmyiibejoKybbGSnzmyRQUzNpsEEjpY6Qk1nPjJM")
index_name = "financial-qa-index"

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
pinecone_index = pc.Index(index_name)

# Load SentenceTransformer model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# QA Pipeline
qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-base")

# Pre-defined Profit and Loss Data
pl_data = {
    "Quarter": [f"Q{(i % 4) + 1} {2000 + (i // 4)}" for i in range(100)],
    "Revenue": [150000 + (i * 30000) for i in range(100)],
    "Operating Expenses": [80000 + (i * 10000) for i in range(100)],
    "Net Income": [70000 + (i * 5000) for i in range(100)],
    "Gross Profit": [100000 + (i * 10000) for i in range(100)],
    "EBT (Earnings Before Tax)": [65000 + (i * 5000) for i in range(100)],
}

# Convert data to DataFrame and add descriptions
pl_df = pd.DataFrame(pl_data)
pl_df["Description"] = pl_df.apply(
    lambda row: f"Quarter: {row['Quarter']}, Revenue: {row['Revenue']}, "
                f"Operating Expenses: {row['Operating Expenses']}, "
                f"Net Income: {row['Net Income']}, Gross Profit: {row['Gross Profit']}, "
                f"EBT: {row['EBT (Earnings Before Tax)']}",
    axis=1
)

# Generate embeddings
embeddings = embedding_model.encode(pl_df["Description"].tolist(), show_progress_bar=True)

# Upload embeddings to Pinecone
def upload_embeddings_to_pinecone():
    vectors = [
        {
            "id": str(i),
            "values": embeddings[i],
            "metadata": {"text": pl_df["Description"][i]},
        }
        for i in range(len(embeddings))
    ]
    pinecone_index.upsert(vectors)

# Retrieve relevant context from Pinecone
def retrieve_relevant_context(query, top_k=3):
    query_embedding = embedding_model.encode(query).tolist()
    search_results = pinecone_index.query(
        vector=query_embedding, top_k=top_k, include_metadata=True
    )
    return [result["metadata"]["text"] for result in search_results["matches"]]

# RAG QA function
def rag_qa(query):
    try:
        context = retrieve_relevant_context(query)
        input_text = f"Context: {' '.join(context)} Question: {query}"
        answer = qa_pipeline(input_text, max_length=100, truncation=True)
        return answer[0]["generated_text"]
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit App
def main():
    st.title("QA Chat bot")

    # Automatically upload data to Pinecone on page load
    upload_embeddings_to_pinecone()

    # Query input and response
    user_query = st.text_input("Enter your financial query:")
    if st.button("Get Answer"):
        if user_query:
            answer = rag_qa(user_query)
            st.write("**Your Query:**", user_query)
            st.write("**Answer:**", answer)
        else:
            st.error("Please enter a query before getting an answer.")

    # Sidebar file uploader (optional)
    st.sidebar.header("Upload File")
    uploaded_file = st.sidebar.file_uploader("Upload P&L File (PDF only)", type=["pdf"])
    if uploaded_file:
        st.sidebar.success("PDF uploaded successfully!")

    # Display P&L table
    st.write("**Profit and Loss Table:**")
    st.dataframe(pl_df)

if __name__ == "__main__":
    main()
