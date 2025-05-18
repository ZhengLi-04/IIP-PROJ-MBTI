import time
import streamlit as st
import base64
from streamlit.components.v1 import html
import os
import torch
from transformers import BertForSequenceClassification, BertTokenizer
import re
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# 在文件开头添加中文检测函数
def contains_chinese(text):
    for char in text:
        if '\u4e00' <= char <= '\u9fff':
            return True
    return False

# 配置设置
MODEL_ROOT = "../FuncCodes/predict_code/500 words/models/"  # 模型根目录
DIMENSIONS = ['IE', 'NS', 'TF', 'JP']  # 四个维度
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 文本预处理函数
def preprocess_text(text):
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# 添加双语模型类
class BilingualMBTITester:
    def __init__(self):
        self.models = {}
        self.tokenizer = None
        self._load_models()

    def _load_models(self):
        model_paths = {
            'IE': '../FuncCodes/predict_code/chinese & english/models/IE_model',
            'NS': '../FuncCodes/predict_code/chinese & english/models/NS_model',
            'TF': '../FuncCodes/predict_code/chinese & english/models/TF_model',
            'JP': '../FuncCodes/predict_code/chinese & english/models/JP_model'
        }
        
        # 加载tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained("../FuncCodes/predict_code/chinese & english/xlm-roberta-base/")
        
        # 加载模型
        for dimension, path in model_paths.items():
            model = AutoModelForSequenceClassification.from_pretrained(path, num_labels=2)
            self.models[dimension] = model.to(DEVICE)
            print(f"成功加载双语模型 {dimension} 维度")
        print("所有双语模型加载完成！")

    def predict(self, text):
        processed_text = preprocess_text(text)
        
        encoding = self.tokenizer(
            processed_text,
            add_special_tokens=True,
            max_length=512,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )

        input_ids = encoding['input_ids'].to(DEVICE)
        attention_mask = encoding['attention_mask'].to(DEVICE)

        predictions = {}
        confidences = {}
        
        for dim, model in self.models.items():
            model.eval()
            with torch.no_grad():
                outputs = model(input_ids=input_ids, attention_mask=attention_mask)
                logits = outputs.logits
                probs = torch.softmax(logits, dim=1)
                pred = torch.argmax(logits, dim=1).item()
                confidence = int(probs[0][pred].item() * 100)
                
                predictions[dim] = pred
                confidences[dim] = confidence

        # 获取词语贡献度
        top_contributing_words = self._get_embedding_contributions(input_ids, attention_mask)
        
        return self._format_mbti(predictions), confidences, top_contributing_words

    def _get_embedding_contributions(self, input_ids, attention_mask):
        word_contributions = {}
        words = self.tokenizer.convert_ids_to_tokens(input_ids.squeeze().cpu().numpy())
        
        embedding_layer = self.models['IE'].get_input_embeddings()
        embeddings = embedding_layer(input_ids)
        
        for i, word in enumerate(words):
            if (word not in self.tokenizer.all_special_tokens and 
                "我" not in word and 
                not (len(word) <= 3 and word.startswith("的")) and 
                len(word) >= 2):
                word_embedding = embeddings[0, i].cpu().detach().numpy()
                importance = np.linalg.norm(word_embedding)
                word_contributions[word] = importance
        
        return sorted(word_contributions.items(), key=lambda x: x[1], reverse=True)[:5]

    def _format_mbti(self, predictions):
        type_map = {
            'IE': {0: 'I', 1: 'E'},
            'NS': {0: 'N', 1: 'S'},
            'TF': {0: 'T', 1: 'F'},
            'JP': {0: 'J', 1: 'P'}
        }
        return ''.join([type_map[dim][pred] for dim, pred in predictions.items()])
    
# MBTITester 类定义
class MBTITester:
    def __init__(self):
        self.models = {}
        self.tokenizer = None
        self._load_models()

    def _load_single_model(self, dimension):
        model_path = os.path.join(MODEL_ROOT, f"{dimension}_model")
        
        if not self.tokenizer:
            self.tokenizer = BertTokenizer.from_pretrained(
                model_path,
                config=os.path.join(model_path, "config.json"),
                tokenizer_config_file=os.path.join(model_path, "tokenizer_config.json"),
                vocab_file=os.path.join(model_path, "vocab.txt")
            )
        
        model = BertForSequenceClassification.from_pretrained(model_path, output_attentions=True)
        return model.to(DEVICE)

    def _load_models(self):
        for dim in DIMENSIONS:
            self.models[dim] = self._load_single_model(dim)
            print(f"成功加载 {dim} 维度模型")
        print("所有模型加载完成！")

    def predict(self, text):
        processed_text = preprocess_text(text)

        encoding = self.tokenizer(
            processed_text,
            add_special_tokens=True,
            max_length=512,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        ).to(DEVICE)

        predictions = {}
        confidences = {}
        word_contributions = {}

        with torch.no_grad():
            for dim, model in self.models.items():
                outputs = model(**encoding)
                logits = outputs.logits
                probs = torch.softmax(logits, dim=1)
                pred = torch.argmax(probs).item()
                confidence = int(probs[0][pred].item() * 100)

                predictions[dim] = pred
                confidences[dim] = confidence

                attention_weights = outputs.attentions
                word_contributions[dim] = self._compute_attention_contributions(attention_weights, encoding)

        total_word_contributions = self._aggregate_word_contributions(word_contributions)
        top_contributing_words = self._get_top_contributing_words(total_word_contributions)

        return self._format_mbti(predictions), confidences, top_contributing_words

    def _compute_attention_contributions(self, attention_weights, encoding):
        tokens = self.tokenizer.convert_ids_to_tokens(encoding['input_ids'][0].cpu().numpy())
        tokens = [token for token in tokens if token not in ['[CLS]', '[SEP]', '[PAD]']]
        word_contributions = {token: 0 for token in tokens}

        for layer in range(len(attention_weights)):
            for head in range(attention_weights[layer].shape[1]):
                attention_map = attention_weights[layer][0, head].detach().cpu().numpy()
                for i, token in enumerate(tokens):
                    word_contributions[token] += np.sum(attention_map[i, :])
        
        return word_contributions

    def _aggregate_word_contributions(self, word_contributions):
        total_word_contributions = {}
        for dim, contributions in word_contributions.items():
            for word, contribution in contributions.items():
                if word not in total_word_contributions:
                    total_word_contributions[word] = 0
                total_word_contributions[word] += contribution
        return total_word_contributions

    def _get_top_contributing_words(self, total_word_contributions, top_n=5):
        top_contributing_words = sorted(total_word_contributions.items(), key=lambda item: item[1], reverse=True)[:top_n]
        return top_contributing_words

    def _format_mbti(self, predictions):
        type_map = {
            'IE': {0: 'I', 1: 'E'},
            'NS': {0: 'N', 1: 'S'},
            'TF': {0: 'T', 1: 'F'},
            'JP': {0: 'J', 1: 'P'}
        }
        return ''.join([type_map[dim][pred] for dim, pred in predictions.items()])

# 初始化模型（确保只初始化一次）
if 'tester' not in st.session_state:
    st.session_state.tester = MBTITester()
if 'bilingual_tester' not in st.session_state:
    st.session_state.bilingual_tester = BilingualMBTITester()

def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

st.markdown("""
    <style>
    [data-testid="stImage"] {
        margin-top: -60px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.image("images/beamer.svg",use_container_width=True)

# 添加响应式文本样式
st.markdown(
    """
    <style>
    button[kind="header"] {
        display: none;
    }
    * {
        font-family: "PingFang SC", "Source Sans Pro", -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    .mbtitest-page-bigtitle {
        font-size: calc(36px + 0.25vw) !important;
        margin-bottom: calc(0px + 0vw) !important;
        font-weight: bold !important;
        margin-top: calc(-20px + 0.25vw) !important;
    }
    .mbtitest-page-title {
        font-size: calc(16px + 0.25vw) !important;
        margin-bottom: calc(8px + 0.25vw) !important;
        font-weight: bold !important;
    }
    .mbtitest-page-type {
        margin-top: calc(8px + 0.25vw) !important;
        font-size: calc(14px + 0.25vw) !important;
        margin-bottom: calc(8px + 0.25vw) !important;
        font-weight: bold !important;
    }
    .mbtitest-page-text {
        font-size: calc(12px + 0.25vw) !important;
        margin-bottom: calc(12px + 0.25vw) !important;
    }
    
    .mbtitest-card {
        background: white;
        border-radius: 20px;
        padding: 20px 20px 10px 20px;
        margin: 10px 10px 10px 10px;
        transition: all 0.3s ease;
        border: 1.5px solid #eee;
    }
    
    .mbtitest-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .mbtitest-page-typetitle {
        font-size: calc(14px + 0.25vw) !important;
        font-weight: bold !important;
        color: #333;
        margin-bottom: 1px !important;
        text-align: center;
    }
    .mbtitest-page-typetitle2 {
        font-size: calc(13px + 0.25vw) !important;
        font-weight: bold !important;
        color: #333;
        margin-bottom: 15px !important;
        text-align: center;
    }
    .mbtitest-card-image {
        text-align: center;
        margin: 10px 0;
    }
    
    .mbtitest-card-text {
        font-size: calc(11px + 0.25vw) !important;
        color: #666;
        line-height: 1.6;
        margin: 10px 10px 10px 10px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<p class="mbtitest-page-bigtitle">🎯 MBTI 性格预测</p>', unsafe_allow_html=True)
st.caption("🚀 通过一段文本，MBTInsight可以自动预测出你的MBTI性格类型。")

# 文本输入区域
user_input = st.text_area(
    "在这里输入你想要分析的文本:",
    height=150,
    placeholder="请输入至少100个字符的英文文本..."
)

# 根据输入自动选择默认模型
default_model_index = 1 if contains_chinese(user_input) else 0

# 模型选择
model_type = st.selectbox(
    "选择预测模型:",
    ["英文版模型 🇬🇧", "双语版模型 🇨🇳 🇬🇧"],
    index=default_model_index
)

# 根据当前选择的模型类型更新占位符文本
placeholder_text = "请输入至少100个字符的" + ("英文文本..." if model_type == "英文版模型 🇬🇧" else "中英文文本...")


# 开始按钮
if st.button("开始分析", type="primary"):
    if len(user_input.strip()) < 100:
        st.error("⚠️ 请输入至少100个字符的文本以确保预测准确性")
    else:
        with st.spinner("正在分析中，请稍候..."):
            progress_bar = st.progress(0)
            
            try:
                # 根据选择的模型类型进行预测
                if model_type == "英文版模型 🇬🇧":
                    prediction, confidences, top_contributing_words = st.session_state.tester.predict(user_input)
                else:
                    prediction, confidences, top_contributing_words = st.session_state.bilingual_tester.predict(user_input)
                
                # 更新进度条
                for i in range(100):
                    time.sleep(0.02)
                    progress_bar.progress(i + 1)
                
                success = True
            except Exception as e:
                st.error(f"分析过程中出现错误: {str(e)}")
                success = False
            
            progress_bar.empty()
            
            if success:
                st.success("✨ 分析完成！")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**选用模型：**")
                    st.markdown(model_type)
                with col2:
                    st.markdown("**预测类型：**")
                    st.markdown(f"**{prediction}**")

                # 显示各维度置信度
                st.markdown("### 维度分析")
                cols = st.columns(4)
                dimensions = ['I/E', 'N/S', 'T/F', 'J/P']
                for i, (dim, col) in enumerate(zip(dimensions, cols)):
                    with col:
                        dim_key = ['IE', 'NS', 'TF', 'JP'][i]
                        st.metric(
                            label=dim,
                            value=f"{confidences[dim_key]}%"
                        )

                # 显示关键词分析
                st.markdown("### 关键词分析")
                st.markdown("对预测结果影响最大的词语：")
                for word, _ in top_contributing_words:
                    st.markdown(f"- {word}")

else:
    placeholder_text = "请输入至少100个字符的" + ("英文文本..." if model_type == "英文版模型 🇬🇧 " else "中英文文本...")
    st.info(f"👆 请在上方输入{placeholder_text}")