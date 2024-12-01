import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import Trainer, TrainingArguments
import torch
from torch.utils.data import Dataset
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# 检查CUDA可用性
if torch.cuda.is_available():
    device = "cuda"
    print("GPU可用，训练将在GPU上进行。")
else:
    device = "cpu"
    print("GPU不可用，训练将在CPU上进行。")

# 1. 读取数据
df = pd.read_csv('esg.csv', encoding='ISO-8859-1')
texts = df['ESG Report'].tolist()
labels = df['ESG Rating'].tolist()

# 2. 编码类别
label_encoder = LabelEncoder()
labels_encoded = label_encoder.fit_transform(labels)

# 3. 分割数据集
train_texts, val_texts, train_labels, val_labels = train_test_split(texts, labels_encoded, test_size=0.2, random_state=42)

# 4. 使用BERT tokenizer

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# 5. 创建Dataset类
class TextDataset(Dataset):
    def __init__(self, texts, labels):
        self.encodings = tokenizer(texts, truncation=True, padding=True, max_length=512)
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

def compute_metrics(pred):
    labels = pred.label_ids  # 获取真实标签
    preds = pred.predictions.argmax(-1)  # 获取模型预测的类别
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='weighted')  # 计算精确率、召回率和F1-score
    acc = accuracy_score(labels, preds)  # 计算准确率
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }

# 6. 准备数据集
train_dataset = TextDataset(train_texts, train_labels)
val_dataset = TextDataset(val_texts, val_labels)

# 7. 加载BERT模型
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(label_encoder.classes_))

# 8. 设置训练参数
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=80,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    evaluation_strategy="epoch",
    save_strategy="no",               # 不保存模型
)

# 9. 创建Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=compute_metrics,
)

# 10. 训练模型
trainer.train()

# 11. 进行预测
predictions = trainer.predict(val_dataset)
predicted_labels = predictions.predictions.argmax(-1)

# 12. 输出预测结果
print("预测标签:", label_encoder.inverse_transform(predicted_labels))