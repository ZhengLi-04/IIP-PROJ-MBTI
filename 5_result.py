import streamlit as st
import base64

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
    * {
        font-family: "Source Sans Pro", "PingFang SC",  -apple-system, BlinkMacSystemFont, sans-serif !important;
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
    .result-page-text {
        font-size: calc(12px + 0.25vw) !important;
        margin-bottom: calc(0px + 0.25vw) !important;
        margin: 0 10px !important;
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

st.markdown('<p class="mbti-page-bigtitle">结果解读</p>', unsafe_allow_html=True)
st.caption("🚀 MBTI 是一种基于荣格心理类型理论发展而来的性格测评工具，通过分析个人在四个维度上的偏好，将人格划分为十六种类型。")


# ... 保持原有样式代码不变 ...

# ============ 新增数据结构 ============
PERSONALITY_DATA = {
    "INTJ": {
        "tagline": "富有想象力和战略性思维，一切皆在计划之中。",  # 一句话评价
        "description": """
            INTJ是一种兼具内向、直觉、思考和判断特质的人格类型。这些深思熟虑的策略家热衷于完善生活中的细节，将创造力和理性运用到他们所做的一切事情上。他们的内心世界通常是一个私密且复杂的领域。<br><br>
            具有INTJ人格类型的人是智力好奇心旺盛的个体，对知识有着根深蒂固的渴望。INTJ通常重视创造性智慧、直截了当的理性和自我提升。他们始终致力于增强智力能力，通常被一种强烈的渴望所驱使，想要掌握任何引起他们兴趣的话题。 <br><br>
            INTJ逻辑性强且思维敏捷，他们以独立思考的能力而自豪.他们有一种非凡的洞察力，能够看穿虚伪和伪善。由于他们的大脑从不停歇，这些人格类型可能会难以找到能够跟上他们对周围一切进行不间断分析的人。但当他们找到欣赏他们强烈热情和思想深度的志同道合者时，INTJ会形成深刻且富有智力刺激的关系，这些关系对他们来说珍贵非常。 <br><br>
        """, 
        "quote": {"text": "思想构成了人的伟大。人只不过是一根芦苇，是自然界中最脆弱的东西，但他是一根会思考的芦苇。", "author": "布莱士·帕斯卡"},  # 名人名言
        "strengths": ["理性主义", "博学多识", "独立自主","坚韧不拔", "好奇心旺盛", "独创性"],  # 优点
        "weaknesses": ["傲慢", "忽视情感", "过度批判", "喜好争论","社交迟钝"],  # 缺点
        "celebrities": [  # 名人列表（对应图片路径）
            {"name": "弗里德里希·尼采", "img": "INTJ_celeb1"},
            {"name": "米歇尔·奥巴马", "img": "INTJ_celeb2"},
            {"name": "埃隆·马斯克", "img": "INTJ_celeb3"}
        ]
    },
    # 在此补充其他15种类型的数据...
}

# ============ 新增展示函数 ============
def show_personality_analysis(mbti_type):
    data = PERSONALITY_DATA.get(mbti_type, {})
    
    with st.container():
        # 顶部卡片 - Tagline + Quote
        with st.container():
            # 顶部卡片 - Tagline + Quote
            st.markdown(f"""
            <div class="mbti-card">
                <p class="mbti-page-typetitle">🌟 {mbti_type} 人格特点</p>
                <div style="border-bottom: 1px dashed #eee; margin: 15px 0;"></div>
                <p class="mbti-page-title">🔖 个性标签</p>
                <p class="result-page-text">{data.get('tagline', '')}</p>
                <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; margin:20px 0;">
                    <p class="result-page-text" style="font-style: italic;">"{data.get('quote', {}).get('text', '')}"</p>
                    <p class="result-page-text" style="text-align: right; color: #666;">—— {data.get('quote', {}).get('author', '')}</p>
                </div>
            </div>  <!-- 添加闭合标签 -->
            """, unsafe_allow_html=True)

        # 类型描述（卡片外）
        st.markdown(f'<p class="mbti-page-title" style="margin-top:30px;">📌 类型解析</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="result-page-text">{data.get("description", "")}</p>', unsafe_allow_html=True)

        # 优点缺点分栏
        col_sw, col_sw2 = st.columns(2)
        with col_sw:
            st.markdown(f"""
            <div class="mbti-card">
                <p class="mbti-page-title">✅ 核心优势</p>
                <ul style="margin-left: 20px;">
                    {''.join([f'<li class="result-page-text">{s}</li>' for s in data.get("strengths", [])])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        with col_sw2:
            st.markdown(f"""
            <div class="mbti-card">
                <p class="mbti-page-title">⚠️ 发展建议</p>
                <ul style="margin-left: 20px;">
                    {''.join([f'<li class="result-page-text">{w}</li>' for w in data.get("weaknesses", [])])}
                </ul>
            </div>
            """, unsafe_allow_html=True)

        # 名人展示（三栏卡片）
        st.markdown('<p class="mbti-page-title" style="margin-top:30px;">✨ 知名人物</p>', unsafe_allow_html=True)
        celeb_cols = st.columns(3)
        for i, celeb in enumerate(data.get("celebrities", [])):
            with celeb_cols[i % 3]:
                celeb_img = get_image_base64(f"images/{celeb['img']}.png")
                st.markdown(f"""
                <div class="mbti-card">
                    <p class="result-page-text" style="text-align: center; font-weight:500;">{celeb['name']}</p>
                    <div class="mbti-card-image">
                        <img src="data:image/png;base64,{celeb_img}" style="width: 80%; border-radius: 10px;">
                    </div>
                </div>
                """, unsafe_allow_html=True)
# ============ 在原有位置调用 ============
# st.session_state.mbti_type = "INTJ"  # 示例类型，实际使用时应从会话状态中获取
if 'mbti_type' in st.session_state:
    st.markdown(f'<p class="mbti-page-type">您的 MBTI 类型是：{st.session_state.mbti_type}</p>', unsafe_allow_html=True)
    show_personality_analysis(st.session_state.mbti_type)  # 传入当前类型
else:
    st.warning("未找到 MBTI 类型信息，请先进行测试。")

# ... 保持原有底部导航代码不变 ...

# st.markdown('<p class="mbti-page-title">📃 理论基础</p>', unsafe_allow_html=True)

# st.markdown('<p class="result-page-text">MBTI，全称 Myers-Briggs Type Indicator，中文翻译为“迈尔斯-布里格斯类型指标”，是一种基于瑞士心理学家卡尔·荣格的心理类型理论发展出来的人格测评工具。最早由美国作家伊莎贝尔·布里格斯·迈尔斯和她的母亲凯瑟琳·库克·布里格斯在 20 世纪 40 年代编制而成。它主要用于测量和描述个人偏好和行为模式，帮助人们更好地理解自己的性格特点，并在职业、教育和人际关系等方面做出更好的决策。</p>', unsafe_allow_html=True)

# st.divider()

# st.markdown('<p class="mbti-page-title">📝 类别介绍</p>', unsafe_allow_html=True)

# st.markdown('<p class="result-page-text">MBTI 通过四个维度——能量获得途径（外向 E 与内向 I）、认识世界（实感 S 与直觉 N）、判断事物（思维 T 与情感 F）以及生活态度（判断 J 与知觉 P）的组合，将人格划分为十六种可能的类型。这种划分不仅帮助人们更深入地了解自己的性格特征、价值观和行为习惯，还为人们提供了一个框架，以更好地理解和欣赏他人的差异。</p>', unsafe_allow_html=True)

# st.markdown('<p class="mbti-page-type">能量获得途径</p>', unsafe_allow_html=True)

# st.markdown('<p class="result-page-text">这方面展示了我们如何与周围环境互动：</p>', unsafe_allow_html=True)

# col1, col2 = st.columns(2)

# with col1:
#     # 获取内向图片的 base64 编码
#     intro_image = get_image_base64("images/16personalities_trait_introverted.png")
#     st.markdown(f"""
#         <div class="mbti-card">
#             <p class="mbti-page-typetitle">🤫 内向 Introverted 🤫</p>
#             <div class="mbti-card-image">
#                 <img src="data:image/png;base64,{intro_image}" style="width: 80%; margin: auto;">
#             </div>
#             <div style="border-bottom: 0.8px solid #ccc; margin: 15px 15px;"></div>
#             <p class="mbti-card-text">内向型个体更喜欢独处活动，而社交互动会让他们感到疲惫。他们通常对外部刺激（例如声音、视觉或气味）比较敏感。</p>
#         </div>
#     """, unsafe_allow_html=True)

# with col2:
#     # 获取外向图片的 base64 编码
#     extro_image = get_image_base64("images/16personalities_trait_extraverted.png")
#     st.markdown(f"""
#         <div class="mbti-card">
#             <p class="mbti-page-typetitle">🤗 外向 Extraverted 🤗</p>
#             <div class="mbti-card-image">
#                 <img src="data:image/png;base64,{extro_image}" style="width: 80%; margin: auto;">
#             </div>
#             <div style="border-bottom: 0.8px solid #ccc; margin: 15px 15px;"></div>
#             <p class="mbti-card-text">外向型个体更喜欢群体活动，而社交互动会给他们带来活力。他们通常比内向型人更有热情，也更容易兴奋。</p>
#         </div>
#     """, unsafe_allow_html=True)


# st.markdown('<p class="mbti-page-type">信息感知方式</p>', unsafe_allow_html=True)

# st.markdown('<p class="result-page-text">这个方面决定了我们如何看待世界以及如何处理信息：</p>', unsafe_allow_html=True)

# col3, col4 = st.columns(2)

# with col3:
#     # 获取实感图片的 base64 编码
#     sensing_image = get_image_base64("images/16personalities_trait_observant.png")
#     st.markdown(f"""
#         <div class="mbti-card">
#             <p class="mbti-page-typetitle">🔍 实感 Sensing 🔍</p>
#             <div class="mbti-card-image">
#                 <img src="data:image/png;base64,{sensing_image}" style="width: 80%; margin: auto;">
#             </div>
#             <div style="border-bottom: 0.8px solid #ccc; margin: 15px 15px;"></div>
#             <p class="mbti-card-text">实感型的人非常实际、务实和脚踏实地。他们倾向于有强烈的习惯，并关注正在发生的事情或已经发生的事情。</p>
#         </div>
#     """, unsafe_allow_html=True)

# with col4:
#     # 获取直觉图片的 base64 编码
#     intuition_image = get_image_base64("images/16personalities_trait_intuitive.png")
#     st.markdown(f"""
#         <div class="mbti-card">
#             <p class="mbti-page-typetitle">🔮 直觉 Intuition 🔮</p>
#             <div class="mbti-card-image">
#                 <img src="data:image/png;base64,{intuition_image}" style="width: 80%; margin: auto;">
#             </div>
#             <div style="border-bottom: 0.8px solid #ccc; margin: 15px 15px;"></div>
#             <p class="mbti-card-text">直觉型的人非常富有想象力、思想开放且充满好奇心。他们更倾向于新奇而非稳定，关注隐藏的意义和未来的可能性。</p>
#         </div>
#     """, unsafe_allow_html=True)

# st.markdown('<p class="mbti-page-type">处理信息的决策方式</p>', unsafe_allow_html=True)

# st.markdown('<p class="result-page-text">这个方面决定了我们做决定和应对情绪的方式：</p>', unsafe_allow_html=True)

# col5, col6 = st.columns(2)
# with col5:
#     # 获取思维图片的 base64 编码
#     thinking_image = get_image_base64("images/16personalities_trait_thinking.png")
#     st.markdown(f"""
#         <div class="mbti-card">
#             <p class="mbti-page-typetitle">🧠 思考 Thinking 🧠</p>
#             <div class="mbti-card-image">
#                 <img src="data:image/png;base64,{thinking_image}" style="width: 80%; margin: auto;">
#             </div>
#             <div style="border-bottom: 0.8px solid #ccc; margin: 15px 15px;"></div>
#             <p class="mbti-card-text">思考者注重客观性和理性，优先考虑逻辑而非情感。他们倾向于隐藏自己的感受，并认为效率比合作更重要。</p>
#         </div>
#     """, unsafe_allow_html=True)
# with col6:
#     # 获取情感图片的 base64 编码
#     feeling_image = get_image_base64("images/16personalities_trait_feeling.png")
#     st.markdown(f"""
#         <div class="mbti-card">
#             <p class="mbti-page-typetitle">❤️ 情感 Feeling ❤️</p>
#             <div class="mbti-card-image">
#                 <img src="data:image/png;base64,{feeling_image}" style="width: 80%; margin: auto;">
#             </div>
#             <div style="border-bottom: 0.8px solid #ccc; margin: 15px 15px;"></div>
#             <p class="mbti-card-text">感性个体敏感且情感丰富。与思考型相比，他们更有同情心，竞争性较低，注重社会和谐与合作。</p>
#         </div>
#     """, unsafe_allow_html=True)


# st.markdown('<p class="mbti-page-type">与周围世界的接触方式</p>', unsafe_allow_html=True)

# st.markdown('<p class="result-page-text">这个方面反映了我们对待工作、规划和决策的方式：</p>', unsafe_allow_html=True)

# col7, col8 = st.columns(2)
# with col7:
#     # 获取判断图片的 base64 编码
#     judging_image = get_image_base64("images/16personalities_trait_judging.png")
#     st.markdown(f"""
#         <div class="mbti-card">
#             <p class="mbti-page-typetitle">📋 判断 Judging 📋</p>
#             <div class="mbti-card-image">
#                 <img src="data:image/png;base64,{judging_image}" style="width: 80%; margin: auto;">
#             </div>
#             <div style="border-bottom: 0.8px solid #ccc; margin: 15px 15px;"></div>
#             <p class="mbti-card-text">判断型个体喜欢有序和结构化的生活方式。他们倾向于提前计划，并在做决定时依赖逻辑和分析。</p>
#         </div>
#     """, unsafe_allow_html=True)

# with col8:
#     # 获取知觉图片的 base64 编码
#     perceiving_image = get_image_base64("images/16personalities_trait_prospecting.png")
#     st.markdown(f"""
#         <div class="mbti-card">
#             <p class="mbti-page-typetitle">🕊️ 感知 Perceiving 🕊️</p>
#             <div class="mbti-card-image">
#                 <img src="data:image/png;base64,{perceiving_image}" style="width: 80%; margin: auto;">
#             </div>
#             <div style="border-bottom: 0.8px solid #ccc; margin: 15px 15px;"></div>
#             <p class="mbti-card-text">感知型个体非常擅长即兴发挥和发现机会。他们倾向于灵活、放松的非传统者，更喜欢保持选择余地。</p>
#         </div>
#     """, unsafe_allow_html=True)

# st.divider()

# st.markdown('<p class="mbti-page-title">👥 类型组</p>', unsafe_allow_html=True)

# col9, col10 = st.columns(2)
# with col9:
#     st.markdown('<p class="mbti-page-type">分析家</p>', unsafe_allow_html=True)

#     # 获取分析家图片的 base64 编码
#     analyst_image = get_image_base64("images/分析.png")
#     st.markdown(f"""
#         <div class="mbti-card">
#             <p class="mbti-page-typetitle2">🧩 分析家（INTJ、INTP、ENTJ、ENTP）🧩 </p>
#             <div class="mbti-card-image">
#                 <img src="data:image/png;base64,{analyst_image}" style="width: 90%; margin: auto;">
#             </div>
#             <div style="border-bottom: 0.8px solid #ccc; margin: 15px 15px;"></div>
#             <p class="mbti-card-text">这些人格类型崇尚理性和公正，擅长智力辩论和科学或技术领域。他们非常独立、思想开放、意志坚定且富有想象力，从功利主义的角度看待许多事物，并且比满足所有人更关心什么有效。这些特质使分析师成为出色的战略思考者，但在社交或浪漫追求方面也会带来困难。</p>
#         </div>
#     """, unsafe_allow_html=True)

# with col10:
#     st.markdown('<p class="mbti-page-type">外交家</p>', unsafe_allow_html=True)

#     analyst_image = get_image_base64("images/外交.png")
#     st.markdown(f"""
#         <div class="mbti-card">
#             <p class="mbti-page-typetitle2">🧩 外交家（INFJ、INFP、ENFJ、ENFP）🧩 </p>
#             <div class="mbti-card-image">
#                 <img src="data:image/png;base64,{analyst_image}" style="width: 90%; margin: auto;">
#             </div>
#             <div style="border-bottom: 0.8px solid #ccc; margin: 15px 15px;"></div>
#             <p class="mbti-card-text">外交官注重同理心和合作，在外交和咨询方面表现出色。属于这种类型的人具有合作性和想象力，通常在工作场所或社交圈中扮演协调者的角色。这些特质使外交官成为温暖、富有同情心和有影响力的人，但在需要完全依赖冷漠的理性或做出艰难决定时，这些问题就会显现出来。</p>
#         </div>
#     """, unsafe_allow_html=True)


# col11, col12 = st.columns(2)

# with col11:
#     st.markdown('<p class="mbti-page-type">守护者</p>', unsafe_allow_html=True)

#     # 获取守护者图片的 base64 编码
#     guardian_image = get_image_base64("images/守护.png")
#     st.markdown(f"""
#         <div class="mbti-card">
#             <p class="mbti-page-typetitle2">🧩 守护者（ISTJ、ISFJ、ESTJ、ESFJ）🧩 </p>
#             <div class="mbti-card-image">
#                 <img src="data:image/png;base64,{guardian_image}" style="width: 90%; margin: auto;">
#             </div>
#             <div style="border-bottom: 0.8px solid #ccc; margin: 15px 15px;"></div>
#             <p class="mbti-card-text">守护者是合作且非常务实的，无论走到哪里都会维护和创造秩序、安全和稳定。属于这些类型的人往往勤奋、细致和传统，擅长物流或行政领域，尤其是那些依赖于清晰的等级和规则的工作。这些人格类型坚持自己的计划，不回避艰巨的任务——然而，他们也可能非常固执，不愿意接受不同的观点。</p>
#         </div>
#     """, unsafe_allow_html=True)

# with col12:
#     st.markdown('<p class="mbti-page-type">探险家</p>', unsafe_allow_html=True)

#     # 获取探险家图片的 base64 编码
#     explorer_image = get_image_base64("images/探险.png")
#     st.markdown(f"""
#         <div class="mbti-card">
#             <p class="mbti-page-typetitle2">🧩 探险家（ISTP、ISFP、ESTP、ESFP）🧩 </p>
#             <div class="mbti-card-image">
#                 <img src="data:image/png;base64,{explorer_image}" style="width: 90%; margin: auto;">
#             </div>
#             <div style="border-bottom: 0.8px solid #ccc; margin: 15px 15px;"></div>
#             <p class="mbti-card-text">探险家是最随性的，并且它们还共享一种与其他类型无法企及的方式与环境建立联系的能力。探索者是实用主义者和务实的，在需要快速反应和随机应变的情况下表现出色。他们是工具和技术的专家，以多种方式使用它们——从掌握物理工具到说服他人。毫不奇怪，这些人格类型在危机、工艺和销售中是不可替代的——然而，他们的特质也可能将他们推向冒险的境地或专注于感官享受。</p>
#         </div>
#     """, unsafe_allow_html=True)


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
    st.markdown('<p class="column-title">重新测试</p>', unsafe_allow_html=True)
    
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
        if st.button('← 重新测试', key='card3'):
            st.switch_page("4_test.py")