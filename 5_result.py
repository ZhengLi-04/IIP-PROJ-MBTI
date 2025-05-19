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


# ============ 新增数据结构 ============
PERSONALITY_DATA = {
    "INTJ": {
        "tagline": "富有想象力和战略性思维，一切皆在计划之中。",
        "description": "INTJ是一种兼具内向、直觉、思考和判断特质的人格类型。这些深思熟虑的策略家热衷于完善生活中的细节，将创造力和理性运用到他们所做的一切事情上。他们的内心世界通常是一个私密且复杂的领域。<br><br>具有INTJ人格类型的人是智力好奇心旺盛的个体，对知识有着根深蒂固的渴望。INTJ通常重视创造性智慧、直截了当的理性和自我提升。他们始终致力于增强智力能力，通常被一种强烈的渴望所驱使，想要掌握任何引起他们兴趣的话题。<br><br>INTJ逻辑性强且思维敏捷，他们以独立思考的能力而自豪，他们有一种非凡的洞察力，能够看穿虚伪和伪善。由于他们的大脑从不停歇，这些人格类型可能会难以找到能够跟上他们对周围一切进行不间断分析的人。但当他们找到欣赏他们强烈热情和思想深度的志同道合者时，INTJ会形成深刻且富有智力刺激的关系，这些关系对他们来说珍贵非常。<br><br>",
        "quote": {"text": "思想构成了人的伟大。人只不过是一根芦苇，是自然界中最脆弱的东西，但他是一根会思考的芦苇。", "author": "布莱士·帕斯卡"},
        "strengths": ["理性主义", "博学多识", "独立自主", "坚韧不拔", "好奇心旺盛", "独创性"],
        "weaknesses": ["傲慢", "忽视情感", "过度批判", "喜好争论", "社交迟钝"],
        "celebrities": [
            {"name": "弗里德里希·尼采", "img": "INTJ_celeb1"},
            {"name": "米歇尔·奥巴马", "img": "INTJ_celeb2"},
            {"name": "埃隆·马斯克", "img": "INTJ_celeb3"}
        ]
    },
    "INTP": {
        "tagline": "富有创造力的发明家，对知识有着不可抑制的渴望。",
        "description": "INTP是一种具有内向、直觉、思考和展望特质的人格类型。这些思维灵活的人喜欢在生活的许多方面采取非传统的方式。他们常常寻找不寻常的道路，将勇于尝试的意愿与个人创造力相结合。<br><br>具有INTP人格类型的人为他们独特的视角和敏锐的智慧感到自豪。他们总是对宇宙的奥秘感到困惑不解——这也许可以解释为什么一些有史以来最具影响力的哲学家和科学家都是INTP。<br><br>INTP人格类型的人通常更喜欢独处，因为当他们独自一人时，很容易沉浸在自己的思绪中。他们还极具创造力和发明才能，不害怕表达他们新颖的思维方式或在众人中脱颖而出。<br><br>",
        "quote": {"text": "重要的是不要停止提问。好奇心有其存在的理由。", "author": "阿尔伯特・爱因斯坦"},
        "strengths": ["善于分析", "独创", "思维开放", "好奇", "寻求真实"],
        "weaknesses": ["疏离", "不易共情", "不安于现状", "过度思考", "缺乏耐心"],
        "celebrities": [
            {"name": "比尔·盖茨", "img": "INTP_celeb1"},
            {"name": "克里斯汀·斯图尔特", "img": "INTP_celeb2"},
            {"name": "阿尔伯特・爱因斯坦", "img": "INTP_celeb3"}
        ]
    },
    "ENTJ": {
        "tagline": "敢作敢当、天马行空且意志坚如磐石的卓越领导者，无论前方是荆棘满途还是无路可走，他们皆能逢山开路、遇水搭桥。",
        "description": "ENTJ人格类型的特点是外向、直觉、思考和判断。他们是果断决策者，热衷于发展动力和成就。在采取行动前，他们会收集信息来构建创意愿景，但很少长时间犹豫不决。<br><br>ENTJ人格类型的人是天生的领导者，拥有非凡的魅力和自信，以权威的方式引领众人达成共同目标。这些性格的人也以高度的理性为特点，凭借强大的动力、坚定的决心和敏锐的头脑来实现他们设定的任何目标。他们的强度可能有时会让他人反感，但最终，ENTJ 为自己的工作道德和令人印象深刻的高度自律感到自豪。<br><br>",
        "quote": {"text": "你的生命有限，切勿浪费时间去过别人想要的生活。", "author": "史蒂夫・乔布斯"},
        "strengths": ["高效", "精力充沛", "自信", "意志坚强", "富有战略眼光", "擅长鼓舞人心"],
        "weaknesses": ["固执专横", "不容异见", "没耐心", "自大", "处理情绪能力差", "冷酷理性"],
        "celebrities": [
            {"name": "史蒂夫・乔布斯", "img": "ENTJ_celeb1"},
            {"name": "戈登·拉姆齐", "img": "ENTJ_celeb2"},
            {"name": "玛格丽特·希尔达·撒切尔", "img": "ENTJ_celeb3"}
        ]
    },
    "ENTP": {
        "tagline": "聪明好奇的思考者，无法抵挡智力挑战的诱惑。",
        "description": "ENTP是一种外向型、直觉型、思考型和前瞻性的人格类型。他们倾向于勇敢且富有创造力，以极大的心智灵活性解构和重建思想。尽管可能会遇到任何阻力，他们仍然奋力追求目标。<br><br>思维敏捷且大胆的ENTP不怕与现状相悖。事实上，他们几乎不怕与任何事物或任何人意见相左。没有什么比言辞交锋更能点燃这些人格类型的热情了——如果谈话转向有争议的领域，那就更好了。<br><br>然而，认为ENTP不讨人喜欢或心存恶意那就错了。相反，这种人格类型的人知识渊博且充满好奇心，有一种玩世不恭的幽默感，并且可以非常有趣。他们只是有一种与众不同的、反传统的乐趣观念——一种通常涉及充满活力的辩论的观念。<br><br>",
        "quote": {"text": "走在不设限的独立思考之路上，将你的想法暴露在争议的危险中。说出你的想法，不要害怕 “傻瓜 ”的标签，而要害怕从众的耻辱。", "author": "托马斯·沃森"},
        "strengths": ["知识渊博", "思维敏捷", "富有创造力", "优秀的头脑风暴者", "富有魅力", "精力充沛"],
        "weaknesses": ["好争论", "不敏感", "不容异见", "难以专注", "不喜欢实际事务"],
        "celebrities": [
            {"name": "阿尔·杨科维克", "img": "ENTP_celeb1"},
            {"name": "亚当·萨维奇", "img": "ENTP_celeb2"},
            {"name": "萨拉·丝沃曼", "img": "ENTP_celeb3"}
        ]
    },
    "INFJ": {
        "tagline": "静谧幽深，却能启迪众人，孜孜不倦的理想主义者。",
        "description": "INFJ是一种内向型、直觉型、情感型和判断型的人格类型。他们倾向于以深思熟虑和富有想象力的方式对待生活。他们的内心愿景、个人价值观以及一种安静、有原则的人道主义精神在各个方面指引着他们。<br><br>理想主义且有原则的INFJ不满足于随波逐流，他们希望站出来有所作为。对于这些富有同情心的人格类型来说，成功并非来自金钱或地位，而是源于追求满足感、帮助他人以及成为世间行善的力量。<br><br>尽管他们有着崇高的目标和雄心，但不要把INFJ误认为是空想家。这种人格类型的人重视正直，他们往往在做了自认为正确的事情之前都不会感到满足。他们骨子里认真负责，秉持着清晰的价值观度过一生，并力求永不偏离真正重要的事物。这不是按照他人或整个社会的标准，而是依照他们自己的智慧和直觉。<br><br>",
        "quote": {"text": "用你期望他人成为的样子来对待他们，你就能帮助他们成为他们所能成为的人。", "author": "约翰·沃尔夫冈·冯·歌德"},
        "strengths": ["善于洞察", "坚持原则", "充满激情", "利他主义", "富有创造力"],
        "weaknesses": ["对批评敏感", "不愿敞开心扉", "追求完美", "逃避平凡", "易心力交瘁"],
        "celebrities": [
            {"name": "马丁·路德·金", "img": "INFJ_celeb1"},
            {"name": "纳尔逊·曼德拉", "img": "INFJ_celeb2"},
            {"name": "特蕾莎修女", "img": "INFJ_celeb3"}
        ]
    },
    "INFP": {
        "tagline": "富有诗意、善良且无私的人，总是热衷于帮助正义事业。",
        "description": "INFP是一种内向型、直觉型、情感型和开放型的人格类型。这种罕见的人格类型的人往往安静、开放且富有想象力，他们以关怀和创造性的态度对待所做的一切。<br><br>尽管INFP型人格的人可能看似安静或不张扬，但他们内心有着丰富而热烈的情感生活。他们富有创造力和想象力，乐于沉浸在白日梦中，在脑海中编织各种故事和对话。INFP以其敏感著称，这些人格类型的人对音乐、艺术、自然以及周围的人有着深刻的情感反应。他们以极其感性和怀旧而闻名，常常保存着特别的纪念品和纪念物，这些能照亮他们的日子，让内心充满喜悦。<br><br>理想主义且富有同理心的INFP型人格渴望深厚而富有灵性的关系，并且感到有责任去帮助他人。由于社会的快节奏和竞争性本质，他们有时可能会感到孤独或被忽视，在一个似乎不欣赏他们独特品质的世界里漂泊不定。然而，正是因为INFP充满了丰富的敏感性和深刻的创造力，他们才拥有与众不同的潜力去建立深厚的联系并推动积极的变革。<br><br>",
        "quote": {"text": "闪光的未必都是金子；流浪者未必都迷失了方向；强者未必会走向衰弱；深根不会被霜冻伤。", "author": "J.R.R.托尔金"},
        "strengths": ["富有同理心", "慷慨大方", "思想开放", "富有创造力", "充满激情", "理想主义"],
        "weaknesses": ["不切实际", "自我孤立", "注意力不集中", "情感脆弱", "过于取悦他人", "自我批评"],
        "celebrities": [
            {"name": "J.R.R.托尔金", "img": "INFP_celeb1"},
            {"name": "威廉·莎士比亚", "img": "INFP_celeb2"},
            {"name": "艾丽西亚·凯斯", "img": "INFP_celeb3"}
        ]
    },
    "ENFJ": {
        "tagline": "魅力非凡、振奋人心的卓越领导者，他们的话语总是娓娓动听，引人入胜，令听众如痴如醉，沉浸其中。",
        "description": "ENFJ是一种外向型、直觉型、情感型和判断型的人格类型。这些热情、直率的人喜欢帮助他人，往往拥有强烈的观念和价值观。他们以富有创意的精力推动目标实现，支持自己的观点。<br><br>ENFJ人格类型的人觉得自己有责任去服务更高的人生目标。他们心思缜密且理想主义，努力对他人的生活和周围世界产生积极影响。这种人格类型的人很少会回避做正确事情的机会，即使这样做远非易事。<br><br>ENFJ人格是天生的领导者，这解释了为什么在许多著名的政治家、教练和教师中都能找到这种人格类型。他们的热情和魅力使他们能够在职业生涯以及生活的各个领域，包括人际关系中激励他人。对于ENFJ型人格的人来说，没有什么比引导朋友和亲人成长，成为最好的自己更能带来深深的喜悦和满足感了。<br><br>",
        "quote": {"text": "当全世界都保持沉默时，即使一个声音也会变得强大。", "author": "马拉拉·尤萨夫扎伊"},
        "strengths": ["善于接纳", "值得信赖", "充满激情", "利他主义", "富有魅力"],
        "weaknesses": ["不切实际", "过于理想主义", "居高临下", "过于认真", "过度共情"],
        "celebrities": [
            {"name": "贝拉克·奥巴马", "img": "ENFJ_celeb1"},
            {"name": "奥普拉·温弗瑞", "img": "ENFJ_celeb2"},
            {"name": "约翰·库萨克", "img": "ENFJ_celeb3"}
        ]
    },
    "ENFP": {
        "tagline": "热情似火、别出心裁且在社交中左右逢源的自由灵魂，无论面对何种境遇，他们皆能乐天知命，笑口常开，用灿烂的笑容点亮生活的每一处角落。",
        "description": "ENFP是一种具有外向、直觉、情感和前瞻性特质的人格类型。这类人倾向于接受那些能够反映他们对他人的希望和善意的重大想法和行动。他们充满活力的能量可以流向许多方向。<br><br>拥有ENFP人格类型的人是真正的自由精神——外向、心胸开阔、思想开放。凭借其活泼、乐观的生活方式，ENFP在任何人群中都格外引人注目。然而，即使他们可能是派对的焦点，他们也不仅仅关心享乐。这些人格类型有着深刻的深度，这种深度源于他们与他人建立有意义的情感联系的强烈渴望。<br><br>",
        "quote": {"text": "我不在乎你如何谋生，只想知道你有何渴望，是否敢追逐心中梦想。", "author": "奥里亚·蒙顿·德里默"},
        "strengths": ["好奇", "敏锐", "热情", "优秀的沟通者", "随和", "善良积极"],
        "weaknesses": ["讨好他人", "注意力不集中", "缺乏条理", "过度迁就", "过度乐观", "不安分"],
        "celebrities": [
            {"name": "小罗伯特·唐尼", "img": "ENFP_celeb1"},
            {"name": "罗宾·威廉姆斯", "img": "ENFP_celeb2"},
            {"name": "昆汀·塔伦蒂诺", "img": "ENFP_celeb3"}
        ]
    },
    "ISTJ": {
        "tagline": "脚踏实地、求真务实的践行者，以对事物的尊重和对实际的把握为准则，其可靠程度毋庸置疑。",
        "description": "ISTJ是一种具有内向、观察型、思考型和判断型特质的人格类型。这类人往往性格内敛但意志坚定，对生活持有理性的态度。他们谨慎地规划自己的行动，并以系统有序的方式加以执行。<br><br>拥有ISTJ人格类型的人言出必行、行出必果，一旦承诺了某事，他们必定会全力兑现。鉴于其负责可靠的天性，ISTJ型人格通常对结构和传统怀有深深的敬意也就不足为奇了。他们往往被那些具有明确等级制度和期望的组织、工作场所及教育环境所吸引。<br><br>虽然ISTJ型的人可能并不特别引人注目或追求关注，但他们在维持社会稳固基础方面所做的贡献却远超许多人的份额。在家庭和社区中，这类人格类型的人常常因其可靠性、务实精神以及在最紧张的情况下仍能保持冷静和理智的能力而赢得他人的尊重。<br><br>",
        "quote": {"text": "我更害怕不运用我所拥有的能力。我更害怕拖延和懒惰。", "author": "丹泽尔·华盛顿"},
        "strengths": ["诚恳直接", "自律", "高度负责", "冷静务实", "有条理且高效", "注重研究"],
        "weaknesses": ["固执", "人情淡薄", "墨守成规", "爱评判", "易倦怠"],
        "celebrities": [
            {"name": "斯汀", "img": "ISTJ_celeb1"},
            {"name": "丹泽尔·华盛顿", "img": "ISTJ_celeb2"},
            {"name": "安格拉·默克尔", "img": "ISTJ_celeb3"}
        ]
    },
    "ISFJ": {
        "tagline": "怀揣赤胆忠心、满怀古道热肠，无论何时何地，只要所爱之人面临困境，他们定会挺身而出、义无反顾地为其遮风挡雨，全力捍卫。",
        "description": "ISFJ是一种具有内向、观察型、情感型和判断型特质的人格类型。这类人通常以自己稳定的方式表现得热情而谦逊。他们高效且负责，在日常生活中对实际细节给予细心关注。<br><br>以他们谦逊、含蓄的方式，ISFJ型人格的人帮助世界正常运转。他们勤奋且忠诚，对周围的人怀有深深的责任感。ISFJ可以被依靠去按时完成任务、记住生日和特殊场合、维护传统，并用关怀和支持的举动去关爱他们的亲人。但他们很少要求对自己所做的一切给予认可，更愿意在幕后工作。<br><br>这是一种能力出众、积极进取的人格类型，拥有丰富的多样化天赋。虽然敏感且富有同情心，但ISFJ也具备出色的分析能力和对细节的敏锐洞察力。尽管他们性格内敛，但往往拥有良好的人际交往技巧和稳固的社会关系。这些人格类型真正体现了整体大于部分之和，他们的多样化优势即使在日常生活中最平凡的方面也能闪耀光芒。<br><br>",
        "quote": {"text": "爱只有通过分享才能成长。只有把自己拥有的给予他人，自己才能拥有更多。", "author": "布莱恩·特雷西"},
        "strengths": ["支持他人", "值得信赖", "善于观察", "充满热情", "勤奋努力", "良好的实践技能"],
        "weaknesses": ["过于谦逊", "把事情放在心上", "压抑情感", "抗拒改变", "过于利他主义"],
        "celebrities": [
            {"name": "碧昂丝", "img": "ISFJ_celeb1"},
            {"name": "伊丽莎白二世", "img": "ISFJ_celeb2"},
            {"name": "艾瑞莎·弗兰克林", "img": "ISFJ_celeb3"}
        ]
    },
    "ESTJ": {
        "tagline": "出色的管理者，在管理事物或人的方面无与伦比。",
        "description": "ESTJ是一种具有外向、观察型、思考型和判断型特质的人格类型。他们拥有极大的毅力，坚定地遵循自己务实的判断。在他人中，他们常常充当稳定力量，能够在逆境中提供坚定的指引。<br><br>ESTJ型人格的人是传统和秩序的代表，他们利用对是非和社交规范的理解，将家庭和社区凝聚在一起。秉持诚实和奉献的价值观，ESTJ因其导师心态以及制定和执行计划的勤奋高效而备受珍视。他们乐于在艰难道路上引领前行，遇到压力时也不会轻易放弃。<br><br>",
        "quote": {"text": "良好的秩序是一切事物的基础。", "author": "埃德蒙·伯克"},
        "strengths": ["忠于职守", "意志坚强", "直接诚实", "忠诚、耐心且可靠", "喜欢创造秩序", "优秀的组织者"],
        "weaknesses": ["缺乏灵活性", "对变化感到不适", "爱评判", "过于关注社会地位", "难以放松", "难以表达情感"],
        "celebrities": [
            {"name": "索尼娅·索托马约尔", "img": "ESTJ_celeb1"},
            {"name": "约翰·D·洛克菲勒", "img": "ESTJ_celeb2"},
            {"name": "朱迪法官", "img": "ESTJ_celeb3"}
        ]
    },
    "ESFJ": {
        "tagline": "非常关心他人，善于社交，受人欢迎，总是乐于助人。",
        "description": "ESFJ是一种具有外向型、观察型、情感型和判断型特点的人格类型。他们注重细节、关注他人，积极融入社交圈子。他们的成就受到坚定价值观的指引，也乐于为他人提供建议。<br><br>对于ESFJ人格类型的人来说，生活中最甜蜜的时刻莫过于与他人分享。这些社交能力出众的个体构成了众多社区的基石，他们向朋友、亲人和邻居敞开心扉，也敞开了自己的心灵。<br><br>这并不意味着他们都是圣人，也不代表他们会喜欢每一个人。实际上，他们更有可能与那些有着相同价值观和观点的人建立亲密关系。然而，无论他人的信仰如何，ESFJ人格的人仍然坚信待客之道和良好礼仪的力量，并且他们往往对周围的人怀有一种责任感。他们慷慨且可靠，常常主动肩负起维系家庭和社区的重任，无论方式是大是小。<br><br>",
        "quote": {"text": "鼓励彼此，振奋彼此，增强彼此的力量。一个人散发出的积极能量，我们大家都能感受到。", "author": "黛博拉·戴"},
        "strengths": ["实用技能强", "责任感强", "非常忠诚", "温暖", "善于与人交往"],
        "weaknesses": ["担忧自身社会地位", "不灵活", "容易受到批评的伤害", "过于需要认可", "过于无私"],
        "celebrities": [
            {"name": "泰勒·斯威夫特", "img": "ESFJ_celeb1"},
            {"name": "詹妮弗·加纳", "img": "ESFJ_celeb2"},
            {"name": "比尔·克林顿", "img": "ESFJ_celeb3"}
        ]
    },
    "ISTP": {
        "tagline": "敢作敢为、脚踏实地的先锋实验者，对于各类工具，他们运用起来驾轻就熟、游刃有余。",
        "description": "ISTP是一种具有内向型、观察型、思考型和展望型特点的人格类型。他们倾向于拥有个人主义的心态，追求目标时不需要太多的外部联系。他们以好奇心和个人技能参与生活，根据需要调整方法。<br><br>ISTP型人格的人喜欢用手和眼睛探索世界，以令人印象深刻的勤奋、轻松的好奇心和健康的怀疑态度触摸和检查周围的事物。他们是天生的创造者，从一个项目转移到另一个项目，构建有用的和非必要的事物，只为乐趣，并在此过程中从环境中学习。他们最大的乐趣莫过于亲自动手拆解事物再将其重新组装，使其比之前稍有改进。<br><br>ISTP型人格的人倾向于直接解决问题，偏好直接的解决方案而非复杂的故障排除方法。他们主要依赖亲身经验和反复试验来执行想法和项目。在此过程中，他们通常更愿意按照自己的节奏和条件工作，避免不必要的干扰。这种类型的人并不热衷于超出必要范围的社交活动，因为他们试图实现自己的目标。事实上，ISTP型人格的人通常觉得常规的社交活动令人疲惫。而且，当他们确实决定与人相聚时，他们几乎总是会选择更小规模、更有意义的互动，而非肤浅的人脉拓展。<br><br>",
        "quote": {"text": "我想过一种不同的生活。我不想每天去同一个地方，见同样的人，做同样的工作。我渴望有趣的挑战。", "author": "哈里森·福特"},
        "strengths": ["勤奋且观察入微", "足智多谋", "随性", "直接真诚", "独立", "脚踏实地"],
        "weaknesses": ["毫不掩饰", "缺乏同理心", "缄默", "容易感到无聊", "过于独立", "过于怀疑"],
        "celebrities": [
            {"name": "奥利维亚·王尔德", "img": "ISTP_celeb1"},
            {"name": "贝尔·格里尔斯", "img": "ISTP_celeb2"},
            {"name": "迈克尔·乔丹", "img": "ISTP_celeb3"}
        ]
    },
    "ISFP": {
        "tagline": "灵动有魅力的艺术家，时刻准备着探索和体验新鲜事物。",
        "description": "ISFP是一种具有内向型、观察型、情感型和展望型特点的人格类型。他们倾向于思想开放，以脚踏实地的热忱对待生活、新体验和他人。他们能够活在当下的能力帮助他们发现令人兴奋的可能性。<br><br>ISFP型人格的人是真正的艺术家——尽管不一定是传统意义上的艺术家。对于这种人格类型的人来说，生活本身就是一块自我表达的画布。从他们的穿着到如何度过闲暇时光，他们的行为方式生动地反映了他们作为独特个体的特质。凭借他们探索的精神和在日常生活中寻找快乐的能力，ISFP型人格的人可能是你所遇到的最有趣的个体之一。<br><br>受公平意识和开放心态的驱使，ISFP型人格的人带着一种富有感染力的鼓励态度走过人生。他们喜欢激励身边的人追随自己的热情，通常也会以同样无拘无束的热情追求自己的兴趣。ISFP型人格的人往往认为自己只是“做自己的事”，但他们可能甚至没有意识到自己有多了不起。<br><br>",
        "quote": {"text": "我每天都会变化。清晨醒来时，我是这样的人；等到入睡时，我确信自己变成了另一个人。", "author": "鲍勃·迪伦"},
        "strengths": ["富有魅力", "善解人意", "友善", "富有想象力", "充满热情"],
        "weaknesses": ["难以适应死板环境", "难以预测", "容易压力过大", "技术能力较弱", "自我价值感波动"],
        "celebrities": [
            {"name": "拉娜·德雷", "img": "ISFP_celeb1"},
            {"name": "艾薇儿·拉维尼", "img": "ISFP_celeb2"},
            {"name": "凯文·科斯特纳", "img": "ISFP_celeb3"}
        ]
    },
    "ESTP": {
        "tagline": "足智多谋，精力旺盛且洞察力极强，沉醉于在险境边缘游走，乐在险中。",
        "description": "ESTP是一种具有外向型、观察型、思考型和展望型特点的人格类型。他们精力充沛且行动导向，能够巧妙地应对眼前的任何事物。无论是在与他人社交还是在个人追求中，他们都热衷于发现生活中的机会。<br><br>ESTP型人格的人是充满活力的个体，洋溢着热情和自发的能量。他们通常具有竞争性，常常认为竞争心态是实现人生成功的一个必要条件。他们具有积极进取、行动导向的态度，很少浪费时间思考过去。实际上，他们非常擅长将注意力集中在当下——以至于他们很少会一整天都陷入对时间的执着中。<br><br>理论、抽象概念以及对全球问题及其影响的冗长讨论，无法使ESTP人格的人保持长久的兴趣。他们让对话充满活力，且具有相当的智慧，但他们更喜欢谈论实际存在的事物——或者更好的是，直接走出去亲身体验。他们通常会“先行动后思考”，在行动中纠正错误，而不是无所事事地制定各种应急计划和退出策略。<br><br>",
        "quote": {"text": "生活要么是一次大胆的冒险，要么什么都不是。", "author": "海伦·凯勒"},
        "strengths": ["大胆无畏", "理性务实", "富有创造力", "敏锐洞察", "直接坦率", "善于社交"],
        "weaknesses": ["缺乏情感敏感性", "缺乏耐心", "冲动", "忽视规则", "忽视整体", "叛逆"],
        "celebrities": [
            {"name": "欧内斯特·海明威", "img": "ESTP_celeb1"},
            {"name": "杰克·尼科尔森", "img": "ESTP_celeb2"},
            {"name": "艾迪·墨菲", "img": "ESTP_celeb3"}
        ]
    },
    "ESFP": {
        "tagline": "洒脱不羁、朝气蓬勃，心中似有一团时刻燃烧的热情如火，在他们身旁，生活仿若一场趣味盎然的奇妙旅程，处处充满惊喜。",
        "description": "ESFP型人格具有外向型、观察型、情感型和展望型特质。这类人热爱充满活力的体验，热切地投入生活，享受探索未知的乐趣。他们通常很健谈，经常鼓励他人参与共同活动。<br><br>在所有人格类型中，ESFP型的人最容易自发地引吭高歌、翩翩起舞。他们沉浸在当下的兴奋中，并希望周围的人也能同样感受到这份热情。在鼓励他人方面，没有其他类型的人能像他们这样慷慨地投入时间和精力，也没有其他类型的人能像他们这样以无法抗拒的魅力去做这件事。<br><br>",
        "quote": {"text": "毫不犹豫地度过每一秒。", "author": "伊尔顿·约翰"},
        "strengths": ["大胆", "独特", "积极热情", "专注当下", "出色的人际交往"],
        "weaknesses": ["敏感", "回避冲突", "容易厌倦", "不擅长规划", "难以专注"],
        "celebrities": [
            {"name": "艾尔顿·约翰", "img": "ESFP_celeb1"},
            {"name": "玛丽莲·梦露", "img": "ESFP_celeb2"},
            {"name": "杰米·奥利弗", "img": "ESFP_celeb3"}
        ]
    }
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