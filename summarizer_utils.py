from summarizer import Summarizer
import pdfplumber
import io

def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def summarize_with_bert(input_content):
    bert_model = Summarizer()

    if isinstance(input_content, io.BytesIO):  # Check if the input is a PDF file
        text = extract_text_from_pdf(input_content)
    else:
        text = input_content

    # Calculate word count before summarization
    word_count_before = len(text.split())

    # Use BERT for extractive summarization
    summary = bert_model(text)

    # Calculate word count after summarization
    word_count_after = len(summary.split())

    return summary, word_count_before, word_count_after
