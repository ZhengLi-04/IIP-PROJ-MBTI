# streamlit run MBTInsight.py
## entry page

import streamlit as st

st.set_page_config(
   page_title="MBTInsight",
   page_icon="",
   layout="wide",
   initial_sidebar_state="expanded",
)
st.logo("full_logo.png", size="large")

# 添加响应式文本样式
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"]{
        min-width: calc(250px + 5vw);
        max-width: calc(250px + 5vw);
    }
    /* 调整导航菜单的字体大小 */
    [data-testid="stSidebarNav"] {
        font-size: calc(0.7em + 0.25vw) !important;
    }
    [data-testid="stSidebarNav"] span {
        font-size: calc(10px + 0.25vw) !important;
    }
    /* 调整导航菜单中的图标大小 */
    [data-testid="stSidebarNav"] svg {
        height: calc(0.7em + 0.25vw) !important;
        width: calc(0.7em + 0.25vw) !important;
    }
    button[kind="header"] {
        display: none;
    }
    * {
        font-family: "PingFang SC", "Source Sans Pro", -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* 响应式文本类 */
    .sidebar-info-title {
        font-size: calc(12px + 0.3vw) !important;
        font-weight: bold !important;
        margin-bottom: calc(4px + 0.25vw) !important;
    }
    .sidebar-info-text {
        font-size: calc(10px + 0.25vw) !important;
        margin-bottom: calc(6px + 0.25vw) !important;
    }
    .sidebar-info-tiny {
        font-size: calc(8px + 0.25vw) !important;
        margin-bottom: calc(6px + 0.25vw) !important;
        color: #666666;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    # 使用markdown和HTML标签来应用自定义样式
    st.markdown('<p class="sidebar-info-title">关于 MBTInsight</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-info-text">MBTInsight 是一个基于文本的 MBTI 自动预测平台，运用前沿自然语言处理技术，通过分析输入文本的语言逻辑与表达习惯，快速精准输出人格类型结果，为用户自我认知、职业规划和社交互动提供专业参考。</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-info-text"></p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-info-title">关于我们</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-info-tiny">本项目由2025年《智能信息处理》课程第3组开发。<br>小组成员: 徐柯婷、李峥、唐宁琳。</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-info-tiny">© MBTInsight 2025，保留一切权利。</p>', unsafe_allow_html=True)

pages = {
    "目录": [
        st.Page("1_main.py", title="首页", icon="🏠"),
        st.Page("2_mbti.py", title="MBTI介绍", icon="🧠"),
        st.Page("3_intro.py", title="项目介绍", icon="📊"),
        st.Page("4_test.py", title="开始测试", icon="📝"),
        st.Page("5_result.py", title="测试结果", icon="📈"),
    ],
}

pg = st.navigation(pages)
pg.run()


