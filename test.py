import pandas as pd

# run:  pip install -r requirements.txt

data = pd.read_csv('SP_500_ESG_Risk_Ratings.csv')

# print(data.head())
# print(data.info())


import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import re

# 下载 NLTK 数据资源（如果未下载过）
# nltk.download('punkt')
# nltk.download('punkt_tab')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('omw-1.4')

# 提取 description 列
description = data.iloc[:, 6]
print(description.head())


# 初始化工具
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# print(description[1])


# 定义文本预处理函数
def preprocess_text(text):
    # 2. 移除标点和非字母字符
    try:
        text = re.sub(f"[{string.punctuation}]", " ", text)  # 替换标点为空格
        text = re.sub(r'\d+', '', text)  # 移除数字
        # 1. 转小写
        text = text.lower()
        # 3. 分词
        tokens = word_tokenize(text)
        # 4. 移除停用词
        tokens = [word for word in tokens if word not in stop_words]
        # 5. 词形还原
        tokens = [lemmatizer.lemmatize(word) for word in tokens]
        # 6. 移除空白单词
        tokens = [word for word in tokens if word.strip()]
    except:
        print("error")
    return " ".join(tokens)  # 返回预处理后的文本

# 对整个列进行预处理
test=description[1:2]
processed_description = test.apply(preprocess_text)

# 查看前几行结果
# print(processed_description.head())


