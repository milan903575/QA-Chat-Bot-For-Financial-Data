
# **Generative AI Chatbot for Financial Data Analysis**

## **Overview**
This project implements a Generative AI Chatbot designed to answer financial queries based on Profit & Loss (P&L) data. The chatbot is built using state-of-the-art technologies like Pinecone, Sentence Transformers, and FLAN-T5 for Retrieval-Augmented Generation (RAG). 

The project includes:
1. **Backend RAG Model**: Implemented in Colab for query processing.
2. **Frontend Interface**: A Streamlit-based UI for file uploads and real-time querying.
3. **PDF Preprocessing Script**: A standalone script for handling real-world challenges in financial document extraction.

---

## **Features**
- Supports **PDF** file uploads for financial data.
- Automatically processes and stores data in a Pinecone vector database.
- Uses **RAG** for generating accurate, natural language responses to user queries.
- Includes a separate preprocessing script for PDFs with complex layouts.

---

## **Technologies Used**
- **Python**: Core programming language.
- **Streamlit**: Frontend for the chatbot.
- **Pinecone**: Vector database for similarity search.
- **Sentence Transformers**: For generating embeddings.
- **FLAN-T5**: Generative model for answering queries.
- **pdfplumber**: For table extraction from PDFs.
- **Tesseract OCR**: For text extraction from image-based PDFs.
- **DistilBART**: For text summarization.

---

## **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone https://github.com/milan903575/QA-Chat-Bot-For-Financial-Data.git
git clone .git
cd QA-Chat-Bot-For-Financial-Data
```

### **2. Install Dependencies**
Ensure you have Python 3.8+ installed.

```bash
pip install -r requirements.txt
```

### **3. Pinecone Setup**
1. **Create a Pinecone Account**:
   - Sign up at [Pinecone.io](https://www.pinecone.io/).
2. **Generate API Key**:
   - Navigate to the API section in the Pinecone dashboard and copy your API key.
3. **Create Index**:
   - Create an index with the following configurations:
     - **Name**: `financial-qa-index`
     - **Dimensions**: `384`
     - **Metric**: `cosine`
     - **Cloud Provider**: `AWS`
     - **Region**: `us-east-1`

Update your Pinecone API key in the `chatbot_streamlit.py` file:
```python
pc = Pinecone(api_key="your-api-key")
```

### **4. Streamlit Frontend**
1. **Run the Streamlit App**:
   ```bash
   streamlit run chatbotstreamlit.py
   ```
2. **Access the App**:
   - Open the link displayed in your terminal (e.g., `http://localhost:8501`).

---

## **Usage Instructions**

### **1. Frontend: Streamlit Chatbot**
- **Upload File**: 
  - Supported formats: PDF and Excel.
  - Upload your P&L data for processing.
- **Enter Query**:
  - Type a financial query (e.g., "What is the net income for Q1 2020?").
- **View Response**:
  - The chatbot retrieves relevant data and generates a natural language response.

### **2. Backend: RAG Model in Colab**
- Use the provided Colab notebook (`ChatBot_collab.ipynb`) for backend testing:
  - **Data Preparation**: Generate embeddings for P&L data.
  - **Store in Pinecone**: Upload embeddings for similarity-based retrieval.
  - **Query and Answer**: Test predefined queries.

### **3. PDF Preprocessing Script**
- Run `test.py` for advanced PDF preprocessing:
  - Extracts tables and text from complex PDFs.
  - Summarizes text using the `distilbart-cnn` model.
  - Saves the processed P&L table as a CSV.

```bash
python preprocessing.py
```

---

## **Project Workflow**

### **1. Backend (Colab Implementation)**
1. **Predefined Data**:
   - Generate dummy financial data for P&L statements.
2. **Embedding Generation**:
   - Convert data descriptions into 384-dimensional vectors using Sentence Transformers.
3. **Pinecone Integration**:
   - Store embeddings in Pinecone for similarity-based retrieval.
4. **Query Processing**:
   - Retrieve relevant data and pass it to FLAN-T5 for generating responses.

### **2. Frontend (Streamlit)**
1. **File Upload**:
   - Accepts PDF files.
2. **Query Input**:
   - Allows users to enter financial queries.
3. **Real-Time Response**:
   - Generates responses based on the uploaded data.

### **3. PDF Preprocessing**
1. **Table Extraction**:
   - Uses `pdfplumber` for detecting and extracting tables from PDFs.
2. **OCR-Based Text Extraction**:
   - Extracts text from image-based PDFs using Tesseract OCR.
3. **Text Summarization**:
   - Summarizes lengthy financial text into concise insights.

---

## **Challenges and Solutions**

### **Challenges**
1. **Complex PDF Layouts**:
   - Irregular tables and merged cells caused data extraction issues.
2. **Large Document Processing**:
   - Memory and performance limitations for large PDFs.
3. **Preprocessing Errors**:
   - OCR and table extraction sometimes failed for low-quality scans.

### **Solutions**
1. **Separate Preprocessing Script**:
   - Decoupled PDF preprocessing for debugging and testing.
2. **Fallback Mechanisms**:
   - Summarization to handle pages without tables.
3. **Efficient Embedding Search**:
   - Optimized query processing with Pinecone for fast retrieval.

---

## **Examples**

### **Queries and Responses**
1. **Query**: "What is the net income for Q1 2020?"
   - **Response**: "The net income for Q1 2020 is $300,000."
2. **Query**: "Which quarter in 2019 had the highest revenue?"
   - **Response**: "Q4 2019 had the highest revenue of $650,000."
3. **Query**: "How has the operating income changed from 2015 to 2020?"
   - **Response**: "Operating income increased from $200,000 in 2015 to $450,000 in 2020."

---

## **Future Improvements**
1. **Advanced PDF Parsing**:
   - Enhance the preprocessing script to handle irregular table structures and noisy data.
2. **Dynamic Data Integration**:
   - Allow real-time updates to Pinecone embeddings when new data is uploaded.
3. **Multi-Language Support**:
   - Extend chatbot capabilities to support financial queries in multiple languages.

---

## **Contributors**
- **Developer**: Milan
- **GitHub**: https://github.com/milan903575/

---

