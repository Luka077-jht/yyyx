import streamlit as st
import pandas as pd
import numpy as np
import random
import time
from datetime import datetime
import streamlit.components.v1 as components
import json
import base64
import os

# 页面配置
st.set_page_config(
    page_title="WATCheese🧀 - 剧集评分 & 推荐系统",
    page_icon="🧀",
    layout="wide"
)

# 自定义CSS样式 - 合并两个文件的样式
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
    
    .main-header {
        font-family: 'Noto Sans SC', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .show-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #1E88E5;
    }
    .rating-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    .meme-tag {
        display: inline-block;
        background-color: #FFE082;
        color: #333;
        padding: 0.3rem 0.8rem;
        margin: 0.2rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .hot-comment {
        background-color: #E3F2FD;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid #2196F3;
    }
    .score-badge {
        background-color: #4CAF50;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
    }
    .stButton button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# 初始化数据
def init_data():
    if 'ratings' not in st.session_state:
        st.session_state.ratings = {}
    if 'drag_sessions' not in st.session_state:
        st.session_state.drag_sessions = 0
    if 'last_rating' not in st.session_state:
        st.session_state.last_rating = None
    if 'shows_df' not in st.session_state:
        st.session_state.shows_df = pd.DataFrame(drama_data)
    if 'user_ratings' not in st.session_state:
        st.session_state.user_ratings = {}
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'main'  # 'main' 或 'detail'
    if 'current_drama' not in st.session_state:
        st.session_state.current_drama = None

# 创意剧集数据 - 用于AI推荐部分
drama_data = [
    {
        'name': '黑暗荣耀', 'country': '韩剧', 'genre': '悬疑,复仇', 'year': '2022', 'episodes': '16',
        'rating': '9.1', 'actors': '宋慧乔,李到晛', 'director': '安吉镐', 'binge_level': '🔥 通宵必追',
        'desc': '校园暴力受害者文东恩精心策划的复仇故事，展现人性的黑暗与救赎',
        'reason': '宋慧乔演技炸裂，复仇剧情紧张刺激，社会议题深刻',
        'mood': '紧张,思考,刺激', 'time': '晚上,深夜', 'season': '秋冬',
        'vibes': '暗黑美学,复仇爽感,社会批判', 'best_with': '🍷红酒 + 毛毯',
        'similar': '《模范出租车》《猪猡之王》', 'memorable_line': '「我需要的不是王子，而是能与我一起跳剑舞的刽子手」',
        'image': 'C:/Users/17347/Desktop/软件图片库/黑暗荣耀.jpg'
    },
    {
        'name': '爱的迫降', 'country': '韩剧', 'genre': '爱情,浪漫', 'year': '2019', 'episodes': '16',
        'rating': '8.7', 'actors': '玄彬,孙艺珍', 'director': '李政孝', 'binge_level': '💖 甜蜜暴击',
        'desc': '韩国财阀女继承人因滑翔伞事故被迫降落在朝鲜，与朝鲜军官相遇相爱的浪漫故事',
        'reason': '玄彬孙艺珍CP感十足，画面唯美，浪漫感人',
        'mood': '浪漫,开心,感动', 'time': '晚上', 'season': '冬季',
        'vibes': '冬日恋歌,跨国浪漫,命运邂逅', 'best_with': '☕热可可 + 毛绒袜',
        'similar': '《来自星星的你》《蓝色大海的传说》', 'memorable_line': '『不是偶然，而是命运』',
        'image': 'C:/Users/17347/Desktop/软件图片库/爱的迫降.jpg'
    },
    {
        'name': '鱿鱼游戏', 'country': '韩剧', 'genre': '悬疑,惊悚', 'year': '2021', 'episodes': '9',
        'rating': '8.9', 'actors': '李政宰,朴海秀', 'director': '黄东赫', 'binge_level': '🎯 一口气刷完',
        'desc': '456名负债者参与生死游戏，争夺456亿韩元奖金的人性考验',
        'reason': 'Netflix全球爆款，游戏设定新颖，人性探讨深刻',
        'mood': '紧张,刺激,思考', 'time': '晚上,深夜', 'season': '全年',
        'vibes': '生存游戏,人性实验,视觉冲击', 'best_with': '🍿爆米花 + 抱枕(紧张时抱)',
        'similar': '《弥留之国的爱丽丝》《要听神明的话》', 'memorable_line': '『我们不是牲畜，我们是人！』',
        'image': 'C:/Users/17347/Desktop/软件图片库/鱿鱼游戏.jpg'
    },
    {
        'name': '请回答1988', 'country': '韩剧', 'genre': '家庭,治愈', 'year': '2015', 'episodes': '20',
        'rating': '9.7', 'actors': '李惠利,朴宝剑', 'director': '申元浩', 'binge_level': '🏡 温暖慢炖',
        'desc': '1988年双门洞五家人的温情故事，展现邻里亲情和青春成长',
        'reason': '温暖感人，细节真实，笑中带泪的经典之作',
        'mood': '治愈,怀旧,感动', 'time': '全天', 'season': '全年',
        'vibes': '复古情怀,邻里温情,青春回忆', 'best_with': '🍜泡面 + 回忆',
        'similar': '《请回答1994》《机智的医生生活》', 'memorable_line': '『大人只是在忍，只是在忙着大人们的事』',
        'image': 'C:/Users/17347/Desktop/软件图片库/请回答1988.jpg'
    },
    {
        'name': '怪奇物语', 'country': '美剧', 'genre': '科幻,悬疑', 'year': '2016', 'episodes': '34',
        'rating': '8.7', 'actors': '米莉·博比·布朗', 'director': '杜夫兄弟', 'binge_level': '👽 奇幻冒险',
        'desc': '小镇男孩失踪引发超自然事件，一群孩子与政府阴谋对抗的故事',
        'reason': '80年代怀旧风，剧情精彩，角色鲜明',
        'mood': '紧张,刺激,怀旧', 'time': '晚上,深夜', 'season': '全年',
        'vibes': '复古科幻,少年冒险,超自然', 'best_with': '🍕披萨 + 霓虹灯',
        'similar': '《暗黑》《X档案》', 'memorable_line': '『朋友不会说谎』',
        "image": "C:/Users/17347/Desktop/软件图片库/怪奇物语.jpg"
    },
    {
        'name': '后翼弃兵', 'country': '美剧', 'genre': '剧情,励志', 'year': '2020', 'episodes': '7',
        'rating': '8.9', 'actors': '安雅·泰勒-乔伊', 'director': '斯科特·弗兰克', 'binge_level': '♟️ 智力对决',
        'desc': '天才少女棋手在男性主导的国际象棋界闯出一片天地的故事',
        'reason': '画面精美，女主魅力十足，智力对决紧张刺激',
        'mood': '振奋,思考,专注', 'time': '下午,晚上', 'season': '秋冬',
        'vibes': '女性力量,智力美学,复古时尚', 'best_with': '♟️国际象棋 + 红酒',
        'similar': '《女王的棋局》《王冠》', 'memorable_line': '『世界上最强大的棋手，是那些独处的人』',
        "image": "C:/Users/17347/Desktop/软件图片库/后翼弃兵.webp"
    },
    {
        'name': '轮到你了', 'country': '日剧', 'genre': '悬疑,推理', 'year': '2019', 'episodes': '20',
        'rating': '8.7', 'actors': '原田知世,田中圭', 'director': '佐久间纪佳', 'binge_level': '🔍 烧脑解谜',
        'desc': '公寓居民参与交换杀人游戏，引发一连串命案和谜团',
        'reason': '推理精彩，每集都有反转，悬念设置巧妙',
        'mood': '紧张,刺激,思考', 'time': '晚上,深夜', 'season': '全年',
        'vibes': '日式推理,公寓谜团,全员恶人', 'best_with': '📝笔记本(记线索) + 🍵绿茶',
        'similar': '《我的恐怖妻子》《3年A班》', 'memorable_line': '『轮到你了』',
        "image": "C:/Users/17347/Desktop/软件图片库/轮到你了.jpg"},
    {
        'name': '初恋', 'country': '日剧', 'genre': '爱情,音乐', 'year': '2022', 'episodes': '9',
        'rating': '8.5', 'actors': '满岛光,佐藤健', 'director': '寒竹百合', 'binge_level': '🎵 视听盛宴',
        'desc': '因意外失忆的女主与初恋男友跨越20年的命运爱情故事',
        'reason': '画面如电影般精美，配乐绝佳，纯爱感人',
        'mood': '浪漫,感动,怀旧', 'time': '晚上,深夜', 'season': '冬季',
        'vibes': '日式纯爱,命运重逢,音乐浪漫', 'best_with': '🎧耳机 + 🍂落叶氛围',
        'similar': '《静雪》《恋爱世纪》', 'memorable_line': '『命运就像磁铁，互相吸引』',
        'image': 'C:/Users/17347/Desktop/软件图片库/初恋.jpg'
     },
     {
        'name': '石纪元','country': '番剧','genre': '科幻,冒险,生存','year': '2019','episodes': '24',
        'rating': '8.7', 'actors': '小林裕介, 古川慎, 市之濑加那', 'director': '饭野慎也', 'binge_level': '🔬 科学复兴',
        'desc': '全人类被神秘光线石化数千年后，科学天才千空带领幸存者用科学知识重建文明',
        'reason': '创意独特，将科学知识融入冒险故事，既热血又寓教于乐',
        'mood': '思考,放松', 'time': '下午,晚上', 'season': '全年',
        'vibes': '科学精神,文明重建,团队合作', 'best_with': '🔬实验笔记 + 碳酸饮料',
        'similar': '《工作细胞》《来自深渊》',
        'memorable_line': '『这个石之世界，由我们来复活！』',
        'image': 'C:/Users/17347/Desktop/软件图片库/石纪元.png'
     },
]


# 五个评分等级
ranking_levels = {
    '夯': {'emoji': '🏆', 'color': '#FF6B6B', 'desc': '神作中的神作'},
    '顶级': {'emoji': '⭐', 'color': '#4ECDC4', 'desc': '顶级优秀作品'},
    '人上人': {'emoji': '👑', 'color': '#45B7D1', 'desc': '优秀作品'},
    'NPC': {'emoji': '😐', 'color': '#FFD93D', 'desc': '普通水平'},
    '拉完了': {'emoji': '💩', 'color': '#C9C9C9', 'desc': '浪费时间'}
}

# ========== AI推荐部分 ==========
def analyze_user_profile(choices):
    profiles = {
        '浪漫主义者': ['爱情', '浪漫', '感动'],
        '推理大师': ['悬疑', '推理', '思考'], 
        '喜剧达人': ['喜剧', '开心', '放松'],
        '冒险家': ['科幻', '奇幻', '刺激'],
        '治愈系': ['治愈', '家庭', '放松']
    }
    
    user_traits = []
    for profile, traits in profiles.items():
        if any(trait in str(choices.values()) for trait in traits):
            user_traits.append(profile)
    
    return user_traits if user_traits else ['探索者']

def generate_personalized_recommendation(drama, user_traits):
    templates = {
        '浪漫主义者': [
            f"💖 这份浪漫专为你定制！《{drama['name']}》将带你体验{random.choice(['刻骨铭心', '跨越时空', '命中注定'])}的爱情",
            f"🎯 根据你的浪漫基因，我们锁定了《{drama['name']}》- {drama['memorable_line']}"
        ],
        '推理大师': [
            f"🔍 推理达人，准备好挑战《{drama['name']}》了吗？这部剧有{random.choice(['层层反转', '精妙诡计', '意想不到'])}的谜题",
            f"🎯 你的逻辑思维会爱上《{drama['name']}》- {drama['memorable_line']}"
        ],
        '治愈系': [
            f"🌼 治愈时刻！《{drama['name']}》就像{random.choice(['冬日暖阳', '心灵按摩', '温柔拥抱'])}般温暖",
            f"🎯 为你的心灵挑选了《{drama['name']}》- {drama['memorable_line']}"
        ]
    }
    
    for trait in user_traits:
        if trait in templates:
            return random.choice(templates[trait])
    
    return f"🎯 我们为你精心匹配了《{drama['name']}》- {drama['memorable_line']}"







def show_drama_detail_expander(drama_info):
    """在当前页面内展开显示剧集详细内容"""
    
    # 直接显示详细内容，使用expander的默认展开状态
    with st.expander(f"🎬 《{drama_info['name']}》详细角色评分系统", expanded=True):
        
        # 剧集基本信息
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"### 📖 剧集信息")
            st.write(f"**国家：** {drama_info['country']}")
            st.write(f"**类型：** {drama_info['genre']}")
            st.write(f"**年份：** {drama_info['year']}")
            st.write(f"**集数：** {drama_info['episodes']}")
            st.write(f"**评分：** ⭐ {drama_info['rating']}")
            st.write(f"**导演：** {drama_info['director']}")
            st.write(f"**主演：** {drama_info['actors']}")
            
            # 显示剧集描述
            st.markdown("### 📝 剧情简介")
            st.info(drama_info['desc'])
            
            # 显示推荐理由
            st.markdown("### 💫 推荐理由")
            st.success(drama_info['reason'])
            
            # 显示经典台词
            st.markdown("### 🎙️ 经典台词")
            st.warning(f"*{drama_info['memorable_line']}*")
        
        with col2:
            # 显示剧集海报
            st.image(drama_info['image'], width=200, caption=drama_info['name'])
            
            # 显示观剧指南
            st.markdown("### 🎪 观剧指南")
            st.write(f"**最佳搭配：** {drama_info['best_with']}")
            st.write(f"**适合时段：** {drama_info['time']}")
            st.write(f"**季节氛围：** {drama_info['season']}")
            st.write(f"**情绪氛围：** {drama_info['vibes']}")
            st.write(f"**同频剧集：** {drama_info['similar']}")
        
        st.markdown("---")
        
        # 角色评分系统
        st.markdown("## 👥 角色评分系统")
        
        # 根据剧集类型生成角色数据
        characters_data = generate_characters_by_drama(drama_info)
        
        # 初始化角色评分数据
        if 'character_ratings' not in st.session_state:
            st.session_state.character_ratings = {}
        
        # 显示角色评分卡片
        for i, character in enumerate(characters_data):
            with st.container():
                col_a, col_b, col_c = st.columns([1, 2, 1])
                
                with col_a:
                    # 角色图片（使用默认图片或剧集图片）
                    character_image = drama_info['image']  # 暂时使用剧集图片
                    st.image(character_image, width=100, caption=character['name'])
                
                with col_b:
                    st.markdown(f"### {character['name']}")
                    st.write(f"**角色：** {character['role']}")
                    st.write(f"**描述：** {character['description']}")
                    
                    # 显示角色梗和热评
                    if character.get('memes'):
                        st.write("**🔥 角色梗：**")
                        for meme in character['memes'][:2]:
                            st.markdown(f'<span style="background: #FFE082; color: #333; padding: 2px 8px; border-radius: 10px; font-size: 0.8rem; margin: 2px;">{meme}</span>', unsafe_allow_html=True)
                
                with col_c:
                    # 五星评分系统
                    st.markdown("#### 角色评分")
                    current_rating = st.session_state.character_ratings.get(character['name'], 0)
                    
                    # 创建五星评分界面
                    rating_cols = st.columns(5)
                    for star in range(1, 6):
                        with rating_cols[star-1]:
                            if st.button("🌟" if star <= current_rating else "⚪", 
                                       key=f"star_{drama_info['name']}_{character['name']}_{star}"):
                                st.session_state.character_ratings[character['name']] = star
                                st.rerun()
                    
                    # 显示当前评分
                    if current_rating > 0:
                        st.markdown(f"**当前评分：** {current_rating}星")
                    
                    # 显示平均评分
                    if character.get('avg_rating'):
                        st.markdown(f"**平均评分：** ⭐ {character['avg_rating']}")
                
                st.markdown("---")
        
        # 角色评分统计
        if st.session_state.character_ratings:
            st.markdown("## 📊 评分统计")
            rated_characters = [name for name, rating in st.session_state.character_ratings.items() if rating > 0]
            if rated_characters:
                st.write(f"**已评分角色：** {len(rated_characters)}个")
                avg_rating = np.mean([rating for rating in st.session_state.character_ratings.values() if rating > 0])
                st.write(f"**平均评分：** ⭐ {avg_rating:.1f}")
                
                # 显示评分最高的角色
                if rated_characters:
                    top_character = max(st.session_state.character_ratings.items(), key=lambda x: x[1])
                    st.write(f"**最喜爱角色：** {top_character[0]} ⭐{top_character[1]}")


def generate_characters_by_drama(drama_info):
    """根据剧集信息生成对应的角色数据"""
    
    drama_name = drama_info['name']
    
    # 不同剧集的角色数据模板
    character_templates = {
        '黑暗荣耀': [
            {'name': '文东恩', 'role': '女主角', 'description': '遭受校园暴力后精心策划复仇的教师', 'avg_rating': 9.2, 'memes': ['妍珍啊', '欢迎来到我的地狱']},
            {'name': '朴妍珍', 'role': '反派', 'description': '校园暴力的主导者，气象主播', 'avg_rating': 8.1, 'memes': ['西八', '气象主播的优雅']},
            {'name': '周汝正', 'role': '男主角', 'description': '帮助文东恩的整形外科医生', 'avg_rating': 8.7, 'memes': ['整形医生的温柔', '文东恩的守护者']},
            {'name': '全在俊', 'role': '反派', 'description': '朴妍珍的丈夫，高尔夫球场代表', 'avg_rating': 7.8, 'memes': ['高尔夫球场代表', '商业精英的冷漠']},
            {'name': '李莎拉', 'role': '反派', 'description': '画家，校园暴力参与者', 'avg_rating': 7.5, 'memes': ['画家的疯狂', '毒品的奴隶']},
            {'name': '崔惠程', 'role': '反派', 'description': '空姐，校园暴力参与者', 'avg_rating': 7.3, 'memes': ['空姐的虚荣', '校园暴力的帮凶']}
        ],
        '爱的迫降': [
            {'name': '尹世理', 'role': '女主角', 'description': '韩国财阀女继承人', 'avg_rating': 8.9, 'memes': ['滑翔伞事故', '财阀千金']},
            {'name': '李正赫', 'role': '男主角', 'description': '朝鲜军官', 'avg_rating': 9.1, 'memes': ['朝鲜军官', '温柔守护']},
            {'name': '徐丹', 'role': '女配角', 'description': '李正赫的未婚妻', 'avg_rating': 8.2, 'memes': ['未婚妻', '家族联姻']},
            {'name': '具承俊', 'role': '男配角', 'description': '神秘商人', 'avg_rating': 8.5, 'memes': ['神秘商人', '跨国背景']}
        ],
        '鱿鱼游戏': [
            {'name': '成奇勋', 'role': '男主角', 'description': '负债累累的失败者', 'avg_rating': 8.8, 'memes': ['456号', '最后的赢家']},
            {'name': '曹尚佑', 'role': '男配角', 'description': '首尔大学高材生', 'avg_rating': 8.3, 'memes': ['218号', '高智商玩家']},
            {'name': '姜晓', 'role': '女主角', 'description': '脱北者', 'avg_rating': 8.7, 'memes': ['067号', '冷静机智']},
            {'name': '吴一男', 'role': '男配角', 'description': '神秘老人', 'avg_rating': 9.0, 'memes': ['001号', '游戏创始人']},
            {'name': '张德秀', 'role': '反派', 'description': '黑帮头目', 'avg_rating': 7.9, 'memes': ['101号', '暴力分子']}
        ],
        '请回答1988': [
            {'name': '成德善', 'role': '女主角', 'description': '双门洞五人帮成员', 'avg_rating': 9.5, 'memes': ['特工队', '学习成绩差']},
            {'name': '金正焕', 'role': '男主角', 'description': '双门洞五人帮成员', 'avg_rating': 9.4, 'memes': ['狗正八', '默默守护']},
            {'name': '崔泽', 'role': '男主角', 'description': '围棋天才', 'avg_rating': 9.3, 'memes': ['喜东东', '围棋天才']},
            {'name': '成善宇', 'role': '男配角', 'description': '双门洞五人帮成员', 'avg_rating': 9.0, 'memes': ['善宇', '温柔体贴']},
            {'name': '刘东龙', 'role': '男配角', 'description': '双门洞五人帮成员', 'avg_rating': 8.8, 'memes': ['娃娃鱼', '搞笑担当']}
        ]
    }
    
    # 如果剧集在模板中，使用模板数据
    if drama_name in character_templates:
        return character_templates[drama_name]
    
    # 否则根据剧集类型生成通用角色数据
    genre = drama_info['genre']
    
    if '爱情' in genre or '浪漫' in genre:
        return [
            {'name': '女主角', 'role': '主角', 'description': '爱情故事的女主角', 'avg_rating': 8.5, 'memes': ['浪漫邂逅', '命运安排']},
            {'name': '男主角', 'role': '主角', 'description': '爱情故事的男主角', 'avg_rating': 8.6, 'memes': ['温柔守护', '浪漫告白']},
            {'name': '男配角', 'role': '配角', 'description': '暗恋女主角的角色', 'avg_rating': 7.8, 'memes': ['默默付出', '单相思']},
            {'name': '女配角', 'role': '配角', 'description': '女主角的闺蜜', 'avg_rating': 7.9, 'memes': ['闺蜜情谊', '情感支持']}
        ]
    elif '悬疑' in genre or '推理' in genre:
        return [
            {'name': '侦探/主角', 'role': '主角', 'description': '解开谜团的关键人物', 'avg_rating': 8.7, 'memes': ['推理高手', '观察入微']},
            {'name': '嫌疑人A', 'role': '配角', 'description': '案件相关人物', 'avg_rating': 7.5, 'memes': ['神秘行为', '可疑举动']},
            {'name': '嫌疑人B', 'role': '配角', 'description': '案件相关人物', 'avg_rating': 7.6, 'memes': ['隐藏动机', '复杂背景']},
            {'name': '助手/搭档', 'role': '配角', 'description': '协助破案的角色', 'avg_rating': 8.2, 'memes': ['得力助手', '默契配合']}
        ]
    elif '科幻' in genre or '奇幻' in genre:
        return [
            {'name': '英雄/主角', 'role': '主角', 'description': '拯救世界的英雄', 'avg_rating': 8.8, 'memes': ['超能力', '命运之子']},
            {'name': '反派', 'role': '反派', 'description': '制造危机的反派', 'avg_rating': 8.1, 'memes': ['邪恶计划', '强大力量']},
            {'name': '伙伴', 'role': '配角', 'description': '主角的忠实伙伴', 'avg_rating': 8.3, 'memes': ['忠诚伙伴', '并肩作战']},
            {'name': '导师', 'role': '配角', 'description': '指导主角的角色', 'avg_rating': 8.4, 'memes': ['智慧长者', '经验丰富']}
        ]
    else:
        # 默认角色模板
        return [
            {'name': '主角', 'role': '主角', 'description': '故事的主要人物', 'avg_rating': 8.5, 'memes': ['成长历程', '关键决策']},
            {'name': '配角A', 'role': '配角', 'description': '重要配角', 'avg_rating': 7.8, 'memes': ['辅助作用', '个性鲜明']},
            {'name': '配角B', 'role': '配角', 'description': '次要配角', 'avg_rating': 7.5, 'memes': ['背景人物', '情节推动']},
            {'name': '反派', 'role': '反派', 'description': '对立角色', 'avg_rating': 8.0, 'memes': ['冲突制造', '复杂动机']}
        ]

def ai_recommendation_interface():
    st.markdown("## 🔮 AI智能心灵匹配")
    
    # 侧边栏 - 用户画像区
    with st.sidebar:
        st.markdown("### 🧠 心灵探测仪")
        st.write("告诉我们你的状态，AI将深度解析你的观剧DNA")
        
        st.markdown("---")
        st.markdown("#### 🎯 灵魂拷问")
        
        q1 = st.selectbox("此刻的你最像什么？" , 
                         ['开化石纪元的千空', '探求真相的网代慎平', '绿洲中的头号玩家', '踏上伟大航路的路飞', '久未进食的东京喰种', '目睹琳死亡的带土'], key="q1")
        
        q2 = st.selectbox("你希望剧集给你什么？",
                         ["一场冒险", "一个拥抱", "一次思考", "一阵欢笑"], key="q2")
        
        q3 = st.selectbox("你的观剧仪式感？",
                         ["零食配剧感觉至上", "专心致志沉浸体验", "倍速观看高燃速通", "细节分析抽丝剥茧"], key="q3")
        
        if st.button("🔮 生成观剧DNA报告", key="dna_report"):
            with st.spinner('AI正在解析你的观剧灵魂...'):
                time.sleep(2)
                
                user_profile = {
                    '开化石纪元的千空':'科普知识型观众',
                    '探求真相的网代慎平':'推理烧脑型观众',
                    '绿洲中的头号玩家':'沉浸体验型观众',
                    '踏上伟大航路的路飞':'追求刺激型观众', 
                    '久未进食的东京喰种':'无精打采型观众',
                    '目睹琳死亡的带土':'寻求治愈型观众'
                }
                
                st.balloons()
                st.success(f"### 🧬 你的观剧DNA：**{user_profile[q1]}**")
                st.write(f"**心灵需求：** {q2}")
                st.write(f"**观剧风格：** {q3}")
    
    # 创意筛选条件
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🌍 时空坐标")
        country = st.selectbox("剧集宇宙", ["全部", "韩剧", "美剧", "日剧","国产剧集", "番剧", "电影"], key="country_select")
        season = st.selectbox("季节氛围", ["全部", "春季", "夏季", "秋季", "冬季"], key="season_select")
    
    with col2:
        st.markdown("### 🎭 情绪频率")
        genre = st.selectbox("故事波长", ["全部", "爱情", "悬疑", "喜剧", "科幻", "治愈", "励志"], key="genre_select")
        mood = st.selectbox("心灵状态", ["全部", "开心", "放松", "浪漫", "感动", "紧张", "刺激", "思考"], key="mood_select")
    
    with col3:
        st.markdown("### ⏰ 观剧时空")
        time_period = st.selectbox("最佳时段", ["全部", "早晨", "中午", "下午", "晚上", "深夜"], key="time_select")
        binge_level = st.selectbox("投入程度", ["全部", "轻度观赏", "中度沉浸", "深度投入"], key="binge_select")
    
    if st.button("✨ 启动AI心灵匹配", type="primary", use_container_width=True, key="ai_match"):
        with st.spinner('🪄 AI正在从多元宇宙搜寻你的命定剧集...'):
            time.sleep(2)
            
            results = []
            for drama in drama_data:
                country_ok = (country == "全部") or (drama['country'] == country)
                genre_ok = (genre == "全部") or (genre in drama['genre'])
                mood_ok = (mood == "全部") or (mood in drama['mood'])
                time_ok = (time_period == "全部") or (time_period in drama['time'])
                season_ok = (season == "全部") or (season in drama['season'])
                
                if country_ok and genre_ok and mood_ok and time_ok and season_ok:
                    results.append(drama)
            
            if results:
                main_recommend = random.choice(results)
                
                user_choices = {'genre': genre, 'mood': mood, 'q1': q1, 'q2': q2}
                user_traits = analyze_user_profile(user_choices)
                personalized_msg = generate_personalized_recommendation(main_recommend, user_traits)
                
                st.markdown("---")
                st.markdown(f"## 🎉 **AI心灵匹配完成！**")
                st.markdown(f"### 🎯 {personalized_msg}")
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                border-radius: 15px; padding: 20px; color: white; margin: 20px 0;">
                    <h2>🎬 {main_recommend['name']}</h2>
                    <p><strong>🌍 宇宙坐标：</strong>{main_recommend['country']}</p>
                    <p><strong>📡 故事频率：</strong>{main_recommend['genre']}</p>
                    <p><strong>⭐ 心灵评分：</strong>{main_recommend['rating']}</p>
                    <p><strong>{main_recommend['binge_level']}</strong></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.image(main_recommend['image'], width=200, caption=main_recommend['name'])
                    
                    st.markdown("#### 🔗 匹配标签")
                    st.markdown(f'<span style="background: #FFD93D; color: #333; padding: 5px 15px; border-radius: 20px; font-weight: bold; display: inline-block; margin: 5px;">🏷️ {main_recommend["vibes"]}</span>', unsafe_allow_html=True)
                    st.markdown(f'<span style="background: #FFD93D; color: #333; padding: 5px 15px; border-radius: 20px; font-weight: bold; display: inline-block; margin: 5px;">🎧 {main_recommend["best_with"]}</span>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown("#### 📖 故事宇宙")
                    st.info(f"**剧情简介：** {main_recommend['desc']}")
                    
                    st.markdown("#### 💫 灵魂共鸣")
                    st.success(f"**推荐理由：** {main_recommend['reason']}")
                    
                    st.markdown("#### 🎙️ 经典回响")
                    st.warning(f"**难忘台词：** *{main_recommend['memorable_line']}*")
                    
                    st.markdown("#### 🎭 创作团队")
                    st.write(f"**导演：** {main_recommend['director']}")
                    st.write(f"**主演：** {main_recommend['actors']}")
                    st.write(f"**年份：** {main_recommend['year']} | **集数：** {main_recommend['episodes']}")
                      # 观剧仪式感
                st.markdown("---")
                st.markdown("## 🎪 沉浸式观剧指南")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("### 🍿 氛围装备")
                    st.write(f"**最佳搭配：** {main_recommend['best_with']}")
                    st.write(f"**适合：** {main_recommend['time']}时段")
                    st.write(f"**季节：** {main_recommend['season']}")
                
                with col2:
                    st.markdown("### 🎵 情绪歌单")
                    st.write("🎶 剧集原声带")
                    st.write("🎧 场景氛围音乐")
                    st.write("📻 年代怀旧金曲")
                
                with col3:
                    st.markdown("### 📚 延伸阅读")
                    st.write(f"**同频剧集：** {main_recommend['similar']}")
                    st.write("🎬 导演其他作品")
                    st.write("📖 相关影视解析")
                
                # 为每个推荐的剧集添加超链接按钮
                st.markdown("---")
                st.markdown("### 🔗 详细剧集信息")
                st.markdown(f"点击下方按钮查看《{main_recommend['name']}》的详细角色评分和评论信息：")
                
                # 使用session state跟踪按钮点击状态
                detail_key = f"show_detail_{main_recommend['name']}"
                if detail_key not in st.session_state:
                    st.session_state[detail_key] = False
                
                # 创建剧集详细页面的超链接按钮
                if st.button(f"🎬 查看《{main_recommend['name']}》详细评分", key=f"detail_{main_recommend['name']}"):
                    st.session_state[detail_key] = not st.session_state[detail_key]
                    st.rerun()
                
                # 如果按钮被点击，显示详细内容
                if st.session_state[detail_key]:
                    show_drama_detail_expander(main_recommend)
                
            else:
                st.error("""
                ### 🚫 多元宇宙信号中断
                在当前维度未找到完美匹配的剧集...
                
                **✨ 建议尝试：**
                - 调整心灵频率（筛选条件）
                - 探索新的故事波长（类型）
                - 让AI为你随机开启惊喜剧集
                """)
                
                # 随机惊喜推荐
                if st.button("🎁 开启AI惊喜盲盒", key="surprise"):
                    surprise = random.choice(drama_data)
                    st.balloons()
                    st.success(f"### 🎉 惊喜剧集：**{surprise['name']}**")
                    st.write(f"**理由：** 有时候，最好的故事出现在意料之外 ✨")
                    image_src = get_drama_image(surprise['name'])
                    if image_src:
                        st.image(image_src, width=200, caption=surprise['name'])

# ========== 拖拽评分部分 ==========
# 获取剧集图片 - 优先使用桌面图片
def get_drama_image(drama_name):
    """根据剧集名称获取桌面上的图片并转换为base64"""
    # 定义剧集名称与图片文件的映射
    image_mapping = {
        '黑暗荣耀': '黑暗荣耀.jpg',
        '爱的迫降': '爱的迫降.jpg', 
        '鱿鱼游戏': '鱿鱼游戏.jpg',
        '请回答1988': '请回答1988.jpg',
        '怪奇物语': '怪奇物语.jpg',
        '后翼弃兵': '后翼弃兵.webp',
        '轮到你了': '轮到你了.jpg',
        '初恋': '初恋.webp',
        '石纪元': '石纪元.png'
    }
    
    # 检查剧集是否在映射中
    if drama_name not in image_mapping:
        return None
    
    # 构建正确的图片路径
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    image_folder = os.path.join(desktop_path, "软件图片库")
    image_filename = image_mapping[drama_name]
    image_path = os.path.join(image_folder, image_filename)
    
    # 检查文件是否存在
    if not os.path.exists(image_path):
        print(f"警告：图片文件不存在 - {image_path}")
        return None
    
    # 将图片转换为base64
    try:
        with open(image_path, "rb") as image_file:
            base64_img = base64.b64encode(image_file.read()).decode("utf-8")
            # 根据文件扩展名设置正确的MIME类型
            if image_path.lower().endswith('.png'):
                return f"data:image/png;base64,{base64_img}"
            elif image_path.lower().endswith('.webp'):
                return f"data:image/webp;base64,{base64_img}"
            else:
                return f"data:image/jpeg;base64,{base64_img}"
    except Exception as e:
        print(f"图片读取错误: {e}")
        return None

ranking_levels = {
    '夯': {'emoji': '🏆', 'color': '#FF6B6B', 'desc': '神作中的神作'},
    '顶级': {'emoji': '⭐', 'color': '#4ECDC4', 'desc': '顶级优秀作品'},
    '人上人': {'emoji': '👑', 'color': '#45B7D1', 'desc': '优秀作品'},
    'NPC': {'emoji': '😐', 'color': '#FFD93D', 'desc': '普通水平'},
    '拉完了': {'emoji': '💩', 'color': '#C9C9C9', 'desc': '浪费时间'}
}

# HTML/JavaScript 拖拽组件 - 修复显示问题，使用本地图片
def drag_drop_component():
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .container {{
                display: flex;
                gap: 20px;
                padding: 20px;
                font-family: Arial, sans-serif;
                height: 100vh;
            }}
            .poster-section {{
                flex: 1;
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                border: 2px dashed #dee2e6;
                overflow-y: auto;
            }}
            .ranking-section {{
                flex: 2;
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                border: 2px dashed #dee2e6;
                overflow-y: auto;
                display: flex;
                flex-direction: column;
                gap: 15px;
            }}
            .poster-grid {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 15px;
                margin-top: 15px;
            }}
            .poster {{
                width: 120px;
                height: 180px;
                border-radius: 8px;
                cursor: grab;
                transition: all 0.3s ease;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                object-fit: cover;
            }}
            .poster:hover {{
                transform: scale(1.05);
                box-shadow: 0 6px 12px rgba(0,0,0,0.15);
            }}
            .poster:active {{
                cursor: grabbing;
            }}
            .ranking-level {{
                padding: 20px;
                border-radius: 10px;
                border: 2px dashed;
                min-height: 100px;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                gap: 15px;
                flex-shrink: 0;
            }}
            .ranking-level.hover {{
                background: rgba(255,255,255,0.8) !important;
                transform: scale(1.02);
            }}
            .rank-icon {{
                font-size: 24px;
            }}
            .rank-info {{
                flex: 1;
            }}
            .rank-title {{
                font-weight: bold;
                font-size: 18px;
                margin: 0;
            }}
            .rank-desc {{
                margin: 5px 0 0 0;
                font-size: 12px;
                color: #666;
            }}
            .dropped-poster {{
                width: 60px;
                height: 90px;
                border-radius: 5px;
                margin: 5px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                object-fit: cover;
            }}
            .dropped-container {{
                display: flex;
                flex-wrap: wrap;
                gap: 5px;
                margin-top: 10px;
                min-height: 100px;
                align-items: flex-start;
            }}
            .success-message {{
                position: fixed;
                top: 20px;
                right: 20px;
                background: #4CAF50;
                color: white;
                padding: 15px;
                border-radius: 5px;
                z-index: 1000;
                display: none;
            }}
        </style>
    </head>
    <body>
        <div class="success-message" id="successMessage">评分成功！</div>
        
        <div class="container">
            <!-- 左侧海报区域 -->
            <div class="poster-section">
                <h3>🎬 剧集海报</h3>
                <p>拖拽海报到右侧评分等级中</p>
                <div class="poster-grid">
    """
    
    # 添加海报 - 使用本地图片
    for drama in drama_data:
        image_src = get_drama_image(drama['name'])
        html_code += f"""
                    <img src="{image_src}" 
                         class="poster" 
                         draggable="true"
                         ondragstart="dragStart(event, '{drama['name']}')"
                         alt="{drama['name']}"
                         title="{drama['name']} - {drama['desc']}">
        """
    
    html_code += """
                </div>
            </div>
            
            <!-- 右侧评分区域 -->
            <div class="ranking-section">
                <h3>📊 评分等级</h3>
                <p>将海报拖拽到对应的等级中</p>
    """
    
    # 添加五个评分等级 - 确保全部显示
    for rank, info in ranking_levels.items():
        html_code += f"""
                <div class="ranking-level" 
                     style="border-color: {info['color']}; background: {info['color']}20;"
                     ondragover="dragOver(event)"
                     ondrop="drop(event, '{rank}')"
                     ondragenter="dragEnter(event)"
                     ondragleave="dragLeave(event)">
                    <div class="rank-icon">{info['emoji']}</div>
                    <div class="rank-info">
                        <div class="rank-title">{rank}</div>
                        <div class="rank-desc">{info['desc']}</div>
                    </div>
                    <div class="dropped-container" id="container-{rank}">
                        <!-- 拖拽过来的海报会显示在这里 -->
                    </div>
                </div>
        """
    
    html_code += """
            </div>
        </div>

        <script>
            // 存储当前拖拽的剧集名称
            let currentDragDrama = '';
            
            function dragStart(event, dramaName) {
                currentDragDrama = dramaName;
                event.dataTransfer.setData('text/plain', dramaName);
                event.dataTransfer.effectAllowed = 'move';
            }
            
            function dragOver(event) {
                event.preventDefault();
                event.dataTransfer.dropEffect = 'move';
            }
            
            function dragEnter(event) {
                event.currentTarget.classList.add('hover');
            }
            
            function dragLeave(event) {
                event.currentTarget.classList.remove('hover');
            }
            
            function drop(event, rank) {
                event.preventDefault();
                event.currentTarget.classList.remove('hover');
                
                const dramaName = currentDragDrama;
                if (dramaName) {
                    // 在对应等级中显示海报
                    const container = document.getElementById(`container-${rank}`);
                    const img = document.createElement('img');
                    // 找到原始图片的src
                    const originalImg = Array.from(document.querySelectorAll('.poster')).find(img => img.alt === dramaName);
                    if (originalImg) {
                        img.src = originalImg.src;
                    }
                    img.className = 'dropped-poster';
                    img.alt = dramaName;
                    img.title = `${dramaName} - ${rank}`;
                    container.appendChild(img);
                    
                    // 发送数据到Streamlit
                    const data = {
                        drama: dramaName,
                        rank: rank,
                        timestamp: new Date().toISOString()
                    };
                    
                    // 使用window.parent.postMessage
                    window.parent.postMessage({
                        type: 'streamlit:dragRating',
                        data: data
                    }, '*');
                    
                    // 显示成功消息
                    showMessage(`成功将《${dramaName}》评为【${rank}】！`);
                }
            }
            
            function showMessage(message) {
                const messageEl = document.getElementById('successMessage');
                messageEl.textContent = message;
                messageEl.style.display = 'block';
                setTimeout(() => {
                    messageEl.style.display = 'none';
                }, 3000);
                console.log(message);
            }
        </script>
    </body>
    </html>
    """
    
    return html_code

# 替代方案：手动评分界面
def manual_rating_interface():
    st.markdown("## 🎯 手动评分系统")
    st.markdown("### 💫 选择剧集并给出评分")
    
    # 剧集选择
    drama_names = [drama['name'] for drama in drama_data]
    selected_drama = st.selectbox("选择剧集", drama_names, key="manual_drama")
    
    # 显示选中剧集的海报
    image_src = get_drama_image(selected_drama)
    if image_src:
        st.image(image_src, width=150, caption=selected_drama)
    
    # 评分选择 - 显示所有五个等级
    rating_options = list(ranking_levels.keys())
    selected_rating = st.selectbox("选择评分等级", rating_options, key="manual_rating")
    
    # 显示选中等级的详细信息
    if selected_rating in ranking_levels:
        info = ranking_levels[selected_rating]
        st.markdown(f"**等级描述:** {info['emoji']} {info['desc']}")
    
    # 评分按钮
    if st.button("提交评分", type="primary", key="manual_submit"):
        # 记录评分
        st.session_state.ratings[selected_drama] = selected_rating
        st.session_state.drag_sessions += 1
        
        # 显示成功消息
        info = ranking_levels[selected_rating]
        st.success(f"✅ 成功将 **《{selected_drama}》** 评为 **{info['emoji']} {selected_rating}** ！")
        st.balloons()
        
        # 立即显示评分统计
        show_rating_stats()

# 拖拽评分界面
def drag_rating_interface():
    st.markdown("## 🎯 动态拖拽评分系统")
    st.markdown("### 💫 将左侧海报拖拽到右侧评分等级中！")
    
    # 添加说明
    with st.expander("💡 使用说明"):
        st.markdown("""
        1. **拖拽海报**：从左侧选择剧集海报
        2. **放入评级区域**：拖拽到右侧对应的评分等级中
        3. **自动记录**：系统会自动记录您的评分
        4. **查看统计**：在"评分统计"标签页查看所有评分
        
        **五个评分等级:**
        - 🏆 夯 - 神作中的神作
        - ⭐ 顶级 - 顶级优秀作品  
        - 👑 人上人 - 优秀作品
        - 😐 NPC - 普通水平
        - 💩 拉完了 - 浪费时间
        """)
    
    # 显示拖拽组件
    try:
        component_html = drag_drop_component()
        component_value = components.html(
            component_html,
            height=800,
            width=None
        )
        
    except Exception as e:
        st.error(f"拖拽组件加载失败: {e}")
        st.info("正在切换到手动评分模式...")
        manual_rating_interface()
        return
# ========== 虎扑式评分统计部分 ==========
def show_rating_stats():
    st.markdown('<div class="main-header">🎬 年度剧集虎扑评分榜</div>', unsafe_allow_html=True)
    
    # 侧边栏 - 筛选器
    with st.sidebar:
        st.header("🔍 筛选设置")
        
        # 类型筛选
        genres = ['全部'] + list(st.session_state.shows_df['genre'].unique())
        selected_genre = st.selectbox("剧集类型", genres)
        
        # 年份筛选
        years = ['全部'] + sorted(st.session_state.shows_df['release_year'].unique(), reverse=True)
        selected_year = st.selectbox("发行年份", years)
        
        # 评分范围
        min_score, max_score = st.slider(
            "评分范围", 
            min_value=0.0, 
            max_value=10.0, 
            value=(8.0, 9.5),
            step=0.1
        )
        
        # 应用筛选
        filtered_shows = st.session_state.shows_df.copy()
        if selected_genre != '全部':
            filtered_shows = filtered_shows[filtered_shows['genre'] == selected_genre]
        if selected_year != '全部':
            filtered_shows = filtered_shows[filtered_shows['release_year'] == selected_year]
        filtered_shows = filtered_shows[
            (filtered_shows['avg_rating'] >= min_score) & 
            (filtered_shows['avg_rating'] <= max_score)
        ]
    
    # 主内容区 - 两列布局
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📺 剧集评分区")
        
        # 剧集展示和评分
        for _, show in filtered_shows.iterrows():
            with st.container():
                st.markdown(f'<div class="show-card">', unsafe_allow_html=True)
                
                # 剧集标题和基本信息
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.write(f"### {show['title']}")
                    st.write(f"**类型:** {show['genre']} | **年份:** {show['release_year']}")
                    st.write(show['description'])
                
                with col_b:
                    st.markdown(f'<div class="score-badge">评分: {show["avg_rating"]}</div>', 
                               unsafe_allow_html=True)
                    st.write(f"👥 {show['rating_count']}人评分")
                
                # 虎扑式热评和梗
                memes, comments = get_show_memes(show['id'])
                
                if memes:
                    st.write("**🔥 热梗:**")
                    meme_cols = st.columns(len(memes))
                    for i, meme in enumerate(memes):
                        with meme_cols[i]:
                            st.markdown(f'<div class="meme-tag">{meme}</div>', unsafe_allow_html=True)
                
                # 评分滑块
                st.markdown('<div class="rating-section">', unsafe_allow_html=True)
                user_rating = st.slider(
                    f"为《{show['title']}》评分",
                    min_value=0.0,
                    max_value=10.0,
                    value=st.session_state.user_ratings.get(show['id'], show['avg_rating']),
                    step=0.1,
                    key=f"rating_{show['id']}"
                )
                
                # 保存用户评分
                if st.button(f"提交评分", key=f"btn_{show['id']}"):
                    st.session_state.user_ratings[show['id']] = user_rating
                    st.success(f"已为《{show['title']}》评分: {user_rating}")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # 显示热评
                if comments:
                    st.write("**💬 虎扑热评:**")
                    for comment in comments:
                        st.markdown(f'<div class="hot-comment">{comment}</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.write("---")
    
    with col2:
        st.subheader("🏆 实时排行榜")
        
        # 排序选项
        sort_by = st.selectbox("排序方式", ["综合评分", "评分人数", "最新年份"])
        
        if sort_by == "综合评分":
            ranked_shows = filtered_shows.sort_values('avg_rating', ascending=False)
        elif sort_by == "评分人数":
            ranked_shows = filtered_shows.sort_values('rating_count', ascending=False)
        else:
            ranked_shows = filtered_shows.sort_values('release_year', ascending=False)
        
        # 显示排行榜
        for i, (_, show) in enumerate(ranked_shows.head(10).iterrows(), 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            
            st.write(f"{medal} **{show['title']}**")
            st.write(f"  评分: **{show['avg_rating']}** 🌟 ({show['rating_count']}人)")
            
            # 显示用户个人评分（如果有）
            user_score = st.session_state.user_ratings.get(show['id'])
            if user_score:
                st.write(f"  我的评分: **{user_score}** ⭐")
            
            st.write("---")
        
        # 统计信息
        st.subheader("📊 数据统计")
        st.write(f"总剧集数: **{len(filtered_shows)}**")
        st.write(f"平均评分: **{filtered_shows['avg_rating'].mean():.1f}**")
        st.write(f"总评分人数: **{filtered_shows['rating_count'].sum():,}**")
        
        # 用户评分统计
        if st.session_state.user_ratings:
            st.write(f"我已评分: **{len(st.session_state.user_ratings)}** 部剧集")
            avg_user_rating = np.mean(list(st.session_state.user_ratings.values()))
            st.write(f"我的平均评分: **{avg_user_rating:.1f}**")

# 主程序
def main():
    # 初始化数据
    init_data()
    
    # 显示主页面
    st.markdown('<h1 class="main-header">🎬 剧集心灵捕手</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">✨ AI深度解析 · 真拖拽评分</p>', unsafe_allow_html=True)
    
    # 标签页导航
    tab1, tab2 = st.tabs(["🔮 AI智能推荐", "🖱️ 拖拽评分"])
    
    with tab1:
        ai_recommendation_interface()
    
    with tab2:
        drag_rating_interface()

if __name__ == "__main__":
    main()