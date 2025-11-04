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
            st.write(f"**评分：** {drama_info['rating']}")
            st.write(f"**主演：** {drama_info['actors']}")
            st.write(f"**导演：** {drama_info['director']}")
            
        with col2:
            # 尝试显示剧集海报
            try:
                if os.path.exists(drama_info['image']):
                    st.image(drama_info['image'], width=200)
                else:
                    st.markdown("📷 *海报加载中...*")
            except:
                st.markdown("📷 *海报暂不可用*")
        
        st.markdown("---")
        
        # 剧情简介
        st.markdown(f"### 📝 剧情简介")
        st.write(drama_info['desc'])
        
        # 推荐理由
        st.markdown(f"### 💡 推荐理由")
        st.write(drama_info['reason'])
        
        # 观看建议
        st.markdown(f"### 🎯 观看建议")
        col3, col4, col5 = st.columns(3)
        with col3:
            st.markdown(f"**💫 心情匹配：** {drama_info['mood']}")
        with col4:
            st.markdown(f"**⏰ 最佳时段：** {drama_info['time']}")
        with col5:
            st.markdown(f"**🍂 推荐季节：** {drama_info['season']}")
        
        st.markdown(f"**🎨 氛围：** {drama_info['vibes']}")
        st.markdown(f"**🍿 最佳搭配：** {drama_info['best_with']}")
        st.markdown(f"**📺 类似剧集：** {drama_info['similar']}")
        
        # 经典台词
        st.markdown(f"### 💬 经典台词")
        st.markdown(f"> {drama_info['memorable_line']}")
        
        # 角色评分系统
        st.markdown("---")
        st.markdown("### 🎭 角色评分系统")
        
        # 根据剧集名称加载对应的角色数据
        drama_name = drama_info['name']
        
        # 角色数据（这里需要根据实际剧集补充完整角色信息）
        characters_data = {
            '黑暗荣耀': [
                {'name': '文东恩', 'role': '女主角', 'desc': '校园暴力受害者，精心策划复仇计划', 'rating': 9.5, 'popularity': 95},
                {'name': '朴妍珍', 'role': '反派', 'desc': '校园暴力的主导者，表面光鲜内心扭曲', 'rating': 8.8, 'popularity': 88},
                {'name': '周汝正', 'role': '男主角', 'desc': '整形外科医生，默默守护文东恩', 'rating': 9.2, 'popularity': 92}
            ],
            '爱的迫降': [
                {'name': '尹世莉', 'role': '女主角', 'desc': '韩国财阀女继承人，意外降落在朝鲜', 'rating': 9.3, 'popularity': 93},
                {'name': '李正赫', 'role': '男主角', 'desc': '朝鲜军官，温柔守护尹世莉', 'rating': 9.4, 'popularity': 94}
            ],
            '鱿鱼游戏': [
                {'name': '成奇勋', 'role': '男主角', 'desc': '负债累累的参赛者，展现人性光辉', 'rating': 9.1, 'popularity': 91},
                {'name': '曹尚佑', 'role': '重要角色', 'desc': '高材生参赛者，在游戏中逐渐黑化', 'rating': 8.9, 'popularity': 89}
            ],
            '请回答1988': [
                {'name': '成德善', 'role': '女主角', 'desc': '活泼开朗的双门洞女孩', 'rating': 9.7, 'popularity': 97},
                {'name': '金正焕', 'role': '男主角', 'desc': '外表冷漠内心温暖的狗焕', 'rating': 9.6, 'popularity': 96}
            ]
        }
        
        # 获取当前剧集的角色数据
        characters = characters_data.get(drama_name, [])
        
        if characters:
            # 显示角色评分卡片
            cols = st.columns(min(3, len(characters)))
            
            for i, character in enumerate(characters):
                with cols[i % len(cols)]:
                    # 角色卡片
                    st.markdown(f"#### {character['name']}")
                    st.markdown(f"**角色：** {character['role']}")
                    st.markdown(f"**描述：** {character['desc']}")
                    
                    # 评分和人气
                    col_rating, col_pop = st.columns(2)
                    with col_rating:
                        st.markdown(f"**评分：** {character['rating']}/10")
                    with col_pop:
                        st.markdown(f"**人气：** {character['popularity']}%")
                    
                    # 评分滑块
                    user_rating = st.slider(
                        f"为{character['name']}评分",
                        min_value=0.0,
                        max_value=10.0,
                        value=character['rating'],
                        step=0.1,
                        key=f"{drama_name}_{character['name']}_rating"
                    )
                    
                    # 保存评分按钮
                    if st.button(f"💾 保存{character['name']}评分", key=f"{drama_name}_{character['name']}_save"):
                        st.success(f"已保存{character['name']}的评分：{user_rating}")
        else:
            st.info("该剧集的角色评分系统正在开发中...")
        
        # 角色对比分析
        if len(characters) >= 2:
            st.markdown("---")
            st.markdown("### 📊 角色对比分析")
            
            # 创建对比数据
            char_names = [char['name'] for char in characters]
            char_ratings = [char['rating'] for char in characters]
            char_popularity = [char['popularity'] for char in characters]
            
            # 使用Streamlit原生图表
            chart_data = pd.DataFrame({
                '角色': char_names,
                '评分': char_ratings,
                '人气': char_popularity
            })
            
            st.bar_chart(chart_data.set_index('角色'))
        
        # 角色梗和热评
        st.markdown("---")
        st.markdown("### 🎭 角色梗 & 热评")
        
        # 角色梗标签
        meme_tags = {
            '黑暗荣耀': ['复仇女王', '校园暴力警示录', '全员恶人', '暗黑美学'],
            '爱的迫降': ['跨国恋天花板', '军官的温柔', '命运般的爱情', '南北韩罗曼史'],
            '鱿鱼游戏': ['人性考验', '生存游戏', '童年游戏黑暗版', '456亿的诱惑'],
            '请回答1988': ['双门洞青春', '邻里温情', '怀旧经典', '笑中带泪']
        }
        
        tags = meme_tags.get(drama_name, ['经典之作', '值得一看', '口碑爆款'])
        tag_html = ''.join([f'<span class="meme-tag">{tag}</span>' for tag in tags])
        st.markdown(f'<div>{tag_html}</div>', unsafe_allow_html=True)
        
        # 热评展示
        hot_comments = {
            '黑暗荣耀': [
                '宋慧乔演技炸裂，从受害者到复仇者的转变太精彩了！',
                '每个角色都很有深度，不是简单的善恶二元对立',
                '复仇剧情紧张刺激，看得人热血沸腾'
            ],
            '爱的迫降': [
                '玄彬孙艺珍CP感绝了，每一帧都像画报',
                '跨国恋拍得这么浪漫，导演太会了',
                '军官的温柔谁能抵挡，李正赫完美男友'
            ],
            '鱿鱼游戏': [
                'Netflix全球爆款，游戏设定太新颖了',
                '人性在极端环境下的展现，引人深思',
                '每个游戏都充满紧张感，一口气刷完'
            ],
            '请回答1988': [
                '温暖治愈，笑中带泪的经典之作',
                '双门洞的邻里情太真实了，仿佛回到童年',
                '每个角色都很有魅力，值得反复观看'
            ]
        }
        
        comments = hot_comments.get(drama_name, ['经典之作，值得推荐！'])
        for comment in comments:
            st.markdown(f'<div class="hot-comment">💬 {comment}</div>', unsafe_allow_html=True)

# AI推荐界面
def ai_recommendation_interface():
    st.markdown('<div class="main-header">WATCheese🧀</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI智能心灵匹配系统 · 为你量身定制剧集推荐</div>', unsafe_allow_html=True)
    
    # 用户画像分析
    with st.expander("🔍 AI心灵匹配分析", expanded=True):
        st.markdown("### 🎯 请告诉我你的追剧偏好")
        
        col1, col2 = st.columns(2)
        
        with col1:
            genre_pref = st.multiselect(
                "🎭 喜欢的剧集类型",
                ['爱情', '悬疑', '喜剧', '科幻', '奇幻', '家庭', '治愈', '励志', '惊悚'],
                default=['爱情', '悬疑']
            )
            
            mood_pref = st.multiselect(
                "💫 想要的心情体验",
                ['浪漫', '开心', '感动', '紧张', '刺激', '思考', '放松', '怀旧'],
                default=['浪漫', '感动']
            )
        
        with col2:
            time_pref = st.multiselect(
                "⏰ 通常的观看时段",
                ['早上', '下午', '晚上', '深夜'],
                default=['晚上', '深夜']
            )
            
            season_pref = st.multiselect(
                "🍂 偏好的观看季节",
                ['春季', '夏季', '秋季', '冬季', '全年'],
                default=['冬季', '全年']
            )
    
    # 分析用户画像
    user_choices = {
        'genre': genre_pref,
        'mood': mood_pref,
        'time': time_pref,
        'season': season_pref
    }
    
    user_traits = analyze_user_profile(user_choices)
    
    # 显示用户画像
    st.markdown("### 👤 你的追剧画像")
    traits_html = ''.join([f'<span class="meme-tag" style="background-color: #4ECDC4;">{trait}</span>' for trait in user_traits])
    st.markdown(f'<div>{traits_html}</div>', unsafe_allow_html=True)
    
    # 生成个性化推荐
    st.markdown("### 🎁 AI为你精心挑选")
    
    # 根据用户偏好筛选剧集
    filtered_dramas = []
    for drama in drama_data:
        # 检查类型匹配
        genre_match = any(genre in drama['genre'] for genre in genre_pref) if genre_pref else True
        
        # 检查心情匹配
        mood_match = any(mood in drama['mood'] for mood in mood_pref) if mood_pref else True
        
        # 检查时段匹配
        time_match = any(time in drama['time'] for time in time_pref) if time_pref else True
        
        # 检查季节匹配
        season_match = any(season in drama['season'] for season in season_pref) if season_pref else True
        
        if genre_match and mood_match and time_match and season_match:
            filtered_dramas.append(drama)
    
    # 如果没有匹配的剧集，显示所有剧集
    if not filtered_dramas:
        filtered_dramas = drama_data
        st.info("🔍 正在为你探索更广泛的剧集选择...")
    
    # 随机选择3部剧集推荐
    recommended_dramas = random.sample(filtered_dramas, min(3, len(filtered_dramas)))
    
    # 显示推荐结果
    for i, drama in enumerate(recommended_dramas):
        with st.expander(f"🎯 推荐 {i+1}: 《{drama['name']}》", expanded=True):
            
            # 推荐理由
            recommendation_text = generate_personalized_recommendation(drama, user_traits)
            st.markdown(f"**💡 {recommendation_text}")
            
            # 剧集基本信息
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**国家：** {drama['country']}")
                st.markdown(f"**类型：** {drama['genre']}")
                st.markdown(f"**评分：** ⭐{drama['rating']}")
                st.markdown(f"**追剧指数：** {drama['binge_level']}")
                
            with col2:
                # 尝试显示海报
                try:
                    if os.path.exists(drama['image']):
                        st.image(drama['image'], width=120)
                    else:
                        st.markdown("📷 *海报加载中...*")
                except:
                    st.markdown("📷 *海报暂不可用*")
            
            # 查看详情按钮
            if st.button(f"🔍 查看《{drama['name']}》详情", key=f"detail_{drama['name']}"):
                st.session_state.current_drama = drama
                st.session_state.current_page = 'detail'
                st.rerun()

# 拖拽评分界面
def drag_rating_interface():
    st.markdown("### 🎯 动态拖拽评分系统")
    st.markdown("💡 将剧集海报拖拽到对应的评分区域，体验沉浸式评分乐趣！")
    
    # 评分区域说明
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"<div style='text-align: center; padding: 10px; background-color: {ranking_levels['夯']['color']}; border-radius: 10px; color: white;'>🏆 夯</div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center; font-size: 0.8rem;'>神作中的神作</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"<div style='text-align: center; padding: 10px; background-color: {ranking_levels['顶级']['color']}; border-radius: 10px; color: white;'>⭐ 顶级</div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center; font-size: 0.8rem;'>顶级优秀作品</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"<div style='text-align: center; padding: 10px; background-color: {ranking_levels['人上人']['color']}; border-radius: 10px; color: white;'>👑 人上人</div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center; font-size: 0.8rem;'>优秀作品</div>", unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"<div style='text-align: center; padding: 10px; background-color: {ranking_levels['NPC']['color']}; border-radius: 10px; color: white;'>😐 NPC</div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center; font-size: 0.8rem;'>普通水平</div>", unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"<div style='text-align: center; padding: 10px; background-color: {ranking_levels['拉完了']['color']}; border-radius: 10px; color: white;'>💩 拉完了</div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center; font-size: 0.8rem;'>浪费时间</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 剧集海报展示区域
    st.markdown("### 🎬 选择你要评分的剧集")
    
    # 显示所有剧集的海报
    cols = st.columns(3)
    
    for i, drama in enumerate(drama_data):
        with cols[i % 3]:
            # 剧集卡片
            st.markdown(f"<div class='show-card'>", unsafe_allow_html=True)
            
            # 海报显示
            try:
                if os.path.exists(drama['image']):
                    st.image(drama['image'], width=150)
                else:
                    st.markdown("📷 *海报加载中...*")
            except:
                st.markdown("📷 *海报暂不可用*")
            
            st.markdown(f"**{drama['name']}**")
            st.markdown(f"⭐ {drama['rating']} | {drama['country']}")
            
            # 手动评分选择（备选方案）
            rating = st.selectbox(
                f"为《{drama['name']}》评分",
                ['请选择评分', '夯', '顶级', '人上人', 'NPC', '拉完了'],
                key=f"manual_rating_{drama['name']}"
            )
            
            if rating != '请选择评分':
                if st.button(f"💾 保存{rating}评分", key=f"save_{drama['name']}"):
                    st.session_state.user_ratings[drama['name']] = rating
                    st.success(f"已为《{drama['name']}》评分：{rating}")
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    # 显示评分统计
    if st.session_state.user_ratings:
        st.markdown("---")
        st.markdown("### 📊 你的评分统计")
        
        rated_shows = list(st.session_state.user_ratings.items())
        cols = st.columns(min(3, len(rated_shows)))
        
        for i, (show_name, rating) in enumerate(rated_shows):
            with cols[i % len(cols)]:
                level_info = ranking_levels[rating]
                st.markdown(f"<div style='text-align: center; padding: 10px; background-color: {level_info['color']}; border-radius: 10px; color: white;'>"
                          f"{level_info['emoji']} {show_name}<br>{rating}"
                          f"</div>", unsafe_allow_html=True)

# 主应用逻辑
def main():
    init_data()
    
    # 侧边栏导航
    st.sidebar.title("🧀 WATCheese导航")
    
    if st.session_state.current_page == 'main':
        # 主页面显示两个主要功能
        tab1, tab2 = st.tabs(["🤖 AI智能推荐", "🎯 动态评分"])
        
        with tab1:
            ai_recommendation_interface()
        
        with tab2:
            drag_rating_interface()
    
    elif st.session_state.current_page == 'detail' and st.session_state.current_drama:
        # 显示剧集详情页面
        show_drama_detail_expander(st.session_state.current_drama)
        
        # 返回主页面按钮
        if st.button("🔙 返回主页面"):
            st.session_state.current_page = 'main'
            st.session_state.current_drama = None
            st.rerun()
    
    # 页脚信息
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ 关于WATCheese")
    st.sidebar.markdown("""
    WATCheese🧀 是一个智能剧集推荐和评分系统，结合AI技术为用户提供个性化的追剧体验。
    
    **主要功能：**
    - 🤖 AI心灵匹配推荐
    - 🎯 动态拖拽评分
    - 🎭 详细角色分析
    - 📊 个性化数据统计
    """)
    
    # 使用说明
    with st.sidebar.expander("📖 使用说明"):
        st.markdown("""
        1. **AI推荐**：选择你的偏好，获取个性化剧集推荐
        2. **动态评分**：拖拽海报或手动选择进行评分
        3. **查看详情**：点击推荐剧集查看详细信息和角色评分
        4. **保存记录**：所有评分会自动保存到本地
        """)

if __name__ == "__main__":
    main()