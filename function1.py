# import os
# import jieba
# import fitz
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud


# use TF-IDF to extract keywords
def extract_keywords_tfidf(text, top_n=10):
    # create the transform
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([text])

    # get the feature names
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.toarray()[0]

    # sort the keywords based on their scores
    sorted_indices = np.argsort(tfidf_scores)[::-1]
    top_keywords = [(feature_names[i], tfidf_scores[i]) for i in sorted_indices[:top_n]]

    return top_keywords


# generate word cloud
def generate_wordcloud(keywords):
    word_freq = {keyword: score for keyword, score in keywords}

    # create the word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)

    # plot the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

def keywords(filename):
    path = "extracted_text/" + filename
    print("The filename is:" + filename)
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()

    # extract keywords using TF-IDF
    keywords = extract_keywords_tfidf(content, top_n=20)  
    generate_wordcloud(keywords)
    print(keywords)
    return keywords
