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
    page_title="🔪 轮到你了角色评分 - 虎扑风格",
    page_icon="🔍",
    layout="wide"
)

# 自定义CSS样式 - 悬疑主题风格
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
    
    .main-header {
        font-family: 'Noto Sans SC', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(45deg, #8B0000, #B22222, #DC143C, #FF0000);
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
        border-left: 4px solid #8B0000;
        transition: all 0.3s ease;
    }
    .character-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    .rating-section {
        background: linear-gradient(135deg, #B22222 0%, #8B0000 100%);
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
        background-color: #FFB6C1;
        color: #8B0000;
        padding: 0.4rem 1rem;
        margin: 0.3rem;
        border-radius: 15px;
        font-size: 1rem;
        font-weight: bold;
    }
    .hot-comment {
        background-color: #FFF0F5;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid #8B0000;
        color: #8B0000;
        font-weight: 500;
    }
    .score-badge {
        background-color: #B22222;
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
        background: linear-gradient(135deg, #B22222, #DC143C);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 1.2rem;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
        box-shadow: 0 4px 8px rgba(178, 34, 34, 0.3);
    }
    .stat-card {
        background: linear-gradient(135deg, #B22222 0%, #8B0000 100%);
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
        border: 4px solid #8B0000;
        margin: 0 auto;
        display: block;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .actor-section {
        background: linear-gradient(135deg, #DC143C 0%, #B22222 100%);
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
    .suspicion-badge {
        background: linear-gradient(135deg, #4B0082, #8A2BE2);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
        display: inline-block;
        margin: 0.2rem;
    }
    .clue-section {
        background: linear-gradient(135deg, #4B0082 0%, #8A2BE2 100%);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        color: white;
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

# 轮到你了角色数据
def initialize_characters():
    characters_data = {
        'id': range(1, 9),
        'name': ['手塚翔太', '手塚菜奈', '黑岛沙和', '尾野干叶', '二阶堂忍', '木下', '藤井淳史', '管理员床岛'],
        'role': ['主角/侦探', '温柔妻子', '数学天才', '神秘邻居', 'AI研究员', '情报收集者', '外科医生', '公寓管理员'],
        'description': [
            '运动品牌公司职员，努力查明交换杀人游戏的真相',
            '翔太的妻子，温柔善良，喜欢推理小说',
            '东京大学数学系学生，聪明冷静的天才少女',
            '行为古怪的神秘美女，对翔太异常执着',
            'AI研究员，开发了分析杀人犯的AI系统',
            '喜欢收集情报的怪人，掌握公寓内各种信息',
            '性格懦弱的外科医生，被卷入杀人游戏',
            '公寓管理员，交换杀人游戏的发起者'
        ],
        'suspicion_level': ['低嫌疑', '受害者', '高嫌疑', '中嫌疑', '低嫌疑', '中嫌疑', '高嫌疑', '受害者'],
        'suspicion_description': [
            '作为主角积极调查真相，嫌疑较低但行为可疑',
            '在第一轮游戏中不幸遇害，是重要受害者',
            '数学天才但行为神秘，多次出现在案发现场',
            '行为诡异的神秘美女，有强烈作案动机',
            'AI研究员帮助破案，但AI分析结果令人怀疑',
            '情报收集者可能知道太多秘密而成为目标',
            '性格懦弱但被威胁参与游戏，行为反常',
            '游戏发起者，第一个受害者，掌握关键信息'
        ],
        'mbti_type': ['ENFJ', 'ISFJ', 'INTJ', 'ENFP', 'INTP', 'ISTJ', 'ISFP', 'ESTJ'],
        'mbti_description': [
            'ENFJ（主人公型）：富有同情心，善于沟通，有领导才能',
            'ISFJ（守护者型）：温柔体贴，重视家庭，有责任感',
            'INTJ（建筑师型）：理性冷静，逻辑思维强，目标明确',
            'ENFP（竞选者型）：热情外向，好奇心强，行为难以预测',
            'INTP（逻辑学家型）：理性分析，独立思考，技术宅',
            'ISTJ（物流师型）：注重细节，可靠踏实，信息收集者',
            'ISFP（探险家型）：敏感细腻，避免冲突，艺术气质',
            'ESTJ（总经理型）：务实果断，重视规则，管理能力强'
        ],
        'actor_name': ['田中圭', '原田知世', '西野七濑', '奈绪', '横滨流星', '田中哲司', '浅香航大', '竹中直人'],
        'actor_bio': [
            '日本实力派演员，以阳光形象和扎实演技著称，代表作众多。',
            '日本资深女演员，演技细腻自然，能够演绎复杂内心戏。',
            '日本新生代女演员，原偶像团体成员，转型演员成功。',
            '日本新生代女演员，擅长演绎性格复杂的角色。',
            '日本当红男演员，模特出身，演技和颜值俱佳。',
            '日本实力派演员，戏路宽广，能够驾驭各种角色类型。',
            '日本新生代男演员，演技自然生动，角色塑造力强。',
            '日本资深演员，喜剧和正剧都能出色演绎的老戏骨。'
        ],
        'famous_works': [
            ['轮到你了', '大叔的爱', '朝5晚9'],
            ['轮到你了', '冬季运动会', '犯罪症候群'],
            ['轮到你了', '虹色时光', '电影 啦啦队之舞'],
            ['轮到你了', '绝叫', '约定的梦幻岛'],
            ['轮到你了', '初恋那天所读的故事', '消失的初恋'],
            ['轮到你了', 'Doctor-X', '半泽直树'],
            ['轮到你了', '对不起青春！', '东京白日梦女'],
            ['轮到你了', '东京爱情故事', '青之炎']
        ],
        'avg_rating': [9.2, 8.8, 9.4, 8.9, 8.7, 8.5, 8.3, 8.6],
        'rating_count': [15200, 13800, 16500, 14200, 12800, 11800, 11200, 12500],
        'image_url': [
            'https://via.placeholder.com/200x300/8B0000/FFFFFF?text=手塚翔太',
            'https://via.placeholder.com/200x300/B22222/FFFFFF?text=手塚菜奈',
            'https://via.placeholder.com/200x300/DC143C/FFFFFF?text=黑岛沙和',
            'https://via.placeholder.com/200x300/FF0000/FFFFFF?text=尾野干叶',
            'https://via.placeholder.com/200x300/4B0082/FFFFFF?text=二阶堂忍',
            'https://via.placeholder.com/200x300/8A2BE2/FFFFFF?text=木下',
            'https://via.placeholder.com/200x300/9370DB/FFFFFF?text=藤井淳史',
            'https://via.placeholder.com/200x300/800080/FFFFFF?text=床岛'
        ],
        'actor_photo_url': [
            'https://via.placeholder.com/200x300/2196F3/FFFFFF?text=田中圭',
            'https://via.placeholder.com/200x300/4CAF50/FFFFFF?text=原田知世',
            'https://via.placeholder.com/200x300/FF9800/FFFFFF?text=西野七濑',
            'https://via.placeholder.com/200x300/F44336/FFFFFF?text=奈绪',
            'https://via.placeholder.com/200x300/9C27B0/FFFFFF?text=横滨流星',
            'https://via.placeholder.com/200x300/607D8B/FFFFFF?text=田中哲司',
            'https://via.placeholder.com/200x300/795548/FFFFFF?text=浅香航大',
            'https://via.placeholder.com/200x300/009688/FFFFFF?text=竹中直人'
        ]
    }
    return pd.DataFrame(characters_data)

# 代表作品图片映射
def get_work_images(work_name):
    work_images = {
        '轮到你了': 'https://via.placeholder.com/200x300/8B0000/FFFFFF?text=轮到你了',
        '大叔的爱': 'https://via.placeholder.com/200x300/2196F3/FFFFFF?text=大叔的爱',
        '朝5晚9': 'https://via.placeholder.com/200x300/9C27B0/FFFFFF?text=朝5晚9',
        '冬季运动会': 'https://via.placeholder.com/200x300/FF9800/FFFFFF?text=冬季运动会',
        '犯罪症候群': 'https://via.placeholder.com/200x300/E91E63/FFFFFF?text=犯罪症候群',
        '虹色时光': 'https://via.placeholder.com/200x300/00BCD4/FFFFFF?text=虹色时光',
        '电影 啦啦队之舞': 'https://via.placeholder.com/200x300/3F51B5/FFFFFF?text=啦啦队',
        '绝叫': 'https://via.placeholder.com/200x300/FF5722/FFFFFF?text=绝叫',
        '约定的梦幻岛': 'https://via.placeholder.com/200x300/8BC34A/FFFFFF?text=梦幻岛',
        '初恋那天所读的故事': 'https://via.placeholder.com/200x300/673AB7/FFFFFF?text=初恋',
        '消失的初恋': 'https://via.placeholder.com/200x300/009688/FFFFFF?text=消失初恋',
        'Doctor-X': 'https://via.placeholder.com/200x300/E91E63/FFFFFF?text=Doctor-X',
        '半泽直树': 'https://via.placeholder.com/200x300/00BCD4/FFFFFF?text=半泽直树',
        '对不起青春！': 'https://via.placeholder.com/200x300/3F51B5/FFFFFF?text=对不起青春',
        '东京白日梦女': 'https://via.placeholder.com/200x300/FF4081/FFFFFF?text=白日梦女',
        '东京爱情故事': 'https://via.placeholder.com/200x300/3F51B5/FFFFFF?text=东爱',
        '青之炎': 'https://via.placeholder.com/200x300/009688/FFFFFF?text=青之炎'
    }
    return work_images.get(work_name, 'https://via.placeholder.com/200x300/666666/FFFFFF?text=默认作品')

# 角色相关的梗和热评
def get_character_memes(character_id):
    memes_dict = {
        1: ["我会找出真相", "菜奈...", "交换杀人游戏", "公寓侦探"],
        2: ["温柔的菜奈", "推理小说迷", "第一受害者", "永远的痛"],
        3: ["数学天才", "黑岛是凶手?", "冷静的可怕", "反转再反转"],
        4: ["尾野的礼物", "神秘美女", "行为诡异", "执着跟踪"],
        5: ["AI分析", "技术宅救星", "黑岛男友", "理性分析"],
        6: ["情报王", "垃圾搜查", "掌握秘密", "信息达人"],
        7: ["懦弱医生", "被威胁参与", "外科手术", "压力山大"],
        8: ["游戏发起者", "第一个死者", "管理员之死", "关键线索"]
    }
    
    comments_dict = {
        1: ["翔太的坚持让人感动，为了菜奈一定要找出真相", "作为主角真的很努力了，每次看到他想哭又坚强的样子就心疼"],
        2: ["菜奈的死是整个故事的转折点，温柔的大姐姐太可惜了", "原田知世的演技太好了，把菜奈的温柔和坚强都演活了"],
        3: ["黑岛这个角色太复杂了，到底是天才还是恶魔？", "西野七濑的演技突破很大，从偶像成功转型演员"],
        4: ["尾野干叶绝对是剧中最毛骨悚然的角色，每次出现都起鸡皮疙瘩", "奈绪的表演太出色了，把那种诡异的美感演绎得淋漓尽致"],
        5: ["二阶堂的AI分析是破案关键，理科男的浪漫", "横滨流星颜值演技都在线，和黑岛的CP感很强"],
        6: ["木下这个情报通太重要了，没有他很多线索都发现不了", "田中哲司的老戏骨演技，把怪人演得活灵活现"],
        7: ["藤井医生太惨了，被卷入游戏身不由己", "浅香航大把医生的懦弱和挣扎演得很真实"],
        8: ["管理员的死拉开了整个故事的序幕，竹中直人的演技没话说", "作为游戏发起者，管理员知道太多秘密了"]
    }
    
    memes = memes_dict.get(character_id, [])
    comments = comments_dict.get(character_id, [])
    return memes[:3], comments[:2]

# 五星评分系统
def star_rating_component(character_id, current_rating=0):
    rating_options = ["未评分", "1星 ⭐", "2星 ⭐⭐", "3星 ⭐⭐⭐", "4星 ⭐⭐⭐⭐", "5星 ⭐⭐⭐⭐⭐"]
    
    rating_key = f"rating_{character_id}"
    
    if current_rating > 0:
        st.markdown(f'<div style="text-align: center; background: #B22222; color: white; padding: 8px; border-radius: 10px; margin: 10px 0;">您已评分: {current_rating}星</div>', unsafe_allow_html=True)
    
    selected_rating = st.selectbox(
        "选择评分",
        options=rating_options,
        index=current_rating,
        key=rating_key
    )
    
    new_rating = rating_options.index(selected_rating)
    
    if new_rating != current_rating and new_rating > 0:
        st.session_state.character_ratings[character_id] = new_rating
        st.session_state.rating_sessions += 1
        st.success(f"✅ 已为{st.session_state.characters_df[st.session_state.characters_df['id'] == character_id]['name'].iloc[0]}评分 {new_rating}星")
        st.rerun()
    
    return None

# 角色评分界面
def character_rating_interface():
    st.markdown('<div class="main-header">🔪 轮到你了角色评分</div>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">✨ 虎扑风格评分系统 · 悬疑主题 · 热评互动</p>', unsafe_allow_html=True)
    
    # 侧边栏 - 筛选器
    with st.sidebar:
        st.header("🔍 筛选设置")
        
        # 角色类型筛选
        roles = ['全部'] + list(st.session_state.characters_df['role'].unique())
        selected_role = st.selectbox("角色类型", roles)
        
        # 嫌疑程度筛选
        suspicion_levels = ['全部'] + list(st.session_state.characters_df['suspicion_level'].unique())
        selected_suspicion = st.selectbox("嫌疑程度", suspicion_levels)
        
        # 评分范围
        min_score, max_score = st.slider(
            "评分范围", 
            min_value=0.0, 
            max_value=10.0, 
            value=(7.5, 9.5),
            step=0.1
        )
        
        # 搜索框
        search_term = st.text_input("🔎 搜索角色", placeholder="输入角色名或描述...")
        
        # 应用筛选
        filtered_characters = st.session_state.characters_df.copy()
        if selected_role != '全部':
            filtered_characters = filtered_characters[filtered_characters['role'] == selected_role]
        
        if selected_suspicion != '全部':
            filtered_characters = filtered_characters[filtered_characters['suspicion_level'] == selected_suspicion]
        
        filtered_characters = filtered_characters[
            (filtered_characters['avg_rating'] >= min_score) & 
            (filtered_characters['avg_rating'] <= max_score)
        ]
        
        if search_term:
            filtered_characters = filtered_characters[
                filtered_characters['name'].str.contains(search_term, case=False) |
                filtered_characters['description'].str.contains(search_term, case=False)
            ]
    
    # 主内容区
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("👥 角色评分区")
        
        # 排序选项
        sort_by = st.selectbox("排序方式", ["综合评分", "评分人数", "角色名称", "嫌疑程度"])
        
        if sort_by == "综合评分":
            ranked_characters = filtered_characters.sort_values('avg_rating', ascending=False)
        elif sort_by == "评分人数":
            ranked_characters = filtered_characters.sort_values('rating_count', ascending=False)
        elif sort_by == "嫌疑程度":
            # 自定义嫌疑程度排序
            suspicion_order = {'受害者': 0, '低嫌疑': 1, '中嫌疑': 2, '高嫌疑': 3}
            ranked_characters = filtered_characters.copy()
            ranked_characters['suspicion_order'] = ranked_characters['suspicion_level'].map(suspicion_order)
            ranked_characters = ranked_characters.sort_values('suspicion_order')
        else:
            ranked_characters = filtered_characters.sort_values('name', ascending=True)
        
        # 角色展示和评分
        for _, character in ranked_characters.iterrows():
            with st.container():
                st.markdown(f'<div class="character-card">', unsafe_allow_html=True)
                
                # 角色信息布局
                col_a, col_b = st.columns([2, 3])
                
                with col_a:
                    st.image(character['image_url'], width='stretch', caption=character['name'])
                    
                    # 嫌疑程度徽章
                    st.markdown(f'<div class="suspicion-badge" style="text-align: center; margin-top: 10px;">嫌疑程度: {character["suspicion_level"]}</div>', 
                               unsafe_allow_html=True)
                    
                    st.markdown(f'<div class="score-highlight" style="text-align: center; margin-top: 10px;">评分: {character["avg_rating"]}</div>', 
                               unsafe_allow_html=True)
                    st.markdown(f'<div style="text-align: center; font-size: 0.9rem; color: #666; margin-top: 5px;">👥 {character["rating_count"]}人评分</div>', 
                               unsafe_allow_html=True)
                
                with col_b:
                    st.markdown(f"<h2 style='font-size: 1.8rem; margin-bottom: 10px;'>{character['name']}</h2>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size: 1.2rem; font-weight: bold; color: #8B0000; margin-bottom: 8px;'>身份: {character['role']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size: 1.1rem; line-height: 1.4; margin-bottom: 15px;'>{character['description']}</p>", unsafe_allow_html=True)
                    
                    # 嫌疑描述
                    st.markdown(f"<p style='font-size: 1rem; color: #B22222; margin-bottom: 15px;'><strong>嫌疑分析:</strong> {character['suspicion_description']}</p>", unsafe_allow_html=True)
                    
                    # 虎扑式热评和梗
                    memes, comments = get_character_memes(character['id'])
                    
                    if memes:
                        st.markdown("<h4 style='font-size: 1.3rem; margin-bottom: 10px;'>🔥 角色热梗</h4>", unsafe_allow_html=True)
                        meme_cols = st.columns(len(memes))
                        for i, meme in enumerate(memes):
                            with meme_cols[i]:
                                st.markdown(f'<div class="meme-tag" style="font-size: 1rem;">{meme}</div>', unsafe_allow_html=True)
                    
                    # 五星评分系统
                    st.markdown("### ⭐ 为角色评分")
                    current_user_rating = st.session_state.character_ratings.get(character['id'], 0)
                    
                    star_rating_component(character['id'], current_user_rating)
                    
                    # 显示热评
                    if comments:
                        st.markdown("<h4 style='font-size: 1.3rem; margin-bottom: 10px;'>💬 虎扑热评</h4>", unsafe_allow_html=True)
                        for comment in comments:
                            st.markdown(f'<div class="hot-comment" style="font-size: 1.1rem; line-height: 1.4;">{comment}</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.write("---")
    
    with col2:
        st.subheader("📊 实时统计")
        
        # 统计卡片
        total_characters = len(filtered_characters)
        avg_rating = filtered_characters['avg_rating'].mean() if total_characters > 0 else 0
        total_ratings = filtered_characters['rating_count'].sum()
        
        col_stat1, col_stat2 = st.columns(2)
        
        with col_stat1:
            st.markdown(f'''
            <div class="stat-card">
                <h3>👥 角色数量</h3>
                <div style="font-size: 1.5rem; font-weight: bold;">{total_characters}</div>
            </div>
            ''', unsafe_allow_html=True)
            
            st.markdown(f'''
            <div class="stat-card">
                <h3>⭐ 平均评分</h3>
                <div style="font-size: 1.5rem; font-weight: bold;">{avg_rating:.1f}</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col_stat2:
            st.markdown(f'''
            <div class="stat-card">
                <h3>📈 总评分数</h3>
                <div style="font-size: 1.5rem; font-weight: bold;">{total_ratings:,}</div>
            </div>
            ''', unsafe_allow_html=True)
            
            user_rated_count = len(st.session_state.character_ratings)
            st.markdown(f'''
            <div class="stat-card">
                <h3>🎯 我已评分</h3>
                <div style="font-size: 1.5rem; font-weight: bold;">{user_rated_count}</div>
            </div>
            ''', unsafe_allow_html=True)
        
        # 嫌疑程度分布
        st.subheader("🔍 嫌疑程度分布")
        suspicion_counts = filtered_characters['suspicion_level'].value_counts()
        for level, count in suspicion_counts.items():
            st.markdown(f"<div style='font-size: 1.2rem; margin-bottom: 10px;'>{level}: <strong>{count}</strong> 人</div>", unsafe_allow_html=True)
        
        # 排行榜
        st.subheader("🏆 角色排行榜")
        
        for i, (_, character) in enumerate(ranked_characters.head(5).iterrows(), 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            
            st.markdown(f"<div style='font-size: 1.2rem; margin-bottom: 10px;'>{medal} <strong>{character['name']}</strong></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 1.1rem; margin-bottom: 5px;'>  评分: <strong>{character['avg_rating']}</strong> 🌟</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 1.1rem; margin-bottom: 5px;'>  嫌疑: {character['suspicion_level']}</div>", unsafe_allow_html=True)
            
            # 显示用户评分
            user_score = st.session_state.character_ratings.get(character['id'])
            if user_score:
                st.markdown(f"<div style='font-size: 1.1rem; margin-bottom: 10px;'>  我的评分: <strong>{user_score}</strong> 🌟</div>", unsafe_allow_html=True)
            
            st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)

# AI角色分析界面
def ai_character_analysis():
    st.markdown("## 🔮 AI角色深度解析")
    st.markdown("### 💫 让AI帮你分析角色特点和悬疑线索")
    
    # 角色选择
    character_names = [char['name'] for _, char in st.session_state.characters_df.iterrows()]
    selected_character = st.selectbox("选择要分析的角色", character_names, key="ai_character")
    
    # 获取角色数据
    character_data = st.session_state.characters_df[st.session_state.characters_df['name'] == selected_character].iloc[0]
    actor_name = character_data['actor_name']
    famous_works = character_data['famous_works']
    
    # 分析维度选择
    analysis_type = st.selectbox("分析维度", 
                                ["角色性格分析", "嫌疑分析", "剧情作用分析", "演技评价", "观众共鸣点", "角色成长轨迹", "演员简介", "代表作品分析"])
    
    if st.button("🔮 启动AI分析", type="primary", key="ai_analyze"):
        with st.spinner('AI正在深度解析角色...'):
            time.sleep(2)
            
            # 模拟AI分析结果
            analysis_results = {
                "角色性格分析": [
                    f"**{selected_character}**的性格在《轮到你了》中极具特色，展现了在悬疑环境中的独特表现",
                    f"**MBTI性格类型**: **{character_data['mbti_type']}** - {character_data['mbti_description']}",
                    f"**性格特点**: {character_data['mbti_description'].split('：')[1]}",
                    f"在交换杀人游戏的极端环境下，{selected_character}的性格特点得到了充分展现",
                    f"角色的人际关系处理方式体现了其性格的核心特征",
                    f"面对生死威胁，{selected_character}展现出了独特的应对策略",
                    f"性格中的优缺点在剧情发展中起到了关键作用",
                    f"与其他角色的互动展现了{selected_character}性格的多面性"
                ],
                "嫌疑分析": [
                    f"**{selected_character}**的嫌疑程度为: **{character_data['suspicion_level']}**",
                    f"**嫌疑分析**: {character_data['suspicion_description']}",
                    f"在交换杀人游戏中，{selected_character}的行为模式值得深入分析",
                    f"角色的动机和机会需要结合具体案件进行考量",
                    f"面对警方调查时，{selected_character}展现出了独特的应对方式",
                    f"与其他角色的关系网也是分析嫌疑的重要线索",
                    f"角色的不在场证明和心理变化是破案关键"
                ],
                "剧情作用分析": [
                    f"**{selected_character}**在《轮到你了》剧情中扮演着重要角色",
                    f"作为{character_data['role']}，在交换杀人游戏中发挥了独特作用",
                    f"与其他角色的互动推动了剧情的关键发展",
                    f"在真相揭露过程中，{selected_character}代表了重要的线索节点",
                    f"角色的选择和行动往往成为剧情转折的关键",
                    f"成长轨迹与主线剧情发展高度契合",
                    f"在悬疑解谜中展现了不可替代的价值"
                ],
                "演技评价": [
                    f"**{actor_name}**的表演为{selected_character}注入了灵魂",
                    "表演特点与角色性格高度契合，增强了角色的可信度",
                    "情感表达的层次感丰富，能够准确传达角色的内心世界",
                    "在关键场景中的表演张力十足，给观众留下深刻印象",
                    "台词处理自然流畅，语气变化恰到好处",
                    "能够通过表演展现角色的成长和变化",
                    "整体表演风格与《轮到你了》的悬疑主题完美融合"
                ],
                "观众共鸣点": [
                    f"**{selected_character}**的角色设定引发了观众的强烈共鸣",
                    "在交换杀人游戏的背景下，角色的个人挣扎让观众感同身受",
                    "面对死亡威胁时的恐惧和勇气让观众揪心",
                    "与其他角色的友情和羁绊让人感动",
                    "解谜过程中的智慧展现引发了观众的敬佩",
                    "角色的命运发展牵动着观众的心弦",
                    "在极端环境下的选择引发了观众的深度思考"
                ],
                "角色成长轨迹": [
                    f"**{selected_character}**在《轮到你了》中经历了显著的成长",
                    "从普通居民到卷入杀人游戏，角色不断突破自我",
                    "心理承受能力/推理能力/勇气等方面都有明显提升",
                    "价值观和世界观随着经历不断成熟和完善",
                    "与其他角色的关系发展也反映了角色的成长",
                    "面对死亡威胁时的应对方式展现了角色的心理成长",
                    "最终的角色定位与初期形成了鲜明对比"
                ],
                "演员简介": [
                    f"**{actor_name}**是日本实力派演员，在《轮到你了》中成功塑造了**{selected_character}**这一经典角色",
                    f"**{actor_name}**的表演风格独特，能够准确把握角色的核心特质",
                    f"通过**{selected_character}**这一角色，**{actor_name}**展现了出色的演技实力",
                    f"**演员简介**: {character_data['actor_bio']}",
                    f"**代表作品**: {', '.join(famous_works)}",
                    f"**表演特点**: 演技富有层次感，角色塑造真实可信",
                    f"**角色理解**: 能够深入理解角色内心，表演富有感染力"
                ],
                "代表作品分析": [
                    f"**{actor_name}**的代表作品包括：**{famous_works[0]}**、**{famous_works[1]}**、**{famous_works[2]}**",
                    f"在**{famous_works[0]}**中，**{actor_name}**展现了出色的演技和角色塑造能力",
                    f"**{famous_works[1]}**是**{actor_name}**的另一部重要作品，展现了其多样化的表演风格",
                    f"通过**{famous_works[2]}**，**{actor_name}**进一步巩固了在演艺界的地位",
                    f"这些作品共同展现了**{actor_name}**宽广的戏路和扎实的表演功底",
                    f"在不同类型作品中的表现证明了**{actor_name}**的专业实力"
                ]
            }
            
            # 显示分析结果
            if analysis_type in ["演员简介", "代表作品分析"]:
                col_img, col_comments = st.columns([1, 2])
                
                with col_img:
                    st.image(character_data['actor_photo_url'], width=300, caption=f"演员: {actor_name}")
                
                with col_comments:
                    st.success(f"### 🎯 AI对**{selected_character}**的{analysis_type}")
                    
                    points_to_show = analysis_results[analysis_type][:4]
                    for point in points_to_show:
                        st.info(f"✨ {point}")
                
                remaining_points = analysis_results[analysis_type][4:]
                if remaining_points:
                    st.markdown("---")
                    st.markdown("### 📝 更多分析")
                    for point in remaining_points:
                        st.info(f"✨ {point}")
            else:
                st.success(f"### 🎯 AI对**{selected_character}**的{analysis_type}")
                
                col_img, col_comments = st.columns([1, 2])
                
                with col_img:
                    st.image(character_data['image_url'], width=300, caption=selected_character)
                
                with col_comments:
                    points_to_show = analysis_results[analysis_type][:4]
                    for point in points_to_show:
                        st.info(f"✨ {point}")
                
                remaining_points = analysis_results[analysis_type][4:]
                if remaining_points:
                    st.markdown("---")
                    st.markdown("### 📝 更多分析")
                    for point in remaining_points:
                        st.info(f"✨ {point}")
            
            # 如果是代表作品分析，显示作品图片
            if analysis_type == "代表作品分析":
                st.markdown("### 🎬 代表作品展示")
                work_cols = st.columns(len(famous_works))
                for i, work in enumerate(famous_works):
                    with work_cols[i]:
                        work_image = get_work_images(work)
                        st.image(work_image, width=200, caption=work)
            
            # 显示评分统计
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("当前评分", f"{character_data['avg_rating']}")
            with col2:
                st.metric("评分人数", f"{character_data['rating_count']:,}")
            with col3:
                user_rating = st.session_state.character_ratings.get(character_data['id'], "未评分")
                st.metric("我的评分", user_rating)

# 主程序
def main():
    # 初始化数据
    init_data()
    
    # 标签页导航
    tab1, tab2 = st.tabs(["👥 角色评分", "🔮 AI分析"])
    
    with tab1:
        character_rating_interface()
    
    with tab2:
        ai_character_analysis()

if __name__ == "__main__":
    main()