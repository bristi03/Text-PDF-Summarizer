from flask import Flask, render_template, request, jsonify
from summarizer_utils import summarize_with_bert
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    text_content = request.form.get('text', None)
    file = request.files.get('file', None)

    if not text_content and not file:
        return jsonify('No input provided')
    elif text_content and file:
        return jsonify('Both PDF and text fields are filled. Please provide only one input')

    elif text_content:
        summary, word_count_before, word_count_after = summarize_with_bert(text_content)
        return jsonify({'summary': summary, 'word_count_before': word_count_before, 'word_count_after': word_count_after})
    elif file:
        summary, word_count_before, word_count_after = summarize_with_bert(file)
        return jsonify({'summary': summary, 'word_count_before': word_count_before, 'word_count_after': word_count_after})
    
if __name__ == '__main__':
    app.run(debug=True)
