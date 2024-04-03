import os
import json
import fitz  # PyMuPDF
from docx import Document
import re
import textract

with open('config.json', 'r') as json_file:
    config = json.load(json_file)

def read_pdf(file_path):
    """Reads a PDF file and returns its text content."""
    text = ''
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
        text = text.strip()
        text = ''.join(char for char in text if 32 <= ord(char) <= 126)
        text = re.sub(' +', ' ', text)
        text = re.sub('__+', '_', text)
        text = re.sub(r'^\d+', '', text)
    return text

def read_docx(file_path):
    """Reads a DOCX file and returns its text content."""
    doc = Document(file_path)
    text = " ".join([paragraph.text for paragraph in doc.paragraphs])
    text = text.strip()
    text = ''.join(char for char in text if 32 <= ord(char) <= 126)
    text = re.sub(' +', ' ', text)
    text = re.sub('__+', '_', text)
    text = re.sub(r'^\d+', '', text)
    return text

def read_doc(file_path):
    """Reads a DOC file and returns its text content using textract."""
    text = textract.process(file_path).decode('utf-8')
    text = text.strip()
    text = ''.join(char for char in text if 32 <= ord(char) <= 126)
    text = re.sub(' +', ' ', text)
    text = re.sub('__+', '_', text)
    text = re.sub(r'^\d+', '', text)
    return text

def process_folder(folder_path, output_folder):
    """Processes each file in the folder and creates a JSON file with their contents."""
    contents = {}
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith('.pdf'):
            print(f'Reading PDF: {file_path} added.')
            contents[filename] = read_pdf(file_path)
        elif filename.endswith('.docx'):
            print(f'Reading DOCX: {file_path} added.')
            contents[filename] = read_docx(file_path)
        elif filename.endswith('.doc'):
            print(f'Reading DOC: {file_path} added.')
            contents[filename] = read_doc(file_path)
            
    json_filename = os.path.basename(folder_path) + '.json'
    with open(os.path.join(output_folder, json_filename), 'w') as json_file:
        json.dump(contents, json_file, indent=4, ensure_ascii=False)

def main(root_folder):
    output_folder = os.path.join(root_folder, 'output_jsons')
    os.makedirs(output_folder, exist_ok=True)
    
    for root, dirs, files in os.walk(root_folder):
        if root == root_folder:
            continue

        process_folder(root, output_folder)
    
if __name__ == '__main__':
    root_folder = config['resume_path']
    main(root_folder)
    os.remove(config['json_path'] + "\\output_jsons.json")
