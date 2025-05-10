import streamlit as st

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
    .mbti-page-bigtitle {
        font-size: calc(36px + 0.25vw) !important;
        margin-bottom: calc(0px + 0vw) !important;
        font-weight: bold !important;
    }
    .mbti-page-title {
        font-size: calc(20px + 0.25vw) !important;
        margin-bottom: calc(8px + 0.25vw) !important;
        font-weight: bold !important;
    }
    .mbti-page-type {
        margin-top: calc(8px + 0.25vw) !important;
        font-size: calc(14px + 0.25vw) !important;
        margin-bottom: calc(8px + 0.25vw) !important;
        font-weight: bold !important;
    }
    .mbti-page-text {
        font-size: calc(12px + 0.25vw) !important;
        margin-bottom: calc(0px + 0.25vw) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<p class="mbti-page-bigtitle">MBTI 介绍</p>', unsafe_allow_html=True)
st.caption("🚀 MBTI 是一种基于荣格心理类型理论发展而来的性格测评工具，通过分析个人在四个维度上的偏好，将人格划分为十六种类型。")



st.markdown('<p class="mbti-page-title">📃 理论基础</p>', unsafe_allow_html=True)

st.markdown('<p class="mbti-page-text">MBTI，全称 Myers-Briggs Type Indicator，中文翻译为“迈尔斯-布里格斯类型指标”，是一种基于瑞士心理学家卡尔·荣格的心理类型理论发展出来的人格测评工具。最早由美国作家伊莎贝尔·布里格斯·迈尔斯和她的母亲凯瑟琳·库克·布里格斯在 20 世纪 40 年代编制而成。它主要用于测量和描述个人偏好和行为模式，帮助人们更好地理解自己的性格特点，并在职业、教育和人际关系等方面做出更好的决策。</p>', unsafe_allow_html=True)

st.divider()

st.markdown('<p class="mbti-page-title">📝 类别介绍</p>', unsafe_allow_html=True)

st.markdown('<p class="mbti-page-text">MBTI 通过四个维度——能量获得途径（外向 E 与内向 I）、认识世界（实感 S 与直觉 N）、判断事物（思维 T 与情感 F）以及生活态度（判断 J 与知觉 P）的组合，将人格划分为十六种可能的类型。这种划分不仅帮助人们更深入地了解自己的性格特征、价值观和行为习惯，还为人们提供了一个框架，以更好地理解和欣赏他人的差异。</p>', unsafe_allow_html=True)

st.markdown('<p class="mbti-page-type">能量获得途径</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown('<p class="mbti-page-typetitle">内向（Introverted）</p>', unsafe_allow_html=True)
    st.image("images/16personalities_trait_introverted.svg", use_container_width=True)
    st.markdown('<p class="mbti-page-text">内向型个体更喜欢独处活动，而社交互动会让他们感到疲惫。他们通常对外部刺激（例如声音、视觉或气味）比较敏感。</p>', unsafe_allow_html=True)

with col2:
    st.markdown('<p class="mbti-page-typetitle">外向（Extraverted）</p>', unsafe_allow_html=True)
    st.image("images/16personalities_trait_extraverted.svg", use_container_width=True)
    st.markdown('<p class="mbti-page-text">外向型个体更喜欢群体活动，而社交互动会给他们带来活力。他们通常比内向型人更有热情，也更容易兴奋。</p>', unsafe_allow_html=True)