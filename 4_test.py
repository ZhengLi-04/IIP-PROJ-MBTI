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
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.logo("full_logo.png", size="large")


def is_chinese(word):
    return all('\u4e00' <= char <= '\u9fff' for char in word)

# 在文件开头添加中文检测函数
def contains_chinese(text):
    for char in text:
        if '\u4e00' <= char <= '\u9fff':
            return True
    return False

def filter_words(words):
    return [item for item in words if '我' not in item[0]]  
# 配置设置
MODEL_ROOT = "../FuncCodes/predict_code/500 words/models/"  # 模型根目录
DIMENSIONS = ['IE', 'NS', 'TF', 'JP']  # 四个维度
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 文本预处理函数
def preprocess_text(text):
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'@\w+', '', text)

    # 新增的预处理步骤
    text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text)  # 只保留文字、数字和中文
    text = re.sub(r'\d+', ' ', text)  # 移除数字
    text = text.lower()  # 转换为小写
    
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# 添加双语模型类
class BilingualMBTITester:
    def __init__(self):
        self.models = {}
        self.tokenizer = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._load_models()
        self.stopwords = {"我", "我在", "我还", "我是", "我们", "的", "了", "是", "在", "有"}

    def _load_models(self):
        model_paths = {
            'IE': '../FuncCodes/predict_code/chinese & english/models/IE_model',
            'NS': '../FuncCodes/predict_code/chinese & english/models/NS_model',
            'TF': '../FuncCodes/predict_code/chinese & english/models/TF_model',
            'JP': '../FuncCodes/predict_code/chinese & english/models/JP_model'
        }
        
        self.tokenizer = AutoTokenizer.from_pretrained("../FuncCodes/predict_code/chinese & english/xlm-roberta-base/")
        self.models = self._load_all_models(model_paths)

    def _load_all_models(self, model_paths):
        models = {}
        for dim, path in model_paths.items():
            model = AutoModelForSequenceClassification.from_pretrained(path, num_labels=2)
            model.to(self.device)
            models[dim] = model
            print(f"成功加载双语模型 {dim} 维度")
        return models

    def predict(self, text):
        processed_text = self._preprocess_text(text)
        encoding = self.tokenizer(
            processed_text,
            add_special_tokens=True,
            max_length=512,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )

        input_ids = encoding['input_ids'].to(self.device)
        attention_mask = encoding['attention_mask'].to(self.device)

        dimension_results = {}
        dimension_probs = {}
        
        for dim, model in self.models.items():
            model.eval()
            with torch.no_grad():
                outputs = model(input_ids=input_ids, attention_mask=attention_mask)
                logits = outputs.logits
                probs = torch.softmax(logits, dim=1)
                pred = torch.argmax(logits, dim=1).item()
                dimension_results[dim] = pred
                dimension_probs[dim] = int(probs[0][pred].item() * 100)

        mbti_type = self._format_mbti(dimension_results)
        # formatted_output = self._format_output(mbti_type, dimension_results, dimension_probs)
        top_contributing_words = self.get_embedding_contributions(input_ids, attention_mask)
        
        return mbti_type, dimension_probs, top_contributing_words

    def _preprocess_text(self, text):
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        text = re.sub(r'@\w+', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def _format_mbti(self, preds):
        return ("I" if preds['IE'] == 0 else "E") + \
               ("N" if preds['NS'] == 0 else "S") + \
               ("T" if preds['TF'] == 0 else "F") + \
               ("J" if preds['JP'] == 0 else "P")

    # def _format_output(self, mbti_type, results, probs):
    #     output = f"预测的MBTI类型: {mbti_type}；"
    #     output += f"{'I' if results['IE']==0 else 'E'}（置信度 {probs['IE']}%）"
    #     output += f"{'N' if results['NS']==0 else 'S'}（置信度 {probs['NS']}%）" 
    #     output += f"{'T' if results['TF']==0 else 'F'}（置信度 {probs['TF']}%）"
    #     output += f"{'J' if results['JP']==0 else 'P'}（置信度 {probs['JP']}%）"
    #     return output

    def compute_word_importance(self, input_ids, model):
        embedding_layer = model.get_input_embeddings()
        embeddings = embedding_layer(input_ids)
        
        word_contributions = {}
        words = self.tokenizer.convert_ids_to_tokens(input_ids.squeeze().cpu().numpy())
        
        for i, word in enumerate(words):
            if word in self.tokenizer.all_special_tokens:
                continue
                
            clean_word = word[1:] if word.startswith("▁") else word
            
            # 应用新的过滤条件
            if (
                len(clean_word) < 2 or
                "我" in clean_word or
                (len(clean_word) <= 3 and clean_word.startswith("的")) or
                clean_word in self.stopwords 
                # (len(clean_word) < 3 and re.fullmatch(r'^[a-zA-Z]+$', clean_word))  # 新增英文短词过滤
            ):
                continue
                
            word_embedding = embeddings[0, i].cpu().detach().numpy()
            importance = np.linalg.norm(word_embedding)
            word_contributions[clean_word] = word_contributions.get(clean_word, 0) + importance
            
        return word_contributions

    def get_embedding_contributions(self, input_ids, attention_mask):
        total_contributions = {}
        for dim, model in self.models.items():
            contributions = self.compute_word_importance(input_ids, model)
            for word, score in contributions.items():
                total_contributions[word] = total_contributions.get(word, 0) + score
                
        top_30 = sorted(total_contributions.items(), key=lambda x: x[1], reverse=True)[:30]
        return top_30

# MBTITester 类定义
class MBTITester:
    def __init__(self):
        self.models = {}
        self.tokenizer = None
        self.stopwords = set([
            'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 
            'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 
            'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 
            'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 
            'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 
            'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 
            'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 
            'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 
            'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 
            'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 
            'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 
            'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 
            'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 
            'wouldn','type','types','lot','people'
        ])
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
        
        # 添加与predict.py一致的过滤逻辑
        meaningful_tokens = [
            token for token in tokens 
            if token.lower() not in self.stopwords 
            and not token.startswith('##') 
            and len(token) >= 3
        ]
        
        word_contributions = {token: 0 for token in meaningful_tokens}

        for layer in range(len(attention_weights)):
            for head in range(attention_weights[layer].shape[1]):
                attention_map = attention_weights[layer][0, head].detach().cpu().numpy()
                for i, token in enumerate(meaningful_tokens):
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

    # 修改 MBTITester._get_top_contributing_words()
    def _get_top_contributing_words(self, total_word_contributions, top_n=30):  # 修改top_n为30
        return sorted(total_word_contributions.items(), key=lambda item: item[1], reverse=True)[:top_n]

    # 添加与predict.py相同的词云生成方法
    def generate_wordcloud(self, top_contributing_words):
        word_freq = {word: contribution for word, contribution in top_contributing_words}
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)
        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        return plt

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


# 首先定义维度全称的映射
DIMENSION_NAMES = {
    'I': 'Introverted',
    'E': 'Extraverted',
    'N': 'Intuition',
    'S': 'Sensing',
    'T': 'Thinking',
    'F': 'Feeling',
    'J': 'Judging',
    'P': 'Perceiving'
}

# 定义每个维度的颜色
DIMENSION_COLORS = {
    'IE': ['#5996B1', '#5996B1'],  # 红色到青色
    'NS': ['#DCB051', '#DCB051'],  # 薄荷绿到橙色
    'TF': ['#54A177', '#54A177'],  # 绿色到粉色
    'JP': ['#826396', '#826396']   # 珊瑚色到蓝色
}

# 更新样式定义
st.markdown(
    """
    <style>
    .dimension-container {
        position: relative;
        margin: 30px 0;
        padding: 0 150px;  /* 为两侧文本留出空间 */
    }
    
    .dimension-bar {
        width: 100%;
        height: 12px;
        border-radius: 6px;
        position: relative;
    }
    
    .dimension-indicator {
        width: 20px;
        height: 20px;
        background: white;
        border: 3px solid;
        border-radius: 50%;
        position: absolute;
        top: -4px;
        transform: translateX(-50%);
        cursor: pointer;
        transition: all 0.3s ease;
        z-index: 2;
    }
    
    .dimension-indicator:hover {
        transform: translateX(-50%) scale(1.2);
        box-shadow: 0 0 10px rgba(0,0,0,0.2);
    }
    
    .dimension-label {
    position: absolute;
    font-size: 14px;
    color: #2d3436;
    width: auto;  /* 固定宽度 */
    text-align: center;
    top: 50%;  
    transform: translateY(-50%);  /* 这里的引号有问题，需要修复 */
    }

    .dimension-label.left {
        left: 30px;  /* 使用固定距离替代transform */
        text-align: right;
    }

    .dimension-label.right {
        right: 30px;  /* 使用固定距离替代transform */
        text-align: left;
    }
    
    .dimension-value {
        position: absolute;
        font-size: 14px;
        font-weight: bold;
        transform: translateX(-50%);
        top: -40px;  /* 上移标签 */
        background: white;
        padding: 2px 8px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        min-width: 100px;  /* 设置最小宽度 */
        width: auto;  /* 允许自适应 */
        white-space: nowrap;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 修改维度条生成函数
def create_dimension_bar(left_type, right_type, confidence, pred, dim_key):
    # 获取维度的颜色
    colors = DIMENSION_COLORS[dim_key]
    # 获取维度的全称
    left_full = DIMENSION_NAMES[left_type]
    right_full = DIMENSION_NAMES[right_type]
    # 计算指示器位置
    position = confidence if pred == 1 else (100 - confidence)
    # 设置渐变色
    gradient = f"linear-gradient(to right, {colors[0]}, {colors[1]})"
    
    html = f"""
    <div class="dimension-container">
        <div class="dimension-label left">{left_full}</div>
        <div class="dimension-bar" style="background: {gradient};">
            <div class="dimension-value" style="left: {position}%; color: {colors[1] if pred == 1 else colors[0]}">
                {confidence}% {right_full if pred == 1 else left_full}
            </div>
            <div class="dimension-indicator" style="left: {position}%; border-color: {colors[1] if pred == 1 else colors[0]};"></div>
        </div>
        <div class="dimension-label right">{right_full}</div>
    </div>
    """
    return html


# 添加响应式文本样式
st.markdown(
    """
    <style>
    button[kind="header"] {
        display: none;
    }
    * {
        font-family: "Source Sans Pro", "PingFang SC",  -apple-system, BlinkMacSystemFont, sans-serif !important;
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
    placeholder="请输入至少100个字符的中/英文文本..."
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

# ... 前面的代码保持不变 ...

# 修改样式定义部分
st.markdown("""
    <style>
    /* 为"开始分析"按钮添加特定样式 */
    .start-analysis-button {
        background-color: #4CAF50 !important;
        color: white !important;
        font-weight: bold !important;
        padding: 10px 20px !important;
        border-radius: 5px !important;
        border: none !important;
        transition: all 0.3s ease !important;
        font-size: 16px !important;
        width: auto !important;
        text-align: center !important;
    }

    .start-analysis-button:hover {
        background-color: #45a049 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
    }
    </style>
""", unsafe_allow_html=True)

# 开始按钮
if st.button("开始分析",key="start-analysis",use_container_width=True, disabled=len(user_input.strip()) < 100 or (model_type == "英文版模型 🇬🇧" and contains_chinese(user_input))):
    if len(user_input.strip()) < 100:
        st.error("⚠️ 请输入至少100个字符的文本以确保预测准确性")
    elif model_type == "英文版模型 🇬🇧" and contains_chinese(user_input):
        st.error("⚠️ 检测到中文字符！英文版模型仅支持英文输入，请切换到双语版模型或更换为纯英文文本。")
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

                st.session_state.mbti_type = prediction
                # 显示各维度置信度
                st.markdown("**维度分析**")

                dimension_pairs = [
                    ('I', 'E', 'IE'),
                    ('N', 'S', 'NS'),
                    ('T', 'F', 'TF'),
                    ('J', 'P', 'JP')
                ]
                
                # 修改维度分析显示部分
                for left, right, dim_key in dimension_pairs:
                    confidence = confidences[dim_key]
                    pred = 1 if prediction[dimension_pairs.index((left, right, dim_key))] == right else 0
                    html = create_dimension_bar(left, right, confidence, pred, dim_key)
                    st.markdown(html, unsafe_allow_html=True)

                
                if model_type == "英文版模型 🇬🇧":
                    st.markdown("**关键词词云分析**")
                    st.markdown("对预测结果影响最大的词语：")
                    
                    col1, col2, col3 = st.columns([1, 8, 1])
                    with col2:
                        st.markdown("<div style='margin-bottom:70px;'></div>", unsafe_allow_html=True)
                        with st.container():
                            plt = st.session_state.tester.generate_wordcloud(top_contributing_words)
                            st.pyplot(plt)
                            plt.close()
                else:
                    # 替换原有的关键词分析部分
                    st.markdown("**关键词词云分析**")
                    st.markdown("对预测结果影响最大的词语：")
                    
                    col1, col2, col3 = st.columns([1, 8, 1])

                    with col2:
                        st.markdown("<div style='margin-bottom:70px;'></div>", unsafe_allow_html=True)
                        with st.container():
                            # 生成词云
                            word_freq = {word: contri for word, contri in top_contributing_words}
                            wordcloud = WordCloud(
                                font_path="/System/Library/Fonts/Hiragino Sans GB.ttc",
                                width=500,  # 适当缩小画布尺寸
                                height=200,
                                background_color='white',
                                scale=0.9
                            ).generate_from_frequencies(word_freq)
                        
                            plt.figure(figsize=(8, 4), dpi=300)  # 调整DPI降低分辨率
                            plt.imshow(wordcloud, interpolation='bilinear')
                            plt.axis("off")
                            st.pyplot(plt, use_container_width=True)  # 使用容器宽度自适应
                            plt.close()

else:
    placeholder_text = "至少100个字符的" + ("英文文本..." if model_type == "英文版模型 🇬🇧 " else "中/英文文本...")
    st.info(f"👆 请在上方输入{placeholder_text}")

# 在样式定义部分添加以下CSS
st.markdown("""
    <style>
    /* ...existing code... */
    
    .keyword-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }
    
    .keyword-tag {
        background: #f1f3f5;
        padding: 3px 15px;
        border-radius: 15px;
        font-size: 14px;
        color: #495057;
        border: 1px solid #e9ecef;
        transition: all 0.2s ease;
    }
    
    .keyword-tag:hover {
        transform: translateY(-2px);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)






# ====================================================
# 底部跳转
# ====================================================

st.divider()
col1, col2, col3 = st.columns(3)
# 修改样式，添加按钮样式

with col1:
    st.markdown('<p class="column-title">返回首页</p>', unsafe_allow_html=True)
    
    with st.container():
        # 使用 base64 编码显示图片
        image_base64 = get_image_base64("images/col1.png")
        st.markdown(f"""
                    <a href="mbti" target="_self">
            <div class="card-container" onclick> 
                <img src="data:image/png;base64,{image_base64}" class="card-image">
            </div>
            </a>
        """, unsafe_allow_html=True)
        # 使用可见按钮
        if st.button('← 返回首页', key='card1',type="tertiary"):
            st.switch_page("1_main.py")

with col2:
    st.markdown('<p class="column-title">了解 MBTI</p>', unsafe_allow_html=True)
    
    with st.container():
        # 使用 base64 编码显示图片
        image_base64 = get_image_base64("images/col2.png")
        st.markdown(f"""
                    <a href="mbti" target="_self">
            <div class="card-container" onclick> 
                <img src="data:image/png;base64,{image_base64}" class="card-image">
            </div>
            </a>
        """, unsafe_allow_html=True)
        if st.button('← 了解更多', key='card2' ,type="tertiary"):
            st.switch_page("2_mbti.py")

with col3:
    st.markdown('<p class="column-title">详细解读</p>', unsafe_allow_html=True)
    
    with st.container():
        # 使用 base64 编码显示图片
        image_base64 = get_image_base64("images/col3.png")
        st.markdown(f"""
                    <a href="result" target="_self">
            <div class="card-container" onclick> 
                <img src="data:image/png;base64,{image_base64}" class="card-image">
            </div>
            </a>
        """, unsafe_allow_html=True)
        # 使用可见按钮
        if st.button('了解更多 →', key='card3',type="tertiary"):
            st.switch_page("5_result.py")

st.markdown("""
    <style>
    .card-container {
        cursor: pointer;
        transition: all 0.3s ease;
        # padding: 10px;
        border-radius: 10px;
        background: white;
        margin-bottom: 2px;
        width: 90%;
    }
    .card-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .card-image {
        width: 100%;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    # /* 自定义按钮样式 */
    # .stButton>button {
    #     background-color: transparent !important;
    #     color: #1E88E5 !important;
    #     border: none !important;
    #     padding: 0 !important;
    #     font-weight: 500 !important;
    #     text-align: right !important;
    #     font-size: calc(10px + 0.2vw) !important;
    # }
    # .stButton>button p, .stButton>button span {
    #     font-size: calc(10px + 0.2vw) !important;  /* 确保按钮内部文字也使用相同大小 */
    # }
    # .stButton>button:hover {
    #     color: #1565C0 !important;
    #     background: none !important;
    #     border: none !important;
    # }
    .column-title {
        font-size: calc(14px + 0.3vw) !important;
        font-weight: bold !important;
        margin-bottom: calc(8px + 0.25vw) !important;
        margin-top: calc(-20px - 0.25vw) !important;
    }
    </style>
""", unsafe_allow_html=True)