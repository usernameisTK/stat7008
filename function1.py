import os
import jieba
import fitz
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud


# 使用 TF-IDF 提取关键词的函数. 也可以用其他算法提取关键词
def extract_keywords_tfidf(text, top_n=10):
    # 创建 TF-IDF 向量化器
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([text])

    # 获取词汇和对应的 TF-IDF 值
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.toarray()[0]

    # 获取排序后的关键词
    sorted_indices = np.argsort(tfidf_scores)[::-1]
    top_keywords = [(feature_names[i], tfidf_scores[i]) for i in sorted_indices[:top_n]]

    return top_keywords


# 生成词云的函数
def generate_wordcloud(keywords):
    word_freq = {keyword: score for keyword, score in keywords}

    # 生成词云
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)

    # 显示词云
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # 关闭坐标轴
    plt.show()

def keywords(filename):
    path = "extracted_text/" + filename
    print("The filename is:" + filename)
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()

    keywords = extract_keywords_tfidf(content, top_n=20)  # 提取更多关键词
    generate_wordcloud(keywords)
    print(keywords)
    return keywords
