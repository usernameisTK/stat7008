import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from textblob import TextBlob

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

# Main function to run the sentiment analysis and generate the outputs
def run_sentiment_analysis():
    # Run the batch sentiment analysis
    sentiment_results = batch_sentiment_analysis(extracted_text_folder)

    # Output the results to a JSON file
    output_file_path = "sentiment_analysis_results.json"
    with open(output_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(sentiment_results, json_file, ensure_ascii=False, indent=4)

    # Load sentiment analysis results
    with open(output_file_path, 'r', encoding='utf-8') as json_file:
        sentiment_results = json.load(json_file)

    # Flatten the sentiment results into a DataFrame for easier analysis and visualization
    data = []
    for filename, sentiment_data in sentiment_results.items():
        for entry in sentiment_data:
            data.append({
                "company": filename,
                "text": entry["text"],
                "sentiment": entry["sentiment"],
                "polarity": entry["polarity"]
            })

    df = pd.DataFrame(data)

    # 2. **Summary Table**: Show a table with sentiment analysis results
    print(df.head())  # Display the first few rows for verification

    # 3. **Sentiment Distribution**: Plot a bar chart of sentiment distribution
    sentiment_counts = df['sentiment'].value_counts()

    # Matplotlib Bar Plot for sentiment distribution
    plt.figure(figsize=(8, 5))
    sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, hue=sentiment_counts.index, palette="coolwarm")
    plt.title('Sentiment Distribution')
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    plt.show()

    # Plotly Visualization for Interactive Charts
    fig = px.bar(sentiment_counts, x=sentiment_counts.index, y=sentiment_counts.values, 
                 labels={'x': 'Sentiment', 'y': 'Count'}, title='Sentiment Distribution')
    fig.show()

    # 4. **Sentiment by Report (Company)**: Compare sentiment across different reports (companies)
    sentiment_by_company = df.groupby(['company', 'sentiment']).size().unstack().fillna(0)
    sentiment_by_company.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='viridis')
    plt.title('Sentiment by Company Report')
    plt.xlabel('Company')
    plt.ylabel('Count')
    plt.xticks(rotation=90)
    plt.show()

