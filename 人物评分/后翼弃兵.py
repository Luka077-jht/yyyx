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
    page_title="♟️ 后翼弃兵角色评分 - 虎扑风格",
    page_icon="♟️",
    layout="wide"
)

# 自定义CSS样式 - 保持黑暗荣耀文件的风格
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
    
    .main-header {
        font-family: 'Noto Sans SC', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(45deg, #2C5530, #4A7C59, #6B8E23, #8FBC8F);
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
    .character-card {
        background-color: #f8f9fa;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #2C5530;
        transition: all 0.3s ease;
    }
    .character-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    .rating-section {
        background: linear-gradient(135deg, #2C5530 0%, #4A7C59 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: #FFFFFF;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
        font-weight: 500;
    }
    .rating-section h1, .rating-section h2, .rating-section h3, .rating-section h4 {
        color: #FFFFFF;
        text-shadow: 0 1px 3px rgba(0,0,0,0.5);
        font-weight: 600;
    }
    .meme-tag {
        display: inline-block;
        background-color: #C8E6C9;
        color: #2E7D32;
        padding: 0.4rem 1rem;
        margin: 0.3rem;
        border-radius: 15px;
        font-size: 1rem;
        font-weight: bold;
    }
    .hot-comment {
        background-color: #E8F5E8;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid #4CAF50;
        color: #2E7D32;
        font-weight: 500;
    }
    .score-badge {
        background-color: #4CAF50;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
    }
    .star-rating {
        font-size: 2rem;
        margin: 10px 0;
        color: white;
    }
    .star-rating .star {
        color: #FFD93D;
        margin: 0 5px;
        cursor: pointer;
        text-shadow: 0 0 3px rgba(255, 217, 61, 0.5);
        font-size: 2rem;
    }
    .star-rating .star.empty {
        color: white;
        opacity: 0.7;
        font-size: 2.2rem;
    }
    .score-highlight {
        background: linear-gradient(135deg, #66BB6A, #81C784);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 1.2rem;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
        box-shadow: 0 4px 8px rgba(102, 187, 106, 0.3);
    }
    .stat-card {
        background: linear-gradient(135deg, #2C5530 0%, #4A7C59 100%);
        color: #FFFFFF;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 10px 0;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
        font-weight: 500;
    }
    .stat-card h3 {
        color: #FFFFFF;
        text-shadow: 0 1px 3px rgba(0,0,0,0.5);
        font-weight: 600;
    }
    .character-image {
        width: 200px;
        height: 200px;
        border-radius: 15px;
        object-fit: cover;
        border: 4px solid #2C5530;
        margin: 0 auto;
        display: block;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .actor-section {
        background: linear-gradient(135deg, #A5D6A7 0%, #66BB6A 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: white;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    .actor-section h3 {
        color: white;
        text-shadow: 0 1px 3px rgba(0,0,0,0.5);
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .works-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        margin-top: 1rem;
    }
    .work-item {
        background: rgba(255, 255, 255, 0.2);
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        font-weight: 500;
        backdrop-filter: blur(10px);
    }
    .actor-info {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 1rem;
    }
    .actor-name {
        font-size: 1.3rem;
        font-weight: bold;
        color: #FFD93D;
    }
</style>
""", unsafe_allow_html=True)

# 初始化数据
def init_data():
    if 'character_ratings' not in st.session_state:
        st.session_state.character_ratings = {}
    if 'rating_sessions' not in st.session_state:
        st.session_state.rating_sessions = 0
    if 'characters_df' not in st.session_state:
        st.session_state.characters_df = initialize_characters()

# 后翼弃兵角色数据
def initialize_characters():
    characters_data = {
        'id': range(1, 9),
        'name': ['Beth Harmon', 'Jolene', 'Harry Beltik', 'Benny Watts', 'Alma Wheatley', 'Mr. Shaibel', 'Vasily Borgov', 'Townes'],
        'role': ['国际象棋天才', '孤儿院好友', '启蒙教练', '象棋导师', '养母', '启蒙老师', '苏联冠军', '记者朋友'],
        'description': [
            '孤儿院长大的象棋天才，拥有惊人的计算能力和直觉',
            'Beth在孤儿院的好友，坚强独立的黑人女孩',
            'Beth的第一个象棋对手，后来成为她的启蒙教练',
            '美国象棋冠军，Beth的重要导师和竞争对手',
            'Beth的养母，曾经是钢琴家，支持Beth的象棋事业',
            '孤儿院的清洁工，教会Beth下棋的启蒙老师',
            '苏联象棋世界冠军，Beth的终极对手',
            '象棋记者，Beth的忠实朋友和暗恋对象'
        ],
        'mbti_type': ['INTJ', 'ESTJ', 'ISTJ', 'ENTP', 'ISFJ', 'ISTP', 'INTJ', 'ENFP'],
        'mbti_description': [
            'INTJ（建筑师型）：战略思维，独立自主，追求完美',
            'ESTJ（总经理型）：务实可靠，组织能力强，保护朋友',
            'ISTJ（物流师型）：严谨认真，遵守规则，忠诚可靠',
            'ENTP（辩论家型）：聪明机智，创新思维，善于竞争',
            'ISFJ（守护者型）：温柔体贴，照顾他人，传统保守',
            'ISTP（鉴赏家型）：实用主义，冷静理性，默默付出',
            'INTJ（建筑师型）：战略大师，沉着冷静，追求卓越',
            'ENFP（竞选者型）：热情友好，理想主义，支持他人'
        ],
        'actor_name': ['Anya Taylor-Joy', 'Moses Ingram', 'Harry Melling', 'Thomas Brodie-Sangster', 'Marielle Heller', 'Bill Camp', 'Marcin Dorociński', 'Jacob Fortune-Lloyd'],
        'actor_bio': [
            '英国女演员，因饰演Beth Harmon一角而获得全球认可',
            '美国女演员，在剧中展现了出色的表演深度',
            '英国演员，成功塑造了Harry Beltik这一复杂角色',
            '英国演员，以独特的表演风格和魅力深受观众喜爱',
            '美国女演员兼导演，演技细腻，情感丰富',
            '美国资深演员，演技扎实，完美诠释了启蒙老师角色',
            '波兰演员，成功演绎了苏联象棋冠军的威严形象',
            '英国演员，以温暖真诚的表演赢得观众喜爱'
        ],
        'famous_works': [
            ['后翼弃兵', '女巫', '菜单'],
            ['后翼弃兵', '欧比旺', '他们/她们'],
            ['后翼弃兵', '哈利波特', '女王的棋局'],
            ['后翼弃兵', '权力的游戏', '真爱至上'],
            ['后翼弃兵', '你能原谅我吗', '日记'],
            ['后翼弃兵', '林肯', '十二金刚'],
            ['后翼弃兵', '冷战', '另一个世界'],
            ['后翼弃兵', '王冠', '绅士们']
        ],
        'avg_rating': [9.6, 8.7, 8.5, 9.2, 8.3, 8.9, 9.4, 8.6],
        'rating_count': [21500, 15200, 13800, 18200, 12500, 16800, 19500, 14200],
        'image_url': [
            # Beth Harmon - 使用可靠的图片URL
            'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=400&h=400&fit=crop',
            # Jolene - 使用可靠的图片URL
            'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=400&h=400&fit=crop',
            # Harry Beltik - 使用可靠的图片URL
            'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop',
            # Benny Watts - 使用可靠的图片URL
            'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&h=400&fit=crop',
            # Alma Wheatley - 使用可靠的图片URL
            'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=400&h=400&fit=crop',
            # Mr. Shaibel - 使用可靠的图片URL
            'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop',
            # Vasily Borgov - 使用可靠的图片URL
            'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop',
            # Townes - 使用可靠的图片URL
            'https://images.unsplash.com/photo-1519244703995-f4e0f30006d5?w=400&h=400&fit=crop'
        ],
        'actor_photo_url': [
            # Anya Taylor-Joy - 使用可靠的图片URL
            'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=300&h=300&fit=crop',
            # Moses Ingram - 使用可靠的图片URL
            'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=300&h=300&fit=crop',
            # Harry Melling - 使用可靠的图片URL
            'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=300&fit=crop',
            # Thomas Brodie-Sangster - 使用可靠的图片URL
            'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=300&h=300&fit=crop',
            # Marielle Heller - 使用可靠的图片URL
            'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=300&h=300&fit=crop',
            # Bill Camp - 使用可靠的图片URL
            'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=300&h=300&fit=crop',
            # Marcin Dorociński - 使用可靠的图片URL
            'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=300&fit=crop',
            # Jacob Fortune-Lloyd - 使用可靠的图片URL
            'https://images.unsplash.com/photo-1519244703995-f4e0f30006d5?w=300&h=300&fit=crop'
        ]
    }
    
    return pd.DataFrame(characters_data)

# 代表作品图片映射
def get_work_images(work_name):
    work_images = {
        # 使用真实的电影海报图片
        '后翼弃兵': 'https://upload.wikimedia.org/wikipedia/en/thumb/0/08/The_Queen%27s_Gambit_%28miniseries%29.png/500px-The_Queen%27s_Gambit_%28miniseries%29.png',
        '女巫': 'https://upload.wikimedia.org/wikipedia/en/thumb/7/7a/The_Witch_%282015_poster%29.png/500px-The_Witch_%282015_poster%29.png',
        '菜单': 'https://upload.wikimedia.org/wikipedia/en/thumb/3/3f/The_Menu_%282022_film%29.png/500px-The_Menu_%282022_film%29.png',
        '欧比旺': 'https://upload.wikimedia.org/wikipedia/en/thumb/4/4e/Obi-Wan_Kenobi_%28TV_series%29.jpg/500px-Obi-Wan_Kenobi_%28TV_series%29.jpg',
        '他们/她们': 'https://upload.wikimedia.org/wikipedia/en/thumb/5/5f/Them_%28TV_series%29.jpg/500px-Them_%28TV_series%29.jpg',
        '哈利波特': 'https://upload.wikimedia.org/wikipedia/en/thumb/b/bf/Harry_Potter_and_the_Philosopher%27s_Stone.jpg/500px-Harry_Potter_and_the_Philosopher%27s_Stone.jpg',
        '女王的棋局': 'https://upload.wikimedia.org/wikipedia/en/thumb/0/08/The_Queen%27s_Gambit_%28miniseries%29.png/500px-The_Queen%27s_Gambit_%28miniseries%29.png',
        '权力的游戏': 'https://upload.wikimedia.org/wikipedia/en/thumb/d/d8/Game_of_Thrones_title_card.jpg/500px-Game_of_Thrones_title_card.jpg',
        '真爱至上': 'https://upload.wikimedia.org/wikipedia/en/thumb/6/67/Love_Actually_movie.jpg/500px-Love_Actually_movie.jpg',
        '你能原谅我吗': 'https://upload.wikimedia.org/wikipedia/en/thumb/7/7e/Can_You_Ever_Forgive_Me%3F_poster.png/500px-Can_You_Ever_Forgive_Me%3F_poster.png',
        '日记': 'https://upload.wikimedia.org/wikipedia/en/thumb/4/4f/The_Diary_of_a_Teenage_Girl_poster.jpg/500px-The_Diary_of_a_Teenage_Girl_poster.jpg',
        '林肯': 'https://upload.wikimedia.org/wikipedia/en/thumb/4/4c/Lincoln_%282012_film%29_poster.jpg/500px-Lincoln_%282012_film%29_poster.jpg',
        '十二金刚': 'https://upload.wikimedia.org/wikipedia/en/thumb/8/8e/The_Dirty_Dozen_%281967%29_poster.jpg/500px-The_Dirty_Dozen_%281967%29_poster.jpg',
        '冷战': 'https://upload.wikimedia.org/wikipedia/en/thumb/7/7e/Cold_War_%282018_film%29.png/500px-Cold_War_%282018_film%29.png',
        '另一个世界': 'https://upload.wikimedia.org/wikipedia/en/thumb/9/9f/Another_World_%28film%29.jpg/500px-Another_World_%28film%29.jpg',
        '王冠': 'https://upload.wikimedia.org/wikipedia/en/thumb/4/4f/The_Crown_title_card.png/500px-The_Crown_title_card.png',
        '绅士们': 'https://upload.wikimedia.org/wikipedia/en/thumb/0/06/The_Gentlemen_%282019%29_poster.jpg/500px-The_Gentlemen_%282019%29_poster.jpg'
    }
    # 使用可靠的备用图片
    return work_images.get(work_name, 'https://upload.wikimedia.org/wikipedia/en/thumb/0/08/The_Queen%27s_Gambit_%28miniseries%29.png/500px-The_Queen%27s_Gambit_%28miniseries%29.png')

# 虎扑风格的热评
def get_hot_comments(character_name):
    comments = {
        'Beth Harmon': [
            "这姑娘下棋的时候眼神太杀了，简直像换了个人！",
            "Beth的成长轨迹太真实了，从孤儿到世界冠军，每一步都不容易",
            "她的天赋和努力完美结合，这才是真正的天才"
        ],
        'Jolene': [
            "Jolene真是好姐妹，关键时刻总是出现",
            "她的独立和坚强让人敬佩，黑人女孩的榜样",
            "Jolene和Beth的友谊跨越了种族和阶级"
        ],
        'Harry Beltik': [
            "Harry从对手变成教练，这个转变太感人了",
            "他是Beth象棋生涯的第一个重要转折点",
            "Harry的严谨和认真是Beth成功的重要基础"
        ],
        'Benny Watts': [
            "Benny太帅了！牛仔帽配象棋，这是什么神仙组合",
            "他是Beth最重要的导师，教会她真正的竞技精神",
            "Benny和Beth的化学反应太强了，希望他们在一起"
        ],
        'Alma Wheatley': [
            "养母虽然有自己的问题，但对Beth是真心的",
            "她的酗酒问题让人心疼，但始终支持Beth",
            "Alma和Beth的母女关系很复杂但很真实"
        ],
        'Mr. Shaibel': [
            "Shaibel先生是真正的启蒙老师，默默付出",
            "没有他就没有Beth的象棋生涯，致敬！",
            "他在孤儿院的地下室教会了Beth一切"
        ],
        'Vasily Borgov': [
            "苏联冠军的气场太强了，真正的王者风范",
            "Borgov是Beth最强大的对手，也是她成长的催化剂",
            "他的冷静和专注是象棋大师的典范"
        ],
        'Townes': [
            "Townes太温柔了，一直默默支持Beth",
            "他是Beth在象棋世界外的避风港",
            "Townes的真诚和善良让人感动"
        ]
    }
    return comments.get(character_name, ["这个角色很有深度，值得细细品味"])

# 生成AI角色分析
def generate_ai_analysis(character_name, rating):
    analysis_templates = {
        'Beth Harmon': [
            f"基于{rating}分的评价，Beth Harmon展现了惊人的象棋天赋和坚韧不拔的精神。她的INTJ人格特质让她在棋盘上如鱼得水，但个人生活的挑战也让她成长。",
            f"{rating}分的Beth Harmon是一个复杂而迷人的角色。她的天才与脆弱并存，在象棋世界和现实生活之间寻找平衡。",
            f"评分{rating}分，Beth的成长轨迹体现了天赋与努力的完美结合。她从孤儿到世界冠军的旅程激励了无数观众。"
        ],
        'Jolene': [
            f"{rating}分的Jolene展现了黑人女性的坚强和独立。她在Beth最需要的时候总是出现，是真正的朋友。",
            f"Jolene的ESTJ人格让她务实可靠，{rating}分的评价体现了她对Beth的无私支持。",
            f"评分{rating}分，Jolene的角色提醒我们友谊和坚持的重要性。"
        ],
        'Harry Beltik': [
            f"Harry Beltik的{rating}分评价体现了他的严谨和认真。作为Beth的启蒙教练，他的贡献不可忽视。",
            f"{rating}分的Harry展现了ISTJ人格的典型特质：忠诚、可靠、注重细节。",
            f"评分{rating}分，Harry从对手到教练的转变是剧中感人的一幕。"
        ],
        'Benny Watts': [
            f"Benny Watts的{rating}分评价充分体现了他的魅力和才华。他的ENTP人格让他成为Beth的完美导师。",
            f"{rating}分的Benny是象棋世界的叛逆者，他的创新思维和竞争精神令人印象深刻。",
            f"评分{rating}分，Benny和Beth的互动是剧中最精彩的对手戏之一。"
        ],
        'Alma Wheatley': [
            f"Alma Wheatley的{rating}分评价反映了她的复杂性和人性弱点。她的ISFJ人格让她渴望照顾他人。",
            f"{rating}分的Alma是一个有缺陷但真心的母亲形象，她的酗酒问题让人心疼。",
            f"评分{rating}分，Alma和Beth的关系展现了非传统母爱的力量。"
        ],
        'Mr. Shaibel': [
            f"Mr. Shaibel的{rating}分评价是对他默默付出的最好肯定。他的ISTP人格让他务实而低调。",
            f"{rating}分的Shaibel先生是真正的启蒙者，他在孤儿院的地下室点燃了Beth的象棋之火。",
            f"评分{rating}分，向这位默默无闻的英雄致敬！"
        ],
        'Vasily Borgov': [
            f"Vasily Borgov的{rating}分评价体现了他的王者风范。作为INTJ人格，他的战略思维无可挑剔。",
            f"{rating}分的Borgov是Beth最强大的对手，他的冷静和专注是象棋大师的典范。",
            f"评分{rating}分，苏联冠军的气场和实力令人敬畏。"
        ],
        'Townes': [
            f"Townes的{rating}分评价反映了他的温柔和真诚。ENFP人格让他成为Beth的忠实朋友。",
            f"{rating}分的Townes是Beth在象棋世界外的避风港，他的支持至关重要。",
            f"评分{rating}分，Townes的善良和理想主义让人感动。"
        ]
    }
    
    templates = analysis_templates.get(character_name, [f"{character_name}获得了{rating}分的评价，这个角色在剧中有着重要的地位。"])
    return random.choice(templates)

# 显示角色评分界面
def show_rating_interface():
    st.markdown('<div class="main-header">♟️ 后翼弃兵角色评分系统</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">虎扑风格 · AI智能分析 · 真实角色数据</div>', unsafe_allow_html=True)
    
    # 显示统计信息
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="stat-card"><h3>📊 总评分次数</h3><div style="font-size: 2rem;">' + 
                   str(st.session_state.rating_sessions) + '</div></div>', unsafe_allow_html=True)
    with col2:
        total_ratings = sum(st.session_state.characters_df['rating_count'])
        st.markdown('<div class="stat-card"><h3>👥 参与用户</h3><div style="font-size: 2rem;">' + 
                   f"{total_ratings:,}" + '</div></div>', unsafe_allow_html=True)
    with col3:
        avg_rating = st.session_state.characters_df['avg_rating'].mean()
        st.markdown('<div class="stat-card"><h3>⭐ 平均评分</h3><div style="font-size: 2rem;">' + 
                   f"{avg_rating:.1f}" + '</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="stat-card"><h3>🎬 剧集热度</h3><div style="font-size: 2rem;">9.8</div></div>', unsafe_allow_html=True)
    
    # 角色选择
    st.markdown('<div class="rating-section"><h3>🎯 选择你要评分的角色</h3></div>', unsafe_allow_html=True)
    
    characters_df = st.session_state.characters_df
    
    # 显示所有角色卡片
    for index, character in characters_df.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 3])
            
            with col1:
                # 显示角色图片
                st.image(character['image_url'], width=200, caption=character['name'])
            
            with col2:
                st.markdown(f'<div class="character-card">', unsafe_allow_html=True)
                
                # 角色基本信息
                st.markdown(f'### {character["name"]} - {character["role"]}')
                st.markdown(f'**{character["description"]}**')
                
                # MBTI信息
                st.markdown(f'🧠 **MBTI类型**: {character["mbti_type"]}')
                st.markdown(f'*{character["mbti_description"]}*')
                
                # 评分信息
                col21, col22, col23 = st.columns(3)
                with col21:
                    st.markdown(f'⭐ **平均评分**: {character["avg_rating"]}')
                with col22:
                    st.markdown(f'👥 **评分人数**: {character["rating_count"]:,}')
                with col23:
                    st.markdown(f'🔥 **角色热度**: {random.randint(85, 98)}%')
                
                # 虎扑风格标签
                tags = ["象棋天才", "成长励志", "女性力量", "时代印记"]
                tag_html = ''.join([f'<span class="meme-tag">{tag}</span>' for tag in random.sample(tags, 2)])
                st.markdown(tag_html, unsafe_allow_html=True)
                
                # 评分滑块
                current_rating = st.session_state.character_ratings.get(character['name'], 5)
                new_rating = st.slider(
                    f'为{character["name"]}评分（1-10分）',
                    min_value=1,
                    max_value=10,
                    value=current_rating,
                    key=f"rating_{character['name']}"
                )
                
                # 更新评分
                if new_rating != current_rating:
                    st.session_state.character_ratings[character['name']] = new_rating
                    st.session_state.rating_sessions += 1
                    st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    # 显示热评
    st.markdown('<div class="rating-section"><h3>💬 虎扑热评</h3></div>', unsafe_allow_html=True)
    
    rated_characters = [name for name, rating in st.session_state.character_ratings.items() if rating > 0]
    if rated_characters:
        for character_name in rated_characters:
            comments = get_hot_comments(character_name)
            for comment in random.sample(comments, min(2, len(comments))):
                st.markdown(f'<div class="hot-comment"><strong>{character_name}</strong>: {comment}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="hot-comment">暂无评分，快来为你喜欢的角色打分吧！</div>', unsafe_allow_html=True)
    
    # AI分析
    if st.session_state.character_ratings:
        st.markdown('<div class="rating-section"><h3>🤖 AI智能角色分析</h3></div>', unsafe_allow_html=True)
        
        for character_name, rating in st.session_state.character_ratings.items():
            analysis = generate_ai_analysis(character_name, rating)
            st.markdown(f'**{character_name}（评分：{rating}分）**: {analysis}')

# 显示演员信息
def show_actor_info():
    st.markdown('<div class="rating-section"><h3>🎭 演员信息</h3></div>', unsafe_allow_html=True)
    
    characters_df = st.session_state.characters_df
    
    for index, character in characters_df.iterrows():
        with st.container():
            st.markdown('<div class="actor-section">', unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 3])
            
            with col1:
                # 显示演员照片
                st.image(character['actor_photo_url'], width=120, caption=character['actor_name'])
            
            with col2:
                st.markdown(f'<div class="actor-info">', unsafe_allow_html=True)
                st.markdown(f'<span class="actor-name">{character["actor_name"]}</span>', unsafe_allow_html=True)
                st.markdown(f'**饰演**: {character["name"]}')
                st.markdown(f'{character["actor_bio"]}')
                
                # 代表作品
                st.markdown('**代表作品**:')
                works_html = '<div class="works-grid">'
                for work in character['famous_works']:
                    works_html += f'<div class="work-item">{work}</div>'
                works_html += '</div>'
                st.markdown(works_html, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

# 显示作品海报
def show_work_posters():
    st.markdown('<div class="rating-section"><h3>🎬 相关作品海报</h3></div>', unsafe_allow_html=True)
    
    # 获取所有作品
    all_works = set()
    for works in st.session_state.characters_df['famous_works']:
        all_works.update(works)
    
    # 显示作品海报
    works_list = list(all_works)
    cols = st.columns(3)
    
    for i, work in enumerate(works_list):
        with cols[i % 3]:
            work_image = get_work_images(work)
            st.image(work_image, caption=work, use_container_width=True)
            st.markdown(f'**{work}**')

# 主函数
def main():
    init_data()
    
    # 侧边栏
    st.sidebar.title("♟️ 导航菜单")
    menu_options = ["角色评分", "演员信息", "作品海报"]
    selected_menu = st.sidebar.radio("选择功能", menu_options)
    
    # 根据选择显示不同内容
    if selected_menu == "角色评分":
        show_rating_interface()
    elif selected_menu == "演员信息":
        show_actor_info()
    elif selected_menu == "作品海报":
        show_work_posters()
    
    # 页脚信息
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 数据统计")
    st.sidebar.markdown(f"**总评分次数**: {st.session_state.rating_sessions}")
    st.sidebar.markdown(f"**已评分角色**: {len(st.session_state.character_ratings)}")
    
    if st.session_state.character_ratings:
        avg_user_rating = sum(st.session_state.character_ratings.values()) / len(st.session_state.character_ratings)
        st.sidebar.markdown(f"**你的平均评分**: {avg_user_rating:.1f}")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("*数据来源: 维基百科 + 虎扑社区*")

if __name__ == "__main__":
    main()