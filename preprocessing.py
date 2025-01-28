import pdfplumber
import pytesseract
from pytesseract import image_to_string
from pdf2image import convert_from_path
import pandas as pd
from transformers import pipeline

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
poppler_path = r"C:\poppler-24.08.0\Library\bin"

def extract_tables_from_pdf(pdf_path):
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_tables = page.extract_tables()
            for table in page_tables:
                df = pd.DataFrame(table)
                if not df.empty:
                    # Use the first row as column headers and remove it from the data
                    df.columns = df.iloc[0]  # Set the first row as header
                    df = df[1:]  # Drop the header row from the data
                    df.reset_index(drop=True, inplace=True)  # Reset index
                    tables.append(df)
    return tables


def extract_text_from_pdf(pdf_path):
    text = []
    images = convert_from_path(pdf_path, poppler_path=poppler_path)
    for image in images:
        page_text = image_to_string(image)
        text.append(page_text)
    return text

def analyze_text_for_profit_loss(text):
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=200, min_length=50, do_sample=False)
        summaries.append(summary[0]["summary_text"])
    return " ".join(summaries)

def create_profit_loss_table(tables, text_summary):
    # Initialize an empty DataFrame
    profit_loss_table = pd.DataFrame()
    
    for table in tables:
        if "profit" in table.to_string().lower() or "loss" in table.to_string().lower():
            profit_loss_table = pd.concat([profit_loss_table, table], ignore_index=True)
    
    # Dynamically add the 'Insights' column
    profit_loss_table["Insights"] = text_summary
    
    return profit_loss_table


def process_large_pdf(pdf_path):
    print("Extracting tables...")
    tables = extract_tables_from_pdf(pdf_path)
    print(f"Extracted {len(tables)} tables.")

    print("Extracting text...")
    text = extract_text_from_pdf(pdf_path)
    print(f"Extracted {len(text)} pages of text.")

    print("Analyzing text for profit and loss insights...")
    try:
        summary = analyze_text_for_profit_loss(" ".join(text))
    except Exception as e:
        print(f"Error during text analysis: {e}")
        summary = ""

    print("Generating profit and loss table...")
    profit_loss_table = create_profit_loss_table(tables, summary)
    profit_loss_table.to_csv("profit_loss_table.csv", index=False)
    print("Profit and Loss Table saved to 'profit_loss_table.csv'.")
    return profit_loss_table

if __name__ == "__main__":
    pdf_path = "M:\\Gen_ChatBot\\sample_test.pdf"
    profit_loss_table = process_large_pdf(pdf_path)
    print(profit_loss_table)
