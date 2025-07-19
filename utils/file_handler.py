# skill_validation_system/utils/file_handler.py

import os
import json
import PyPDF2
import docx

def save_file(file, upload_folder):
    """
    Saves an uploaded file to the specified folder, ensuring the folder exists.

    Args:
        file: The file object from the Flask request.
        upload_folder (str): The path to the folder where the file will be saved.

    Returns:
        str: The full path to the saved file.
    """
    # Ensure the target directory exists. If not, create it.
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    # Construct the full file path and save the file
    filepath = os.path.join(upload_folder, file.filename)
    file.save(filepath)
    return filepath

def read_file_content(filepath):
    """
    Reads the text content from a given file, supporting PDF (.pdf) and Word (.docx) formats.

    Args:
        filepath (str): The path to the file.

    Returns:
        str: The extracted text content of the file, or an empty string if the format is unsupported or an error occurs.
    """
    content = ""
    try:
        # Check the file extension to use the correct library
        if filepath.lower().endswith(".pdf"):
            with open(filepath, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                # Extract text from each page
                for page in reader.pages:
                    content += page.extract_text() or ""
        elif filepath.lower().endswith(".docx"):
            doc = docx.Document(filepath)
            # Extract text from each paragraph
            for para in doc.paragraphs:
                content += para.text + "\n"
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return ""
    return content

def read_json(filepath):
    """
    Reads and parses data from a JSON file.

    Args:
        filepath (str): The path to the JSON file.

    Returns:
        list or dict: The data from the JSON file. Returns an empty list if the file doesn't exist.
    """
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading JSON from {filepath}: {e}")
        return []

def write_json(filepath, data):
    """
    Writes Python data (list or dict) to a JSON file with indentation.

    Args:
        filepath (str): The path to the JSON file.
        data (list or dict): The data to write.
    """
    try:
        # Ensure the directory exists before writing
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Error writing JSON to {filepath}: {e}")
