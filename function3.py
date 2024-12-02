import os
import pdfplumber
from transformers import pipeline

# Function to extract text from a single PDF
def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        print(f"File {pdf_path} doesn't exist!")
        return

    pdf_name = os.path.basename(pdf_path)
    txt_name = os.path.splitext(pdf_name)[0] + ".txt"

    # Output folder for extracted text files
    output_folder = "extracted_text"
    os.makedirs(output_folder, exist_ok=True)
    txt_path = os.path.join(output_folder, txt_name)

    extracted_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                extracted_text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return None

    try:
        with open(txt_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(extracted_text)
        print(f"Extracted text saved to: {txt_path}")
        return txt_path
    except Exception as e:
        print(f"Error saving text to file: {e}")
        return None

# Function to batch extract text from all PDFs in a folder
def batch_extract_from_folder(folder_path):
    txt_files = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_file_path = os.path.join(folder_path, filename)
            txt_path = extract_text_from_pdf(pdf_file_path)
            if txt_path:
                txt_files.append(txt_path)
    print('Finished transforming PDFs to text files.')
    return txt_files

# Function to split text into chunks
def split_into_chunks(text, chunk_size=512):
    words = text.split()
    chunks = [
        " ".join(words[i : i + chunk_size])
        for i in range(0, len(words), chunk_size)
    ]
    return chunks

# Function to classify sentiment of a text file
def classify_sentiments(text_file_path, sentiment_model):
    try:
        with open(text_file_path, "r", encoding="utf-8") as file:
            content = file.read()
            if not content.strip():
                print(f"No text found in {text_file_path}. Skipping.")
                return

        # Split content into chunks
        chunks = split_into_chunks(content, chunk_size=512)

        # Classify each chunk and aggregate results
        all_predictions = []
        for chunk in chunks:
            predictions = sentiment_model(chunk)
            all_predictions.extend(predictions)

        # Print or process the predictions
        print(f"Sentiment predictions for {text_file_path}:")
        for idx, prediction in enumerate(all_predictions):
            print(f"Chunk {idx+1}: {prediction}")
    except Exception as e:
        print(f"Error processing {text_file_path}: {e}")

# Main function
def main():
    # Specify the folder containing the PDF files
    pdf_folder_path = "original_pdf"

    # Extract text from all PDFs in the folder
    txt_files = batch_extract_from_folder(pdf_folder_path)

    # Load pre-trained sentiment analysis model
    sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

    # Classify sentiments for each extracted text file
    for txt_file in txt_files:
        classify_sentiments(txt_file, sentiment_model)

# Run the script
if __name__ == "__main__":
    main()
