# -*- coding: utf-8 -*-
"""
Created on Fri Jun 20 13:09:05 2025

@author: student
"""
import pandas as pd
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# 一、載入你標註好的 Excel
df = pd.read_excel('職缺人工標註樣本.xlsx')

# 二、資料預處理：合併職缺名稱與描述欄位
df['text'] = df['jobName'].fillna('') + ' ' + df['description'].fillna('')

# 三、定義特徵（X）與標籤（y）
X_text = df['text']
y = df['is_data_analysis_job']

# 四、定義中文分詞的 tokenizer
def jieba_tokenizer(text):
    return jieba.lcut(text)

# 五、TF-IDF 向量化（支援中文分詞）
vectorizer = TfidfVectorizer(tokenizer=jieba_tokenizer, max_features=1000)
X = vectorizer.fit_transform(X_text)


# 六、切分資料
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 七、訓練模型
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# 八、評估效果
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))


#九、(額外)模型最重視的關鍵詞（前 20 名）
import numpy as np

# 取得特徵重要性分數
importances = model.feature_importances_

# 抓出 TF-IDF 中的詞彙（注意：要用 get_feature_names_out）
words = vectorizer.get_feature_names_out()

# 取出前 20 個最重要的詞
top_indices = np.argsort(importances)[::-1][:20]
top_words = [(words[i], round(importances[i], 4)) for i in top_indices]

# 輸出結果
print("🔍 模型最重視的前 20 個詞（根據 TF-IDF 權重 + 隨機森林學習）：")
for i, (word, score) in enumerate(top_words, 1):
    print(f"{i}. {word}: {score}")



