import streamlit as st
import base64
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import altair as alt

st.logo("full_logo.png", size="large")

# 添加 base64 图片转换函数
def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

# 添加响应式文本样式
st.markdown(
    """
    <style>
    button[kind="header"] {
        display: none;
    }
    .dataframe td {
    white-space: normal !important;
    height: auto !important;
    padding: 8px 12px !important;
    }
    table {
        font-size: calc(10px + 0.15vw) !important;
    }
    th {
        font-size: calc(10px + 0.15vw) !important;
        padding: 6px 10px !important;
        background: #f8f9fa !important;
    }
    td {
        font-size: calc(11px + 0.15vw) !important;
        padding: 5px 10px !important;
    }
    * {
        font-family: "Source Sans Pro", "PingFang SC",  -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
    .intro-page-bigtitle {
        font-size: calc(36px + 0.25vw) !important;
        margin-bottom: calc(0px + 0vw) !important;
        font-weight: bold !important;
        margin-top: calc(-60px + 0.25vw) !important;
    }
    .intro-page-title {
        font-size: calc(16px + 0.25vw) !important;
        margin-bottom: calc(8px + 0.25vw) !important;
        font-weight: bold !important;
    }
    .intro-page-type {
        margin-top: calc(8px + 0.25vw) !important;
        font-size: calc(14px + 0.25vw) !important;
        margin-bottom: calc(8px + 0.25vw) !important;
        font-weight: bold !important;
    }
    .intro-page-text {
        font-size: calc(12px + 0.25vw) !important;
        margin-bottom: calc(12px + 0.25vw) !important;
    }
    
    /* 卡片容器样式 */
    .intro-card {
        background: white;
        border-radius: 20px;
        padding: 20px 20px 10px 20px;
        margin: 10px 10px 10px 10px;
        transition: all 0.3s ease;
        border: 1.5px solid #eee;
    }
    
    .intro-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* 卡片标题样式 */
    .intro-page-typetitle {
        font-size: calc(14px + 0.25vw) !important;
        font-weight: bold !important;
        color: #333;
        margin-bottom: 1px !important;
        text-align: center;
    }
    .intro-page-typetitle-2 {
        font-size: calc(10px + 0.25vw) !important;
        font-weight: bold !important;
        color: #333;
        margin-bottom: 1px !important;
        text-align: center;
    }
    .intro-page-typetitle2 {
        font-size: calc(13px + 0.25vw) !important;
        font-weight: bold !important;
        color: #333;
        margin-bottom: 15px !important;
        text-align: center;
    }
    /* 卡片图片容器 */
    .intro-card-image {
        text-align: center;
        margin: 10px 0;
    }
    
    /* 卡片文本样式 */
    .intro-card-text {
        font-size: calc(11px + 0.25vw) !important;
        color: #666;
        line-height: 1.6;
        margin: 10px 10px 10px 10px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<p class="intro-page-bigtitle">项目介绍</p>', unsafe_allow_html=True)
st.caption("🚀 MBTInsight 是一个基于文本的 MBTI 自动预测平台，运用前沿自然语言处理技术，通过分析输入文本的语言逻辑与表达习惯，快速精准输出人格类型结果，为用户自我认知、职业规划和社交互动提供专业参考。")

tab1, tab2 = st.tabs(["英文版模型 🇬🇧 ", "双语版模型 🇨🇳 🇬🇧"])




# ==========================================================
# 英文版模型部分
# ==========================================================
with tab1:
    st.markdown('<p class="intro-page-title">📊 数据集说明</p>', unsafe_allow_html=True)
    st.markdown('<p class="intro-page-text">训练集共106067条数据，测试集共8675条数据。</p>', unsafe_allow_html=True)
    # # 原始数据
    # train_counts = {
    #     "INTP": 24961, "INTJ": 22427, "INFJ": 14963, "INFP": 12134,
    #     "ENTP": 11725, "ENFP": 6167,  "ISTP": 3424,  "ENTJ": 2955,
    #     "ESTP": 1986,  "ENFJ": 1534,  "ISTJ": 1243,  "ISFP": 875,
    #     "ISFJ": 650,   "ESTJ": 482,   "ESFP": 360,   "ESFJ": 181
    # }
    # test_counts = {
    #     "INFP": 1832,  "INFJ": 1470,  "INTP": 1304,  "INTJ": 1091,
    #     "ENTP": 685,   "ENFP": 675,   "ISTP": 337,   "ISFP": 271,
    #     "ENTJ": 231,   "ISTJ": 205,   "ENFJ": 190,   "ISFJ": 166,
    #     "ESTP": 89,    "ESFP": 48,    "ESFJ": 42,    "ESTJ": 39
    # }

    # # 转成长表格格式
    # df = (
    #     pd.DataFrame({
    #         "Train": pd.Series(train_counts),
    #         "Test":  pd.Series(test_counts),
    #     })
    #     .reset_index().melt(id_vars="index", var_name="Dataset", value_name="Count")
    #     .rename(columns={"index": "Type"})
    # )

    # # 如果你想要在同一张图中并排而非分面，去掉 column，改为 x 的二级分组：
    # chart = (
    #     alt.Chart(df)
    #     .mark_bar()
    #     .encode(
    #         x=alt.X("Type:N", sort=list(train_counts.keys()), title="MBTI 类型"),
    #         xOffset="Dataset:N",
    #         y=alt.Y("Count:Q", title="数量"),
    #         color=alt.Color("Dataset:N", scale=alt.Scale(range=["#ff7f0e","#1f77b4"]))
    #     )
    #     .properties(width=600, height=350)
    # )

    # st.altair_chart(chart, use_container_width=True)
    sample_data = pd.DataFrame({
        "字段名称": ["type", "posts"],
        "字段说明": ["MBTI人格类型（16种）", "500个英文单词"],
        "示例": ["INTP/INTJ/INFJ...", "loose overthinking ruin friendship insecurity learn ..."]
    })
    
    st.caption("📋 数据集字段说明")
    st.table(sample_data.style.hide(axis="index"))

    st.markdown('<p class="intro-page-title">🔮 模型介绍</p>', unsafe_allow_html=True)
    st.markdown('<p class="intro-page-text">使用预训练的BERT模型作为基础，在BERT的基础上添加了一个全连接层，用于进行二分类任务。每个维度的分类任务都使用一个独立的模型进行训练，从而将复杂的16分类问题转换为4个二分类问题。</p>', unsafe_allow_html=True)

    st.markdown('<p class="intro-page-title">📈 模型效果</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        image_base64 = get_image_base64("images/eng_train_acc.png")
        st.markdown(f"""
            <div class="intro-card word-cloud-card">
                <p class="intro-page-typetitle">验证集上的准确率</p>
                <div class="intro-card-image">
                    <img src="data:image/png;base64,{image_base64}" style="width: 100%; margin: auto;">
                </div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        image_base64 = get_image_base64("images/eng_test_acc.png")
        st.markdown(f"""
            <div class="intro-card word-cloud-card">
                <p class="intro-page-typetitle">测试集上的准确率</p>
                <div class="intro-card-image">
                    <img src="data:image/png;base64,{image_base64}" style="width: 100%; margin: auto;">
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('<p class="intro-page-title">🧐 高频词分析</p>', unsafe_allow_html=True)

    # 创建四行布局
    for trait_pair in [("E/I", "e.png", "i.png"), 
                    ("S/N", "s.png", "n.png"),
                    ("T/F", "t.png", "f.png"),
                    ("J/P", "j.png", "p.png")]:
        row = st.columns([0.5, 0.5])  # 每行分为两列
        
        # 左侧特征
        with row[0]:
            image_base64 = get_image_base64(f"images/eng_fre_{trait_pair[1]}")
            st.markdown(f"""
                <div class="intro-card word-cloud-card">
                    <p class="intro-page-typetitle">{trait_pair[0].split('/')[0]} 型特征词云</p>
                    <div class="intro-card-image">
                        <img src="data:image/png;base64,{image_base64}" style="width: 100%; margin: auto;">
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # 右侧特征
        with row[1]:
            image_base64 = get_image_base64(f"images/eng_fre_{trait_pair[2]}")
            st.markdown(f"""
                <div class="intro-card word-cloud-card">
                    <p class="intro-page-typetitle">{trait_pair[0].split('/')[1]} 型特征词云</p>
                    <div class="intro-card-image">
                        <img src="data:image/png;base64,{image_base64}" style="width: 100%; margin: auto;">
                    </div>
                </div>
            """, unsafe_allow_html=True)






# ==========================================================
# 双语版模型部分
# ==========================================================
with tab2:
    st.markdown('<p class="intro-page-title">📊 数据集说明</p>', unsafe_allow_html=True)
    st.markdown('<p class="intro-page-text">数据集共10544条数据。</p>', unsafe_allow_html=True)
    
    sample_data = pd.DataFrame({
        "字段名称": ["type", "posts"],
        "字段说明": ["MBTI人格类型（16种）", "用户的一段中文/英文自述"],
        "示例": ["INTP/INTJ/INFJ...", "我为自己快速适应新环境的能力感到自豪。我在充满活力的环境中发挥出色..."]
    })
    
    st.caption("📋 数据集字段说明")
    st.table(sample_data.style.hide(axis="index"))

    # # 修改为新的数据
    # counts = {
    #     "ESFP": 747, "ESFJ": 729, "ESTP": 717, "ESTJ": 710,
    #     "ENFP": 702, "ENTJ": 700, "ISFP": 666, "ISFJ": 664,
    #     "INFP": 652, "ENTP": 647, "ENFJ": 633, "ISTP": 626,
    #     "ISTJ": 600, "INTP": 598, "INTJ": 591, "INFJ": 562
    # }

    # # 转成长表格格式
    # df = (
    #     pd.DataFrame({
    #         "Count": pd.Series(counts),
    #     })
    #     .reset_index()
    #     .rename(columns={"index": "Type"})
    # )

    # # 绘制条形图
    # chart = (
    #     alt.Chart(df)
    #     .mark_bar()
    #     .encode(
    #         x=alt.X("Type:N", sort=list(counts.keys()), title="MBTI 类型"),
    #         y=alt.Y("Count:Q", title="数量"),
    #         color=alt.value("#1f77b4")  # 使用单一颜色
    #     )
    #     .properties(width=600, height=350)
    # )

    # st.altair_chart(chart, use_container_width=True)

    # ...rest of the code...

    st.markdown('<p class="intro-page-title">🔮 模型介绍</p>', unsafe_allow_html=True)
    st.markdown('<p class="intro-page-text">使用 langid 库对输入文本进行自动语言检测，识别是否为英文、中文等，为后续分析和过滤低置信语言样本提供依据。选用 XLM-Roberta（跨语言预训练模型）作为主干，具备自动识别语言、跨语言共享语义、中英混杂处理能力强等能力。</p>', unsafe_allow_html=True)

    st.markdown('<p class="intro-page-title">📈 模型效果</p>', unsafe_allow_html=True)

    col1, col2,col3,col4 = st.columns(4)
    with col1:
        image_base64 = get_image_base64("images/cheng_train_ie.png")
        st.markdown(f"""
            <div class="intro-card word-cloud-card">
                <p class="intro-page-typetitle-2">验证集上I/E维度混淆矩阵</p>
                <div class="intro-card-image">
                    <img src="data:image/png;base64,{image_base64}" style="width: 100%; margin: auto;">
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        image_base64 = get_image_base64("images/cheng_train_ns.png")
        st.markdown(f"""
            <div class="intro-card word-cloud-card">
                <p class="intro-page-typetitle-2">验证集上N/S维度混淆矩阵</p>
                <div class="intro-card-image">
                    <img src="data:image/png;base64,{image_base64}" style="width: 100%; margin: auto;">
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        image_base64 = get_image_base64("images/cheng_train_tf.png")
        st.markdown(f"""
            <div class="intro-card word-cloud-card">
                <p class="intro-page-typetitle-2">验证集上T/F维度混淆矩阵</p>
                <div class="intro-card-image">
                    <img src="data:image/png;base64,{image_base64}" style="width: 100%; margin: auto;">
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        image_base64 = get_image_base64("images/cheng_train_jp.png")
        st.markdown(f"""
            <div class="intro-card word-cloud-card">
                <p class="intro-page-typetitle-2">验证集上J/P维度混淆矩阵</p>
                <div class="intro-card-image">
                    <img src="data:image/png;base64,{image_base64}" style="width: 100%; margin: auto;">
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('<p class="intro-page-title">🧐 高频词分析</p>', unsafe_allow_html=True)

    # 创建四行布局
    for trait_pair in [("E/I", "e.png", "i.png"), 
                    ("S/N", "s.png", "n.png"),
                    ("T/F", "t.png", "f.png"),
                    ("J/P", "j.png", "p.png")]:
        row = st.columns([0.5, 0.5])  # 每行分为两列
        
        # 左侧特征
        with row[0]:
            image_base64 = get_image_base64(f"images/cheng_fre_{trait_pair[1]}")
            st.markdown(f"""
                <div class="intro-card word-cloud-card">
                    <p class="intro-page-typetitle">{trait_pair[0].split('/')[0]} 型特征词云</p>
                    <div class="intro-card-image">
                        <img src="data:image/png;base64,{image_base64}" style="width: 100%; margin: auto;">
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # 右侧特征
        with row[1]:
            image_base64 = get_image_base64(f"images/cheng_fre_{trait_pair[2]}")
            st.markdown(f"""
                <div class="intro-card word-cloud-card">
                    <p class="intro-page-typetitle">{trait_pair[0].split('/')[1]} 型特征词云</p>
                    <div class="intro-card-image">
                        <img src="data:image/png;base64,{image_base64}" style="width: 100%; margin: auto;">
                    </div>
                </div>
            """, unsafe_allow_html=True)

st.divider()



# ====================================================
# 底部跳转
# ====================================================

col1, col2, col3 = st.columns(3)
# 修改样式，添加按钮样式
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
    /* 自定义按钮样式 */
    .stButton>button {
        background-color: transparent !important;
        color: #1E88E5 !important;
        border: none !important;
        padding: 0 !important;
        font-weight: 500 !important;
        text-align: right !important;
        font-size: calc(10px + 0.2vw) !important;
    }
    .stButton>button p, .stButton>button span {
        font-size: calc(10px + 0.2vw) !important;  /* 确保按钮内部文字也使用相同大小 */
    }
    .stButton>button:hover {
        color: #1565C0 !important;
        background: none !important;
        border: none !important;
    }
    .column-title {
        font-size: calc(14px + 0.3vw) !important;
        font-weight: bold !important;
        margin-bottom: calc(8px + 0.25vw) !important;
        margin-top: calc(-20px - 0.25vw) !important;
    }
    </style>
""", unsafe_allow_html=True)


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
        if st.button('← 返回首页', key='card1'):
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
        # 使用可见按钮
        if st.button('← 了解更多', key='card2'):
            st.switch_page("2_mbti.py")

with col3:
    st.markdown('<p class="column-title">开始测试</p>', unsafe_allow_html=True)
    
    with st.container():
        # 使用 base64 编码显示图片
        image_base64 = get_image_base64("images/col3.png")
        st.markdown(f"""
                    <a href="test" target="_self">
            <div class="card-container" onclick> 
                <img src="data:image/png;base64,{image_base64}" class="card-image">
            </div>
            </a>
        """, unsafe_allow_html=True)
        # 使用可见按钮
        if st.button('点击开始 →', key='card3'):
            st.switch_page("4_test.py")