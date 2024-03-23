from flask import Flask, render_template, request, jsonify
from summarizer_utils import summarize_with_bart
import pdfplumber

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_word_count', methods=['POST'])
def get_word_count():
    text_content = request.form.get('text', None)
    file = request.files.get('file', None)

    if not text_content and not file:
        return jsonify(error='No input provided')

    elif text_content and file:
        return jsonify(error='Both PDF and text fields are filled. Please provide only one input')

    elif text_content:
        # If text content is provided, calculate the word count and return it
        word_count_before = len(text_content.split())
        return jsonify(word_count_before=word_count_before)

    elif file:
        # If a file is uploaded, read its text content and then calculate the word count
        with pdfplumber.open(file) as pdf:
            text_content = ""
            for page in pdf.pages:
                text_content += page.extract_text()
        word_count_before = len(text_content.split())
        return jsonify(word_count_before=word_count_before)

@app.route('/summarize', methods=['POST'])
def summarize():
    text_content = request.form.get('text', None)
    file = request.files.get('file', None)

    if not text_content and not file:
        return jsonify(error='No input provided')

    elif text_content and file:
        return jsonify(error='Both PDF and text fields are filled. Please provide only one input')

    elif text_content:
        # If text content is provided, directly pass it to the summarizer function
        summary, word_count_after = summarize_with_bart(text_content)
        return jsonify({'summary': summary, 'word_count_after': word_count_after})

    elif file:
        # If a file is uploaded, read its text content and then pass it to the summarizer function
        with pdfplumber.open(file) as pdf:
            text_content = ""
            for page in pdf.pages:
                text_content += page.extract_text()
        summary, word_count_after = summarize_with_bart(text_content)
        return jsonify({'summary': summary, 'word_count_after': word_count_after})

if __name__ == '__main__':
    app.run(debug=True)
