## main page
import streamlit as st
import base64
from streamlit.components.v1 import html

def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

st.markdown("""
    <style>
    [data-testid="stImage"] {
        margin-top: -60px !important;  # 负值会使图片向上移动
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
    /* 响应式文本类 */
    .welcome-title {
        margin-top: -30px !important;
        font-size: calc(24px + 0.3vw) !important;
        font-weight: bold !important;
        margin-bottom: calc(4px + 0.25vw) !important;
    }
    .main-page-text {
        font-size: calc(12px + 0.25vw) !important;
        margin-bottom: calc(-40px + 0.25vw) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 使用自定义样式显示标题
st.markdown('<p class="welcome-title">欢迎使用 MBTInsight! 🚀</p>', unsafe_allow_html=True)
st.markdown('<p class="main-page-text">MBTInsight 是一个基于文本的 MBTI 自动预测平台，运用前沿自然语言处理技术，通过分析输入文本的语言逻辑与表达习惯，快速精准输出人格类型结果，为用户自我认知、职业规划和社交互动提供专业参考。</p>', unsafe_allow_html=True)
    
st.divider()


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
    st.markdown('<p class="column-title">了解 MBTI</p>', unsafe_allow_html=True)
    
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
        if st.button('了解更多 →', key='card1'):
            st.switch_page("2_mbti.py")

with col2:
    st.markdown('<p class="column-title">关于此项目</p>', unsafe_allow_html=True)
    
    with st.container():
        # 使用 base64 编码显示图片
        image_base64 = get_image_base64("images/col2.png")
        st.markdown(f"""
                    <a href="intro" target="_self">
            <div class="card-container" onclick> 
                <img src="data:image/png;base64,{image_base64}" class="card-image">
            </div>
            </a>
        """, unsafe_allow_html=True)
        # 使用可见按钮
        if st.button('了解更多 →', key='card2'):
            st.switch_page("3_intro.py")

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