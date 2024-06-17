from flask import Flask, request, jsonify, render_template
import fitz  # PyMuPDF
import docx
import nltk
import os

app = Flask(__name__)

# Ensure nltk resources are available
nltk.download('punkt')
nltk.download('stopwords')

# Create the uploads directory if it doesn't exist
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text(file_path):
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension.lower() in ['.doc', '.docx']:
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file type")

def keyword_search(text, keywords):
    words = nltk.word_tokenize(text)
    words = [word.lower() for word in words if word.isalnum()]
    word_set = set(words)
    keyword_counts = {keyword.lower(): 1 if keyword.lower() in word_set else 0 for keyword in keywords}
    return keyword_counts

def score_keywords(keyword_counts, total_keywords_given):
    total_keywords_found = sum(keyword_counts.values())
    score = ((total_keywords_found / total_keywords_given)*100) if total_keywords_given > 0 else 0
    return score

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_keywords():
    if 'resume' not in request.files:
        app.logger.error('No file uploaded')
        return jsonify({"error": "No file uploaded"}), 400

    resume = request.files['resume']
    keywords = request.form['keywords'].split(',')

    file_path = os.path.join(UPLOAD_FOLDER, resume.filename)
    resume.save(file_path)

    try:
        text = extract_text(file_path)
        app.logger.info(f"Extracted text: {text[:100]}")  # Print first 100 characters of extracted text
        keyword_counts = keyword_search(text, keywords)
        app.logger.info(f"Keyword counts: {keyword_counts}")  # Print keyword counts
        score = score_keywords(keyword_counts, len(keywords))
    except Exception as e:
        app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(file_path)

    return jsonify({"Resume match percentage": score , "keyword_counts": keyword_counts })

if __name__ == '__main__':
    app.run(debug=True)
