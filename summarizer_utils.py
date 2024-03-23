from transformers import BartForConditionalGeneration, BartTokenizer
import pdfplumber
import io

def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def summarize_with_bart(input_content):
    bart_model = BartForConditionalGeneration.from_pretrained("bart_samsum_news_model")
    bart_tokenizer = BartTokenizer.from_pretrained("bart_samsum_news_model")

    #if isinstance(input_content, io.BytesIO):  # Check if the input is a PDF file
        #text = extract_text_from_pdf(input_content)
    #else:
    text = input_content

    # Tokenize the input text
    inputs = bart_tokenizer([text], max_length=1024, return_tensors='pt', truncation=True)

    # Generate the summary
    summary_ids = bart_model.generate(inputs['input_ids'], 
                                      num_beams=20,  # Increase the number of beams for better exploration
                                      length_penalty=2.0,  # Adjust the length penalty to encourage longer summaries
                                      max_length=500,  # Set a maximum length for the generated summary
                                      early_stopping=True)  # Enable early stopping to prevent overly long summaries
    summary = bart_tokenizer.decode(summary_ids[0], skip_special_tokens=True)


    # Calculate word count after summarization
    word_count_after = len(summary.split())

    return summary, word_count_after
