import os
import pdfplumber

def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        print(f"file {pdf_path} doesn't exist!")
        return

    pdf_name = os.path.basename(pdf_path)
    txt_name = os.path.splitext(pdf_name)[0] + ".txt"

    # output folder
    output_folder = "extracted_text"
    os.makedirs(output_folder, exist_ok=True)
    txt_path = os.path.join(output_folder, txt_name)

    extracted_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                extracted_text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error: {e}")
        return


    try:
        cleaned_text = clean_text(extracted_text)
        with open(txt_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(cleaned_text)
        print(f"File saved to: {txt_path}")
    except Exception as e:
        print(f"Error: {e}")

"""批量更新，输入初始数据所在文件夹:pdf_folder_path = 'original_pdf' """
def batch_extract_from_folder(folder_path):
    print('Start transforming...')
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_file_path = os.path.join(folder_path, filename)
            extract_text_from_pdf(pdf_file_path)
    print('Finish transforming.')

# Specify the folder containing the PDF files
pdf_folder_path = "original_pdf"
batch_extract_from_folder(pdf_folder_path)



import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer




def clean_text(text):

    # 1. remove non-alphabetic characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # 2. convert to lowercase
    text = text.lower()
    
    # 3. tokenize the text
    words = word_tokenize(text)
    
    # 4. remove stop words
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    
    # 5. lemmatization
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    
    # 6. remove empty strings
    words = [word for word in words if word.strip() != '']
    
    # 7. join the words back into a full text
    cleaned_text = ' '.join(words)
    
    return cleaned_text
