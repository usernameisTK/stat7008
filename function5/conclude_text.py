"""
Prediction
"""
from transformers import pipeline, AutoTokenizer
import textwrap
# from keybert import KeyBERT
# import jieba
import pandas as pd
import torch
import time
import os

""" 生成摘要 """
def generate_summary(text, max_length=1024, max_new_tokens=150):
    # 检查是否有可用的 GPU
    device = 0 if torch.cuda.is_available() else -1  # -1 表示使用 CPU
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", revision="a4f8f3e", device=device)

    # 将长文本分割为多个部分
    wrapped_text = textwrap.wrap(text, width=max_length)
    total_parts_num = len(wrapped_text)
    summaries = []
    # print(f"Start Summarying.")
    for i, part in enumerate(wrapped_text):
        # print(f"Summarying {i+1} part/ Totally {total_parts_num} parts")
        summary = summarizer(part, max_new_tokens=max_new_tokens, do_sample=False)  # 只使用 max_new_tokens
        summaries.append(summary[0]['summary_text'])

    # print('Joining')
    # 合并所有摘要
    final_summary = ' '.join(summaries)
    return final_summary

"""总结文本"""
def conclude(text):
    # 总结文本
    result = generate_summary(text, max_length=1024, max_new_tokens=150)

    # 计算总结后文本的单词数量
    while len(result.split()) > 512:
        result = generate_summary(result, max_length=1024, max_new_tokens=150)

    return result

"""将总结的写入csv"""
def conclude_update(company_name, txt_name):

    path = os.path.join("..", "extracted_text", txt_name)  # 上一级目录中的 extracted_text 文件夹
    print("The filename is:" + txt_name)
    with open(path, 'r', encoding='utf-8') as file:
        text = file.read()

    # 定义输出的文件路径
    csv_file_path = "esg.csv"

    # 读取 CSV 文件
    df = pd.read_csv(csv_file_path, encoding='ISO-8859-1')

    # 总结文本
    result = conclude(text)

    # 更新特定公司的 ESG Report 列
    df.loc[df['Name'] == company_name, 'ESG Report'] = result

    # 保存更新后的 DataFrame 回 CSV 文件
    df.to_csv(csv_file_path, index=False)

    print(f"{company_name}已更新。")

"""批量更新csv"""
def update_csv():
    # 导入文件。 raw.xlsx是初始文件路径。esg.csv是总结文本并导入后的路径

    company_name = pd.read_csv("raw.csv", encoding='ISO-8859-1')['Name']

    start_time = time.time()

    for name in company_name:
        txt_path = name +'.txt'
        conclude_update(name, txt_path)
        end_time = time.time()
        print(f'{name} Finished. Time:{(end_time - start_time)//60}min {(end_time - start_time)%60}s')

"""Main function"""
if __name__ == "__main__":
    update_csv()