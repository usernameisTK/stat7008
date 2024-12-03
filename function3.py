import os
from transformers import pipeline

class TextExtractor:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def get_text_files(self):
        """Returns a list of .txt files in the specified folder."""
        if not os.path.exists(self.folder_path):
            raise FileNotFoundError(f"Folder {self.folder_path} does not exist.")
        
        txt_files = [
            os.path.join(self.folder_path, file)
            for file in os.listdir(self.folder_path)
            if file.endswith(".txt")
        ]
        
        if not txt_files:
            raise FileNotFoundError(f"No text files found in {self.folder_path}.")
        
        return txt_files


class SentimentAnalyzer:
    def __init__(self):
        # Load a pre-trained sentiment analysis model
        self.model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

    def split_into_chunks(self, text, chunk_size=512):
        """Split text into chunks of a specified size."""
        words = text.split()
        chunks = [
            " ".join(words[i : i + chunk_size])
            for i in range(0, len(words), chunk_size)
        ]
        return chunks

    def classify_sentiments(self, text_file_path):
        """Classify the sentiment of text in a file."""
        try:
            with open(text_file_path, "r", encoding="utf-8") as file:
                content = file.read()
                if not content.strip():
                    print(f"No text found in {text_file_path}. Skipping.")
                    return

            # Split content into chunks
            chunks = self.split_into_chunks(content)

            # Classify each chunk and aggregate results
            all_predictions = []
            for chunk in chunks:
                predictions = self.model(chunk)
                all_predictions.extend(predictions)

            # Print or process the predictions
            print(f"Sentiment predictions for {text_file_path}:")
            for idx, prediction in enumerate(all_predictions):
                print(f"Chunk {idx+1}: {prediction}")
        except Exception as e:
            print(f"Error processing {text_file_path}: {e}")


class ESGSentimentProcessor:
    def __init__(self, text_folder):
        self.text_folder = text_folder
        self.text_extractor = TextExtractor(text_folder)
        self.sentiment_analyzer = SentimentAnalyzer()

    def process(self):
        """Process all text files in the specified folder."""
        try:
            # Get all .txt files from the folder
            txt_files = self.text_extractor.get_text_files()

            # Analyze sentiment for each file
            for txt_file in txt_files:
                self.sentiment_analyzer.classify_sentiments(txt_file)
        except Exception as e:
            print(f"Error: {e}")


# Run the script
if __name__ == "__main__":
    # Specify the folder containing the extracted text files
    txt_folder_path = "extracted_text"  # Replace with your actual folder path

    # Initialize and run the sentiment processor
    processor = ESGSentimentProcessor(txt_folder_path)
    processor.process()
