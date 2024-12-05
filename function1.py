import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import matplotlib.pyplot as plt
from wordcloud import WordCloud

nltk.download('stopwords')
nltk.download('punkt')

# Function to fetch file content from GitHub
def fetch_github_file_content(username, repository, filepath):
    url = f'https://api.github.com/repos/{username}/{repository}/contents/{filepath}'
    response = requests.get(url)
    
    if response.status_code == 200:
        content = response.json().get('content')
        if content:
            return base64.b64decode(content).decode('utf-8')
    
    return None

# Function to extract keywords using TF-IDF
def extract_keywords_tfidf(text, top_n=10):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.toarray()[0]
    sorted_indices = tfidf_scores.argsort()[::-1]
    top_keywords = [(feature_names[i], tfidf_scores[i]) for i in sorted_indices[:top_n]]
    return top_keywords

# Function to generate word cloud from keywords
def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

# Function to analyze text file with LDA
def analyze_text_file_with_lda(text):
    stop_words = set(stopwords.words('english'))
    words = [word.lower() for word in word_tokenize(text) if word.isalnum() and word.lower() not in stop_words]
    
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(words)
    
    lda = LatentDirichletAllocation(n_components=5, random_state=42)
    lda.fit(X)
    
    top_keywords = [(vectorizer.get_feature_names_out()[i] for i in topic.argsort()[:-6:-1]) for topic in lda.components_]
    return top_keywords

# Function to analyze text file using different methods and return results
def analyze_text_file(filename):
    path = os.path.join(os.getcwd(), filename)
    print("Analyzing file:", filename)
    
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    tfidf_keywords = extract_keywords_tfidf(content)
    generate_wordcloud(content)
    lda_keywords = analyze_text_file_with_lda(content)
    
    return tfidf_keywords, lda_keywords

# Get the current working directory
current_directory = os.getcwd()

# Get a list of all files in the current working directory
file_names = [f for f in os.listdir(current_directory) if os.path.isfile(os.path.join(current_directory, f))]

# Iterate over each file in the working directory, analyze the file, and print the results
for filename in file_names:
    tfidf_keywords, lda_keywords = analyze_text_file(filename)
    print("File:", filename)
    print("TF-IDF Keywords:", tfidf_keywords)
    print("LDA Keywords:", lda_keywords)
    print("-------------------------------------------------")
