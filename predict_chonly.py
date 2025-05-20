from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 设置设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 加载模型函数
def load_models(model_paths):
    models = {}
    for dimension, path in model_paths.items():
        model = AutoModelForSequenceClassification.from_pretrained(path, num_labels=2)
        model.to(device)
        models[dimension] = model
    return models

# 预处理文本
def preprocess_text(text):
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# 预测函数（返回百分比置信度并格式化输出）
def predict_mbti(text, models, tokenizer):
    processed_text = preprocess_text(text)

    encoding = tokenizer(
        processed_text,
        add_special_tokens=True,
        max_length=512,
        padding='max_length',
        truncation=True,
        return_tensors='pt'
    )

    input_ids = encoding['input_ids'].to(device)
    attention_mask = encoding['attention_mask'].to(device)

    dimension_results = {}
    dimension_probs = {}

    for dim, model in models.items():
        model.eval()
        with torch.no_grad():
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=1)
            pred = torch.argmax(logits, dim=1).item()
            dimension_results[dim] = pred
            dimension_probs[dim] = int(probs[0][pred].item() * 100)

    # 构建MBTI类型
    mbti_type = ""
    mbti_type += "I" if dimension_results['IE'] == 0 else "E"
    mbti_type += "N" if dimension_results['NS'] == 0 else "S"
    mbti_type += "T" if dimension_results['TF'] == 0 else "F"
    mbti_type += "J" if dimension_results['JP'] == 0 else "P"

    # 格式化输出
    mbti_output = f"预测的MBTI类型: {mbti_type}；"
    mbti_output += f"{'I' if dimension_results['IE']==0 else 'E'}（置信度 {dimension_probs['IE']}%）"
    mbti_output += f"{'N' if dimension_results['NS']==0 else 'S'}（置信度 {dimension_probs['NS']}%）"
    mbti_output += f"{'T' if dimension_results['TF']==0 else 'F'}（置信度 {dimension_probs['TF']}%）"
    mbti_output += f"{'J' if dimension_results['JP']==0 else 'P'}（置信度 {dimension_probs['JP']}%）"

    return mbti_output

# 获取嵌入层贡献度（排除包含“我”的词、短词、以“的”开头的短词）
def get_embedding_contributions(input_ids, attention_mask, model, tokenizer):
    embedding_layer = model.get_input_embeddings()
    embeddings = embedding_layer(input_ids)
    
    word_contributions = {}
    words = tokenizer.convert_ids_to_tokens(input_ids.squeeze().cpu().numpy())
    
    for i, word in enumerate(words):
        if (
            word not in tokenizer.all_special_tokens and
            "我" not in word and
            not (len(word) <= 3 and word.startswith("的")) and
            len(word) >= 2
        ):
            word_embedding = embeddings[0, i].cpu().detach().numpy()
            importance = np.linalg.norm(word_embedding)
            word_contributions[word] = importance
    
    # 获取贡献度最高的30个词汇
    top_30_words = sorted(word_contributions.items(), key=lambda x: x[1], reverse=True)[:30]
    return top_30_words

# 生成词云
def generate_wordcloud(top_contributing_words):
    word_freq = {word: contribution for word, contribution in top_contributing_words}

    # 设置中文字体路径，确保中文显示
    wordcloud = WordCloud(
        font_path="SimHei.ttf",  # 中文字体路径
        width=800, 
        height=400, 
        background_color='white'
    ).generate_from_frequencies(word_freq)

    # 显示词云
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

# 加载所有模型
def load_all_models():
    model_paths = {
        'IE': '../FuncCodes/predict_code/chinese & english/models/IE_model',
        'NS': '../FuncCodes/predict_code/chinese & english/models/NS_model',
        'TF': '../FuncCodes/predict_code/chinese & english/models/TF_model',
        'JP': '../FuncCodes/predict_code/chinese & english/models/JP_model'
    }
    tokenizer = AutoTokenizer.from_pretrained("../FuncCodes/predict_code/chinese & english/xlm-roberta-base")
    models = load_models(model_paths)
    return models, tokenizer

# 主函数进行预测
def main():
    models, tokenizer = load_all_models()

    test_texts = [
        "我为自己快速适应新环境的能力感到自豪。我在充满活力的环境中发挥出色，并喜欢冒险。我对自己的决策能力有信心，并天生善于机智应对。我还为自己强大的实践和解决问题的能力感到自豪。我在找到实际解决方案方面很机智和高效。此外，我非常重视自己与他人的容易沟通的能力。我有魅力，并且喜欢社交，这使得我能够与来自各个领域的人建立牢固的关系。"
    ]

    print("\n测试预测:")
    for text in test_texts:
        result = predict_mbti(text, models, tokenizer)
        print(f"文本片段: {text[:50]}...")
        print(result)
        print("-" * 60)

        # 获取嵌入层贡献度
        encoding = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
        input_ids = encoding['input_ids'].to(device)
        attention_mask = encoding['attention_mask'].to(device)
        
        top_embedding_words = get_embedding_contributions(input_ids, attention_mask, models['IE'], tokenizer)
        print("嵌入层贡献度最大的词汇: ")
        for word, importance in top_embedding_words:
            print(f"{word}: {importance}")

        # 生成词云
        generate_wordcloud(top_embedding_words)

        print("-" * 60)

if __name__ == "__main__":
    main()
