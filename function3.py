import os
from transformers import pipeline

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
    # Folder containing the extracted .txt files
    txt_folder_path = "extracted_text"

    # Verify the folder exists
    if not os.path.exists(txt_folder_path):
        print(f"Folder {txt_folder_path} does not exist.")
        return

    # List all .txt files in the folder
    txt_files = [
        os.path.join(txt_folder_path, file)
        for file in os.listdir(txt_folder_path)
        if file.endswith(".txt")
    ]

    if not txt_files:
        print(f"No text files found in {txt_folder_path}.")
        return

    # Load pre-trained sentiment analysis model
    sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

    # Classify sentiments for each .txt file
    for txt_file in txt_files:
        classify_sentiments(txt_file, sentiment_model)

# Run the script
if __name__ == "__main__":
    main()
