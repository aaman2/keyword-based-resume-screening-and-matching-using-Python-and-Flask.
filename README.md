# keyword based resume Screening matching using Python and Flask.
This code is a Flask application that performs keyword matching on uploaded resumes (in PDF or DOCX format) against specified keywords. Here's a breakdown of what each part of the code does:

Imports:

Imports necessary modules from Flask for web application functionality (Flask, request, jsonify, render_template).
Imports additional modules (fitz from PyMuPDF for PDF handling, docx for DOCX handling, nltk for natural language processing, and os for operating system operations).
Flask Setup:

Initializes a Flask application.
Sets up a route / that renders an index.html template (not shown in the provided code).
NLTK Setup:

Downloads necessary NLTK resources (punkt for tokenization and stopwords).
File Upload Handling:

Defines an UPLOAD_FOLDER where uploaded files (resumes) will be stored.
Creates the directory specified by UPLOAD_FOLDER if it does not exist.
Text Extraction Functions:

extract_text_from_pdf(file_path): Uses PyMuPDF (fitz) to extract text from a PDF file.
extract_text_from_docx(file_path): Uses docx module to extract text from a DOCX file.
extract_text(file_path): Determines the file type and calls the appropriate extraction function.
Keyword Search Functions:

keyword_search(text, keywords): Tokenizes the extracted text, converts tokens to lowercase, and counts occurrences of specified keywords.
score_keywords(keyword_counts, total_keywords_given): Calculates a percentage score based on how many of the specified keywords were found in the resume.
Flask Routes:

/: Renders an index.html template.
/search (POST method): Handles keyword search requests.
Checks if a file named 'resume' is uploaded.
Saves the uploaded resume file to the UPLOAD_FOLDER.
Extracts text from the uploaded resume using extract_text.
Performs keyword search using keyword_search.
Calculates score using score_keywords.
Returns JSON response containing the score and keyword counts.
Logs errors and exceptions.
Main Execution:

Starts the Flask application if this script is executed directly.
Purpose:
This Flask application serves a practical purpose where users can upload resumes, specify keywords, and receive a percentage score indicating how well the resume matches those keywords. It integrates file handling, text extraction from different formats (PDF, DOCX), natural language processing for keyword matching, and web interface using Flask.

Usage:
To use this application, you would typically run it on a server, navigate to the web interface, upload a resume file, enter keywords separated by commas, and submit the form to get a matching score. The application handles errors gracefully by logging them and returning appropriate error messages in JSON format.

Overall, it provides a basic yet effective mechanism for keyword-based resume screening and matching using Python and Flask.
