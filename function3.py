import os
from textblob import TextBlob
import json

# Path to the folder containing the extracted text files
extracted_text_folder = "extracted_text"

# Function to load text from a file
def load_text_from_file(txt_file_path):
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to perform sentiment analysis using TextBlob
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # Polarity score: -1 (negative) to 1 (positive)
    if polarity > 0:
        sentiment = 'positive'
    elif polarity < 0:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    return sentiment, polarity

# Function to analyze sentiments of ESG-related issues in a company's report
def analyze_esg_sentiment(txt_file_path):
    text = load_text_from_file(txt_file_path)
    
    # You may need to filter relevant ESG content, depending on how your data is structured
    esg_keywords = ['environmental', 'social', 'governance', 'sustainability', 'impact', 'csr', 'ethics']
    esg_text = []

    for line in text.split("\n"):
        if any(keyword in line.lower() for keyword in esg_keywords):
            esg_text.append(line)

    # If no ESG-related text found, skip the file
    if not esg_text:
        return None

    # Perform sentiment analysis on the ESG-related text
    sentiment_results = []
    for line in esg_text:
        sentiment, polarity = analyze_sentiment(line)
        sentiment_results.append({
            "text": line,
            "sentiment": sentiment,
            "polarity": polarity
        })

    return sentiment_results

# Function to analyze all text files in the folder
def batch_sentiment_analysis(extracted_text_folder):
    sentiment_analysis_results = {}

    for filename in os.listdir(extracted_text_folder):
        if filename.endswith(".txt"):
            txt_file_path = os.path.join(extracted_text_folder, filename)
            result = analyze_esg_sentiment(txt_file_path)
            if result:
                sentiment_analysis_results[filename] = result

    return sentiment_analysis_results

# Run the batch sentiment analysis
sentiment_results = batch_sentiment_analysis(extracted_text_folder)

# Output the results to a JSON file
output_file_path = "sentiment_analysis_results.json"
with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(sentiment_results, json_file, ensure_ascii=False, indent=4)

print(f"Sentiment analysis completed and saved to: {output_file_path}")
