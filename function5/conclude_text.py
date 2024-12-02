"""
Prediction
"""
from transformers import pipeline, AutoTokenizer
import textwrap
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
import time

import os


class TextDataset(Dataset):
    def __init__(self, csv_file, text_folder):
        self.df = pd.read_csv(csv_file, encoding='ISO-8859-1')
        self.text_folder = text_folder  # 存储文本文件的文件夹

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        company_name = self.df.iloc[idx]['Company Name']  # 获取公司名称
        txt_path = os.path.join(self.text_folder, f"{company_name}.txt")  # 构建文本文件路径

        # 读取文本文件内容
        with open(txt_path, 'r', encoding='utf-8') as file:
            text = file.read()

        return company_name, text

""" 生成摘要 """
def generate_summary(text, max_length=512, max_new_tokens=120):
    device = 0 if torch.cuda.is_available() else -1
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", revision="a4f8f3e", device=device)

    wrapped_texts = textwrap.wrap(text, width=max_length)
    summaries = []


    part_summaries = summarizer(wrapped_texts, max_new_tokens=max_new_tokens, do_sample=False)
    summaries.append(' '.join([summary['summary_text'] for summary in part_summaries]))

    return summaries[0]

"""总结文本"""
def conclude(text):
    result = generate_summary(text)

    while len(result.split()) > 512:
        result = generate_summary(result)

    return result

"""总结文本"""
def update_csv(csv_file, text_folder):
    dataset = TextDataset(csv_file, text_folder)
    dataloader = DataLoader(dataset, batch_size=1, shuffle=False)

    # 读取原始 ESG_Score_Conclusion.csv
    df = pd.read_csv(csv_file, encoding='ISO-8859-1')

    results = []
    start_time = time.time()
    # 遍历 DataLoader 中的每一项
    print("Start summarizing...")
    for company_name, text in dataloader:

        company_name = company_name[0]  # 因为批量大小为1，取第一个元素
        summary = conclude(text[0])  # 生成摘要

        # 更新 DataFrame 的第三列
        df.loc[df['Company Name'] == company_name, 'ESG Report Conclusion'] = summary

        # 保存更新后的 DataFrame 到 CSV
        df.to_csv(csv_file, index=False)

        end_time = time.time()
        total_time = end_time - start_time
        print(f"{company_name} has been summarized to {len(summary.split())} words! Total update time: {round(total_time//3600)}h {round(total_time//60)}min {round(total_time%60, 1)}s")

"""Main function"""
if __name__ == "__main__":
    csv_file = 'ESG_Score_Conclusion.csv'
    text_folder = '../extracted_text'
    update_csv(csv_file, text_folder)