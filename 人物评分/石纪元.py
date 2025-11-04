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
    page_title="🔬 石纪元角色评分 - 虎扑风格",
    page_icon="⚗️",
    layout="wide"
)

# 自定义CSS样式 - 科学主题风格
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
    
    .main-header {
        font-family: 'Noto Sans SC', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(45deg, #2E7D32, #43A047, #66BB6A, #388E3C);
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
        border-left: 4px solid #2E7D32;
        transition: all 0.3s ease;
    }
    .character-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    .rating-section {
        background: linear-gradient(135deg, #66BB6A 0%, #388E3C 100%);
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
        color: #1B5E20;
        padding: 0.4rem 1rem;
        margin: 0.3rem;
        border-radius: 15px;
        font-size: 1rem;
        font-weight: bold;
    }
    .hot-comment {
        background-color: #E8F5E9;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid #388E3C;
        color: #2E7D32;
        font-weight: 500;
    }
    .score-badge {
        background-color: #43A047;
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
        background: linear-gradient(135deg, #4CAF50, #66BB6A);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 1.2rem;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
        box-shadow: 0 4px 8px rgba(76, 175, 80, 0.3);
    }
    .stat-card {
        background: linear-gradient(135deg, #66BB6A 0%, #388E3C 100%);
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
        border: 4px solid #2E7D32;
        margin: 0 auto;
        display: block;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .actor-section {
        background: linear-gradient(135deg, #81C784 0%, #4CAF50 100%);
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
    .science-badge {
        background: linear-gradient(135deg, #2196F3, #1976D2);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
        display: inline-block;
        margin: 0.2rem;
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

# 石纪元角色数据
def initialize_characters():
    characters_data = {
        'id': range(1, 8),
        'name': ['千空', '大树', '小川杠', '狮子王司', '克罗姆', '琥珀', '琉璃'],
        'role': ['科学天才', '体力担当', '技术专家', '武力领袖', '科学助手', '村落战士', '巫女'],
        'description': [
            '拥有超人科学知识的高中生，目标是复兴全人类文明',
            '千空的好友，拥有超强体力的高中生',
            '科学王国技术部部长，擅长制造和工程',
            '司帝国的创立者，拥有超凡武力的青年',
            '石化前就对科学有兴趣的少年，千空的得力助手',
            '石神村的战士，身手敏捷的少女',
            '石神村的巫女，拥有预知能力的少女'
        ],
        'science_level': ['超天才级', '普通级', '专家级', '普通级', '优秀级', '普通级', '特殊能力'],
        'science_description': [
            '掌握从零重建文明所需的全部科学知识，记忆力超群',
            '体力超群但科学知识有限，擅长执行体力任务',
            '工程技术专家，能够将千空的构想变为现实',
            '武力值MAX，但对科学知识了解有限',
            '对科学有浓厚兴趣，学习能力强，千空的优秀助手',
            '战斗技能优秀，对科学知识逐渐学习',
            '拥有预知未来的特殊能力，对科学有独特理解'
        ],
        'mbti_type': ['INTP', 'ESFJ', 'ISTJ', 'ENTJ', 'ENFP', 'ESTP', 'INFJ'],
        'mbti_description': [
            'INTP（逻辑学家型）：天才科学家性格，逻辑思维强，好奇心旺盛，理性分析',
            'ESFJ（执政官型）：忠诚伙伴，重视友情，乐于助人，团队精神强',
            'ISTJ（物流师型）：务实工程师，注重细节，可靠踏实，执行力强',
            'ENTJ（指挥官型）：强势领袖，目标明确，决策果断，领导力强',
            'ENFP（竞选者型）：热情学习者，好奇心强，富有创意，适应力强',
            'ESTP（企业家型）：行动派战士，勇敢果断，实践能力强，冒险精神',
            'INFJ（提倡者型）：神秘巫女，直觉敏锐，富有洞察力，理想主义'
        ],
        'actor_name': ['小林裕介', '古川慎', '市之濑加那', '中村悠一', '佐藤元', '上田丽奈', '沼仓爱美'],
        'actor_bio': [
            '日本实力派声优，以演绎理性冷静的天才角色见长，声音富有辨识度。',
            '日本新生代声优，擅长演绎热血真诚的角色，声线温暖富有感染力。',
            '日本女声优，声音清澈甜美，擅长演绎聪明能干的女性角色。',
            '日本资深声优，声线低沉富有磁性，擅长演绎强势领袖型角色。',
            '日本新生代声优，演技自然生动，擅长演绎活泼热情的少年角色。',
            '日本实力派女声优，声线多变，能够演绎从可爱到帅气的各种角色。',
            '日本女声优，声音温柔神秘，擅长演绎富有神秘感的女性角色。'
        ],
        'famous_works': [
            ['石纪元', 'Re:从零开始的异世界生活', '魔法科高中的劣等生'],
            ['石纪元', '一拳超人', '辉夜大小姐想让我告白'],
            ['石纪元', '卡罗尔与星期二', 'SSSS.GRIDMAN'],
            ['石纪元', '我的英雄学院', '粗点心战争'],
            ['石纪元', '咒术回战', '星合之空'],
            ['石纪元', 'DARLING in the FRANXX', '比宇宙更远的地方'],
            ['石纪元', '偶像大师', 'Wake Up, Girls!']
        ],
        'avg_rating': [9.4, 8.3, 8.6, 8.8, 8.5, 8.2, 8.0],
        'rating_count': [14200, 11800, 12500, 13500, 11200, 9800, 8600],
        'image_url': [
            'https://static.wikia.nocookie.net/dr-stone/images/9/93/Senku_Ishigami_%28Anime%29.png/revision/latest?cb=20190710154134',
            'https://static.wikia.nocookie.net/dr-stone/images/6/69/Taiju_Oki_%28Anime%29.png/revision/latest?cb=20190705185117',
            'https://static.wikia.nocookie.net/dr-stone/images/7/72/Yuzuriha_Ogawa_Full_Body_%28Anime%29.png/revision/latest?cb=20190719182512',
            'https://static.wikia.nocookie.net/dr-stone/images/5/50/Tsukasa_Shishio_%28Anime%29.png/revision/latest/scale-to-width-down/536?cb=20190712212715',
            'https://static.wikia.nocookie.net/dr-stone/images/3/3a/Chrome_Anime_Profile.png/revision/latest?cb=20190816201633',
            'https://static.wikia.nocookie.net/dr-stone/images/a/a2/Kohaku_Anime_Profile.png/revision/latest?cb=20190816215803',
            'https://static.wikia.nocookie.net/dr-stone/images/7/75/Ruri_Anime_Profile.png/revision/latest?cb=20190816221228'
        ],
        'actor_photo_url': [
            'https://via.placeholder.com/200x300/2196F3/FFFFFF?text=小林裕介',
            'https://via.placeholder.com/200x300/4CAF50/FFFFFF?text=古川慎',
            'https://via.placeholder.com/200x300/FF9800/FFFFFF?text=市之濑加那',
            'https://via.placeholder.com/200x300/F44336/FFFFFF?text=中村悠一',
            'https://via.placeholder.com/200x300/9C27B0/FFFFFF?text=佐藤元',
            'https://via.placeholder.com/200x300/607D8B/FFFFFF?text=上田丽奈',
            'https://via.placeholder.com/200x300/795548/FFFFFF?text=沼仓爱美'
        ]
    }
    return pd.DataFrame(characters_data)

# 代表作品图片映射
def get_work_images(work_name):
    work_images = {
        '石纪元': 'https://via.placeholder.com/200x300/2E7D32/FFFFFF?text=石纪元',
        'Re:从零开始的异世界生活': 'https://via.placeholder.com/200x300/2196F3/FFFFFF?text=Re:0',
        '魔法科高中的劣等生': 'https://via.placeholder.com/200x300/9C27B0/FFFFFF?text=魔科',
        '一拳超人': 'https://via.placeholder.com/200x300/FF9800/FFFFFF?text=一拳',
        '辉夜大小姐想让我告白': 'https://via.placeholder.com/200x300/E91E63/FFFFFF?text=辉夜',
        '卡罗尔与星期二': 'https://via.placeholder.com/200x300/00BCD4/FFFFFF?text=卡罗尔',
        'SSSS.GRIDMAN': 'https://via.placeholder.com/200x300/3F51B5/FFFFFF?text=GRIDMAN',
        '我的英雄学院': 'https://via.placeholder.com/200x300/FF5722/FFFFFF?text=我英',
        '粗点心战争': 'https://via.placeholder.com/200x300/8BC34A/FFFFFF?text=粗点心',
        '咒术回战': 'https://via.placeholder.com/200x300/673AB7/FFFFFF?text=咒术',
        '星合之空': 'https://via.placeholder.com/200x300/009688/FFFFFF?text=星合',
        'DARLING in the FRANXX': 'https://via.placeholder.com/200x300/E91E63/FFFFFF?text=DARLING',
        '比宇宙更远的地方': 'https://via.placeholder.com/200x300/00BCD4/FFFFFF?text=比宇宙',
        '偶像大师': 'https://via.placeholder.com/200x300/FF4081/FFFFFF?text=偶像大师',
        'Wake Up, Girls!': 'https://via.placeholder.com/200x300/3F51B5/FFFFFF?text=WUG'
    }
    return work_images.get(work_name, 'https://via.placeholder.com/200x300/666666/FFFFFF?text=默认作品')

# 角色相关的梗和热评
def get_character_memes(character_id):
    memes_dict = {
        1: ["100亿%", "复活全人类", "科学就是力量", "千空实验室"],
        2: ["体力担当", "千空最好的朋友", "肌肉笨蛋", "忠诚的伙伴"],
        3: ["技术部部长", "复活可乐", "工程专家", "可靠的大姐姐"],
        4: ["司帝国", "强者生存", "武力MAX", "理念冲突"],
        5: ["科学助手", "千空弟子", "好奇心旺盛", "学习能力强"],
        6: ["村落战士", "身手敏捷", "勇敢少女", "战斗专家"],
        7: ["预知能力", "石神村巫女", "神秘少女", "特殊能力者"]
    }
    
    comments_dict = {
        1: ["千空的科学知识太强了，从零重建文明看得热血沸腾", "100亿%的经典台词已经成为科学迷的信仰"],
        2: ["大树虽然科学不行，但这份友情和坚持太感人了", "体力担当在石器时代真的太重要了"],
        3: ["小川杠的技术能力是科学王国的重要支撑", "女性角色的科学能力展现得很出色"],
        4: ["司的理念虽然极端但很有深度，角色塑造很成功", "武力与科学的对决很有戏剧性"],
        5: ["克罗姆的学习热情让人感动，是千空的完美助手", "从科学小白到得力助手的成长很励志"],
        6: ["琥珀的战斗场面太帅了，女战士形象很立体", "在科学时代保持战士本色很有特色"],
        7: ["琉璃的预知能力为剧情增加了神秘色彩", "巫女与科学的结合很有创意"]
    }
    
    memes = memes_dict.get(character_id, [])
    comments = comments_dict.get(character_id, [])
    return memes[:3], comments[:2]

# 五星评分系统
def star_rating_component(character_id, current_rating=0):
    rating_options = ["未评分", "1星 ⭐", "2星 ⭐⭐", "3星 ⭐⭐⭐", "4星 ⭐⭐⭐⭐", "5星 ⭐⭐⭐⭐⭐"]
    
    rating_key = f"rating_{character_id}"
    
    if current_rating > 0:
        st.markdown(f'<div style="text-align: center; background: #4CAF50; color: white; padding: 8px; border-radius: 10px; margin: 10px 0;">您已评分: {current_rating}星</div>', unsafe_allow_html=True)
    
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
    st.markdown('<div class="main-header">🔬 石纪元角色评分</div>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">✨ 虎扑风格评分系统 · 科学主题 · 热评互动</p>', unsafe_allow_html=True)
    
    # 侧边栏 - 筛选器
    with st.sidebar:
        st.header("🔍 筛选设置")
        
        # 角色类型筛选
        roles = ['全部'] + list(st.session_state.characters_df['role'].unique())
        selected_role = st.selectbox("角色类型", roles)
        
        # 科学等级筛选
        science_levels = ['全部'] + list(st.session_state.characters_df['science_level'].unique())
        selected_science = st.selectbox("科学等级", science_levels)
        
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
        
        if selected_science != '全部':
            filtered_characters = filtered_characters[filtered_characters['science_level'] == selected_science]
        
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
        sort_by = st.selectbox("排序方式", ["综合评分", "评分人数", "角色名称", "科学等级"])
        
        if sort_by == "综合评分":
            ranked_characters = filtered_characters.sort_values('avg_rating', ascending=False)
        elif sort_by == "评分人数":
            ranked_characters = filtered_characters.sort_values('rating_count', ascending=False)
        elif sort_by == "科学等级":
            # 自定义科学等级排序
            science_order = {'超天才级': 0, '专家级': 1, '优秀级': 2, '特殊能力': 3, '普通级': 4}
            ranked_characters = filtered_characters.copy()
            ranked_characters['science_order'] = ranked_characters['science_level'].map(science_order)
            ranked_characters = ranked_characters.sort_values('science_order')
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
                    
                    # 科学等级徽章
                    st.markdown(f'<div class="science-badge" style="text-align: center; margin-top: 10px;">科学等级: {character["science_level"]}</div>', 
                               unsafe_allow_html=True)
                    
                    st.markdown(f'<div class="score-highlight" style="text-align: center; margin-top: 10px;">评分: {character["avg_rating"]}</div>', 
                               unsafe_allow_html=True)
                    st.markdown(f'<div style="text-align: center; font-size: 0.9rem; color: #666; margin-top: 5px;">👥 {character["rating_count"]}人评分</div>', 
                               unsafe_allow_html=True)
                
                with col_b:
                    st.markdown(f"<h2 style='font-size: 1.8rem; margin-bottom: 10px;'>{character['name']}</h2>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size: 1.2rem; font-weight: bold; color: #2E7D32; margin-bottom: 8px;'>身份: {character['role']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size: 1.1rem; line-height: 1.4; margin-bottom: 15px;'>{character['description']}</p>", unsafe_allow_html=True)
                    
                    # 科学能力描述
                    st.markdown(f"<p style='font-size: 1rem; color: #388E3C; margin-bottom: 15px;'><strong>科学能力:</strong> {character['science_description']}</p>", unsafe_allow_html=True)
                    
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
        
        # 科学等级分布
        st.subheader("🔬 科学等级分布")
        science_counts = filtered_characters['science_level'].value_counts()
        for level, count in science_counts.items():
            st.markdown(f"<div style='font-size: 1.2rem; margin-bottom: 10px;'>{level}: <strong>{count}</strong> 人</div>", unsafe_allow_html=True)
        
        # 排行榜
        st.subheader("🏆 角色排行榜")
        
        for i, (_, character) in enumerate(ranked_characters.head(5).iterrows(), 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            
            st.markdown(f"<div style='font-size: 1.2rem; margin-bottom: 10px;'>{medal} <strong>{character['name']}</strong></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 1.1rem; margin-bottom: 5px;'>  评分: <strong>{character['avg_rating']}</strong> 🌟</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 1.1rem; margin-bottom: 5px;'>  科学: {character['science_level']}</div>", unsafe_allow_html=True)
            
            # 显示用户评分
            user_score = st.session_state.character_ratings.get(character['id'])
            if user_score:
                st.markdown(f"<div style='font-size: 1.1rem; margin-bottom: 10px;'>  我的评分: <strong>{user_score}</strong> 🌟</div>", unsafe_allow_html=True)
            
            st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)

# AI角色分析界面
def ai_character_analysis():
    st.markdown("## 🔮 AI角色深度解析")
    st.markdown("### 💫 让AI帮你分析角色特点和科学能力")
    
    # 角色选择
    character_names = [char['name'] for _, char in st.session_state.characters_df.iterrows()]
    selected_character = st.selectbox("选择要分析的角色", character_names, key="ai_character")
    
    # 获取角色数据
    character_data = st.session_state.characters_df[st.session_state.characters_df['name'] == selected_character].iloc[0]
    actor_name = character_data['actor_name']
    famous_works = character_data['famous_works']
    
    # 分析维度选择
    analysis_type = st.selectbox("分析维度", 
                                ["角色性格分析", "科学能力分析", "剧情作用分析", "演技评价", "观众共鸣点", "角色成长轨迹", "演员简介", "代表作品分析"])
    
    if st.button("🔮 启动AI分析", type="primary", key="ai_analyze"):
        with st.spinner('AI正在深度解析角色...'):
            time.sleep(2)
            
            # 模拟AI分析结果
            analysis_results = {
                "角色性格分析": [
                    f"**{selected_character}**的性格在石纪元世界中独具特色，展现了在文明重建中的独特价值",
                    f"**MBTI性格类型**: **{character_data['mbti_type']}** - {character_data['mbti_description']}",
                    f"**性格特点**: {character_data['mbti_description'].split('：')[1]}",
                    f"在石化世界的极端环境下，{selected_character}的性格特点得到了充分展现",
                    f"角色的人际关系处理方式体现了其性格的核心特征",
                    f"面对文明重建的挑战，{selected_character}展现出了独特的应对策略",
                    f"性格中的优缺点在剧情发展中起到了关键作用",
                    f"与其他角色的互动展现了{selected_character}性格的多面性"
                ],
                "科学能力分析": [
                    f"**{selected_character}**的科学能力等级为: **{character_data['science_level']}**",
                    f"**能力描述**: {character_data['science_description']}",
                    f"在科学王国重建过程中，{selected_character}发挥了不可替代的作用",
                    f"科学知识的应用方式体现了角色的独特思维方式",
                    f"面对技术难题时，{selected_character}展现出了出色的解决问题的能力",
                    f"科学创新能力在文明重建中起到了关键作用",
                    f"知识传授和学习能力也是{selected_character}科学能力的重要组成部分"
                ],
                "剧情作用分析": [
                    f"**{selected_character}**在石纪元剧情中扮演着重要角色",
                    f"作为{character_data['role']}，在文明重建中发挥了独特作用",
                    f"与其他角色的互动推动了剧情的关键发展",
                    f"在科学vs武力的主题冲突中，{selected_character}代表了重要的价值立场",
                    f"角色的选择和行动往往成为剧情转折的关键",
                    f"成长轨迹与主线剧情发展高度契合",
                    f"在团队协作中展现了不可替代的价值"
                ],
                "演技评价": [
                    f"**{actor_name}**的配音表演为{selected_character}注入了灵魂",
                    "声线特点与角色性格高度契合，增强了角色的可信度",
                    "情感表达的层次感丰富，能够准确传达角色的内心世界",
                    "在关键场景中的表演张力十足，给观众留下深刻印象",
                    "台词处理自然流畅，语气变化恰到好处",
                    "能够通过声音展现角色的成长和变化",
                    "整体表演风格与石纪元的科幻冒险主题完美融合"
                ],
                "观众共鸣点": [
                    f"**{selected_character}**的角色设定引发了观众的强烈共鸣",
                    "在文明重建的宏大背景下，角色的个人成长让观众感同身受",
                    "面对困境时的坚持和勇气激励了许多观众",
                    "与其他角色的友情和羁绊让人感动",
                    "科学探索的精神引发了观众对知识的向往",
                    "角色的命运发展牵动着观众的心弦",
                    "在极端环境下的选择引发了观众的深度思考"
                ],
                "角色成长轨迹": [
                    f"**{selected_character}**在石纪元中经历了显著的成长",
                    "从石化苏醒到参与文明重建，角色不断突破自我",
                    "科学能力/战斗技能/领导能力等方面都有明显提升",
                    "价值观和世界观随着经历不断成熟和完善",
                    "与其他角色的关系发展也反映了角色的成长",
                    "面对挫折时的应对方式展现了角色的心理成长",
                    "最终的角色定位与初期形成了鲜明对比"
                ],
                "演员简介": [
                    f"**{actor_name}**是日本实力派声优，在《石纪元》中成功塑造了**{selected_character}**这一经典角色",
                    f"**{actor_name}**的表演风格独特，能够准确把握角色的核心特质",
                    f"通过**{selected_character}**这一角色，**{actor_name}**展现了出色的配音实力",
                    f"**演员简介**: {character_data['actor_bio']}",
                    f"**代表作品**: {', '.join(famous_works)}",
                    f"**配音特点**: 声线富有辨识度，表演细腻真实",
                    f"**角色塑造**: 能够深入理解角色内心，表演富有层次感"
                ],
                "代表作品分析": [
                    f"**{actor_name}**的代表作品包括：**{famous_works[0]}**、**{famous_works[1]}**、**{famous_works[2]}**",
                    f"在**{famous_works[0]}**中，**{actor_name}**展现了出色的配音实力和角色塑造能力",
                    f"**{famous_works[1]}**是**{actor_name}**的另一部重要作品，展现了其多样化的表演风格",
                    f"通过**{famous_works[2]}**，**{actor_name}**进一步巩固了在声优界的地位",
                    f"这些作品共同展现了**{actor_name}**宽广的戏路和扎实的配音功底",
                    f"在不同类型作品中的表现证明了**{actor_name}**的专业实力"
                ]
            }
            
            # 显示分析结果
            if analysis_type in ["演员简介", "代表作品分析"]:
                col_img, col_comments = st.columns([1, 2])
                
                with col_img:
                    st.image(character_data['actor_photo_url'], width=300, caption=f"声优: {actor_name}")
                
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