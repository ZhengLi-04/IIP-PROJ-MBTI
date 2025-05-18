import streamlit as st
import base64

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
    * {
        font-family: "PingFang SC", "Source Sans Pro", -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    .mbti-page-bigtitle {
        font-size: calc(36px + 0.25vw) !important;
        margin-bottom: calc(0px + 0vw) !important;
        font-weight: bold !important;
        margin-top: calc(-60px + 0.25vw) !important;
    }
    .mbti-page-title {
        font-size: calc(16px + 0.25vw) !important;
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
    
    /* 卡片容器样式 */
    .mbti-card {
        background: white;
        border-radius: 20px;
        padding: 20px 20px 10px 20px;
        margin: 10px 10px 10px 10px;
        transition: all 0.3s ease;
        border: 1.5px solid #eee;
    }
    
    .mbti-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* 卡片标题样式 */
    .mbti-page-typetitle {
        font-size: calc(16px + 0.25vw) !important;
        font-weight: bold !important;
        color: #333;
        margin-bottom: 15px !important;
        text-align: center;
    }
    .mbti-page-typetitle2 {
        font-size: calc(13px + 0.25vw) !important;
        font-weight: bold !important;
        color: #333;
        margin-bottom: 15px !important;
        text-align: center;
    }
    /* 卡片图片容器 */
    .mbti-card-image {
        text-align: center;
        margin: 20px 0;
    }
    
    /* 卡片文本样式 */
    .mbti-card-text {
        font-size: calc(11px + 0.25vw) !important;
        color: #666;
        line-height: 1.6;
        margin: 10px 10px 10px 10px !important;
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

st.markdown('<p class="mbti-page-text">这方面展示了我们如何与周围环境互动：</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # 获取内向图片的 base64 编码
    intro_image = get_image_base64("images/16personalities_trait_introverted.png")
    st.markdown(f"""
        <div class="mbti-card">
            <p class="mbti-page-typetitle">🤫 内向 Introverted 🤫</p>
            <div class="mbti-card-image">
                <img src="data:image/png;base64,{intro_image}" style="width: 80%; margin: auto;">
            </div>
            <div style="border-bottom: 0.8px solid #ccc; margin: 15px 15px;"></div>
            <p class="mbti-card-text">内向型个体更喜欢独处活动，而社交互动会让他们感到疲惫。他们通常对外部刺激（例如声音、视觉或气味）比较敏感。</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    # 获取外向图片的 base64 编码
    extro_image = get_image_base64("images/16personalities_trait_extraverted.png")
    st.markdown(f"""
        <div class="mbti-card">
            <p class="mbti-page-typetitle">🤗 外向 Extraverted 🤗</p>
            <div class="mbti-card-image">
                <img src="data:image/png;base64,{extro_image}" style="width: 80%; margin: auto;">
            </div>
            <div style="border-bottom: 0.8px solid #ccc; margin: 15px 15px;"></div>
            <p class="mbti-card-text">外向型个体更喜欢群体活动，而社交互动会给他们带来活力。他们通常比内向型人更有热情，也更容易兴奋。</p>
        </div>
    """, unsafe_allow_html=True)


st.markdown('<p class="mbti-page-type">信息感知方式</p>', unsafe_allow_html=True)

st.markdown('<p class="mbti-page-text">这个方面决定了我们如何看待世界以及如何处理信息：</p>', unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    # 获取实感图片的 base64 编码
    sensing_image = get_image_base64("images/16personalities_trait_observant.png")
    st.markdown(f"""
        <div class="mbti-card">
            <p class="mbti-page-typetitle">🔍 实感 Sensing 🔍</p>
            <div class="mbti-card-image">
                <img src="data:image/png;base64,{sensing_image}" style="width: 80%; margin: auto;">
            </div>
            <div style="border-bottom: 0.8px solid #ccc; margin: 15px 15px;"></div>
            <p class="mbti-card-text">实感型的人非常实际、务实和脚踏实地。他们倾向于有强烈的习惯，并关注正在发生的事情或已经发生的事情。</p>
        </div>
    """, unsafe_allow_html=True)

with col4:
    # 获取直觉图片的 base64 编码
    intuition_image = get_image_base64("images/16personalities_trait_intuitive.png")
    st.markdown(f"""
        <div class="mbti-card">
            <p class="mbti-page-typetitle">🔮 直觉 Intuition 🔮</p>
            <div class="mbti-card-image">
                <img src="data:image/png;base64,{intuition_image}" style="width: 80%; margin: auto;">
            </div>
            <div style="border-bottom: 0.8px solid #ccc; margin: 15px 15px;"></div>
            <p class="mbti-card-text">直觉型的人非常富有想象力、思想开放且充满好奇心。他们更倾向于新奇而非稳定，关注隐藏的意义和未来的可能性。</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown('<p class="mbti-page-type">处理信息的决策方式</p>', unsafe_allow_html=True)

st.markdown('<p class="mbti-page-text">这个方面决定了我们做决定和应对情绪的方式：</p>', unsafe_allow_html=True)

col5, col6 = st.columns(2)
with col5:
    # 获取思维图片的 base64 编码
    thinking_image = get_image_base64("images/16personalities_trait_thinking.png")
    st.markdown(f"""
        <div class="mbti-card">
            <p class="mbti-page-typetitle">🧠 思考 Thinking 🧠</p>
            <div class="mbti-card-image">
                <img src="data:image/png;base64,{thinking_image}" style="width: 80%; margin: auto;">
            </div>
            <div style="border-bottom: 0.8px solid #ccc; margin: 15px 15px;"></div>
            <p class="mbti-card-text">思考者注重客观性和理性，优先考虑逻辑而非情感。他们倾向于隐藏自己的感受，并认为效率比合作更重要。</p>
        </div>
    """, unsafe_allow_html=True)
with col6:
    # 获取情感图片的 base64 编码
    feeling_image = get_image_base64("images/16personalities_trait_feeling.png")
    st.markdown(f"""
        <div class="mbti-card">
            <p class="mbti-page-typetitle">❤️ 情感 Feeling ❤️</p>
            <div class="mbti-card-image">
                <img src="data:image/png;base64,{feeling_image}" style="width: 80%; margin: auto;">
            </div>
            <div style="border-bottom: 0.8px solid #ccc; margin: 15px 15px;"></div>
            <p class="mbti-card-text">感性个体敏感且情感丰富。与思考型相比，他们更有同情心，竞争性较低，注重社会和谐与合作。</p>
        </div>
    """, unsafe_allow_html=True)


st.markdown('<p class="mbti-page-type">与周围世界的接触方式</p>', unsafe_allow_html=True)

st.markdown('<p class="mbti-page-text">这个方面反映了我们对待工作、规划和决策的方式：</p>', unsafe_allow_html=True)

col7, col8 = st.columns(2)
with col7:
    # 获取判断图片的 base64 编码
    judging_image = get_image_base64("images/16personalities_trait_judging.png")
    st.markdown(f"""
        <div class="mbti-card">
            <p class="mbti-page-typetitle">📋 判断 Judging 📋</p>
            <div class="mbti-card-image">
                <img src="data:image/png;base64,{judging_image}" style="width: 80%; margin: auto;">
            </div>
            <div style="border-bottom: 0.8px solid #ccc; margin: 15px 15px;"></div>
            <p class="mbti-card-text">判断型个体喜欢有序和结构化的生活方式。他们倾向于提前计划，并在做决定时依赖逻辑和分析。</p>
        </div>
    """, unsafe_allow_html=True)

with col8:
    # 获取知觉图片的 base64 编码
    perceiving_image = get_image_base64("images/16personalities_trait_prospecting.png")
    st.markdown(f"""
        <div class="mbti-card">
            <p class="mbti-page-typetitle">🕊️ 感知 Perceiving 🕊️</p>
            <div class="mbti-card-image">
                <img src="data:image/png;base64,{perceiving_image}" style="width: 80%; margin: auto;">
            </div>
            <div style="border-bottom: 0.8px solid #ccc; margin: 15px 15px;"></div>
            <p class="mbti-card-text">感知型个体非常擅长即兴发挥和发现机会。他们倾向于灵活、放松的非传统者，更喜欢保持选择余地。</p>
        </div>
    """, unsafe_allow_html=True)

st.divider()

st.markdown('<p class="mbti-page-title">👥 类型组</p>', unsafe_allow_html=True)

col9, col10 = st.columns(2)
with col9:
    st.markdown('<p class="mbti-page-type">分析家</p>', unsafe_allow_html=True)

    # 获取分析家图片的 base64 编码
    analyst_image = get_image_base64("images/分析.png")
    st.markdown(f"""
        <div class="mbti-card">
            <p class="mbti-page-typetitle2">🧩 分析家（INTJ、INTP、ENTJ、ENTP）🧩 </p>
            <div class="mbti-card-image">
                <img src="data:image/png;base64,{analyst_image}" style="width: 90%; margin: auto;">
            </div>
            <div style="border-bottom: 0.8px solid #ccc; margin: 15px 15px;"></div>
            <p class="mbti-card-text">这些人格类型崇尚理性和公正，擅长智力辩论和科学或技术领域。他们非常独立、思想开放、意志坚定且富有想象力，从功利主义的角度看待许多事物，并且比满足所有人更关心什么有效。这些特质使分析师成为出色的战略思考者，但在社交或浪漫追求方面也会带来困难。</p>
        </div>
    """, unsafe_allow_html=True)

with col10:
    st.markdown('<p class="mbti-page-type">外交家</p>', unsafe_allow_html=True)

    analyst_image = get_image_base64("images/外交.png")
    st.markdown(f"""
        <div class="mbti-card">
            <p class="mbti-page-typetitle2">🧩 外交家（INFJ、INFP、ENFJ、ENFP）🧩 </p>
            <div class="mbti-card-image">
                <img src="data:image/png;base64,{analyst_image}" style="width: 90%; margin: auto;">
            </div>
            <div style="border-bottom: 0.8px solid #ccc; margin: 15px 15px;"></div>
            <p class="mbti-card-text">外交官注重同理心和合作，在外交和咨询方面表现出色。属于这种类型的人具有合作性和想象力，通常在工作场所或社交圈中扮演协调者的角色。这些特质使外交官成为温暖、富有同情心和有影响力的人，但在需要完全依赖冷漠的理性或做出艰难决定时，这些问题就会显现出来。</p>
        </div>
    """, unsafe_allow_html=True)


col11, col12 = st.columns(2)

with col11:
    st.markdown('<p class="mbti-page-type">守护者</p>', unsafe_allow_html=True)

    # 获取守护者图片的 base64 编码
    guardian_image = get_image_base64("images/守护.png")
    st.markdown(f"""
        <div class="mbti-card">
            <p class="mbti-page-typetitle2">🧩 守护者（ISTJ、ISFJ、ESTJ、ESFJ）🧩 </p>
            <div class="mbti-card-image">
                <img src="data:image/png;base64,{guardian_image}" style="width: 90%; margin: auto;">
            </div>
            <div style="border-bottom: 0.8px solid #ccc; margin: 15px 15px;"></div>
            <p class="mbti-card-text">守护者是合作且非常务实的，无论走到哪里都会维护和创造秩序、安全和稳定。属于这些类型的人往往勤奋、细致和传统，擅长物流或行政领域，尤其是那些依赖于清晰的等级和规则的工作。这些人格类型坚持自己的计划，不回避艰巨的任务——然而，他们也可能非常固执，不愿意接受不同的观点。</p>
        </div>
    """, unsafe_allow_html=True)

with col12:
    st.markdown('<p class="mbti-page-type">探险家</p>', unsafe_allow_html=True)

    # 获取探险家图片的 base64 编码
    explorer_image = get_image_base64("images/探险.png")
    st.markdown(f"""
        <div class="mbti-card">
            <p class="mbti-page-typetitle2">🧩 探险家（ISTP、ISFP、ESTP、ESFP）🧩 </p>
            <div class="mbti-card-image">
                <img src="data:image/png;base64,{explorer_image}" style="width: 90%; margin: auto;">
            </div>
            <div style="border-bottom: 0.8px solid #ccc; margin: 15px 15px;"></div>
            <p class="mbti-card-text">探险家是最随性的，并且它们还共享一种与其他类型无法企及的方式与环境建立联系的能力。探索者是实用主义者和务实的，在需要快速反应和随机应变的情况下表现出色。他们是工具和技术的专家，以多种方式使用它们——从掌握物理工具到说服他人。毫不奇怪，这些人格类型在危机、工艺和销售中是不可替代的——然而，他们的特质也可能将他们推向冒险的境地或专注于感官享受。</p>
        </div>
    """, unsafe_allow_html=True)


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