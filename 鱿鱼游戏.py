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
    page_title="🦑 鱿鱼游戏角色评分 - 虎扑风格",
    page_icon="🔺",
    layout="wide"
)

# 自定义CSS样式 - 生存游戏主题风格
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
    
    .main-header {
        font-family: 'Noto Sans SC', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(45deg, #FF6B6B, #FF8E8E, #FFAAAA, #FF6B6B);
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
        border-left: 4px solid #FF6B6B;
        transition: all 0.3s ease;
    }
    .character-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    .rating-section {
        background: linear-gradient(135deg, #FF8E8E 0%, #FF6B6B 100%);
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
        background-color: #FFD8D8;
        color: #D32F2F;
        padding: 0.4rem 1rem;
        margin: 0.3rem;
        border-radius: 15px;
        font-size: 1rem;
        font-weight: bold;
    }
    .hot-comment {
        background-color: #FFECEC;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid #FF6B6B;
        color: #D32F2F;
        font-weight: 500;
    }
    .score-badge {
        background-color: #FF8E8E;
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
        background: linear-gradient(135deg, #FF8E8E, #FF6B6B);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 1.2rem;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
        box-shadow: 0 4px 8px rgba(255, 142, 142, 0.3);
    }
    .stat-card {
        background: linear-gradient(135deg, #FF8E8E 0%, #FF6B6B 100%);
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
        border: 4px solid #FF6B6B;
        margin: 0 auto;
        display: block;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .actor-section {
        background: linear-gradient(135deg, #FFAAAA 0%, #FF8E8E 100%);
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
    .survival-badge {
        background: linear-gradient(135deg, #4A90E2, #357ABD);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
        display: inline-block;
        margin: 0.2rem;
    }
    .game-section {
        background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
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

# 鱿鱼游戏角色数据
def initialize_characters():
    characters_data = {
        'id': range(1, 9),
        'name': ['成奇勋', '曹尚佑', '姜晓', '阿里', '吴一男', '韩美女', '张德秀', '负责人'],
        'role': ['主角/456号', '首尔大学高材生', '脱北者', '巴基斯坦劳工', '001号老人', '蛇蝎美人', '黑道老大', '游戏负责人'],
        'description': [
            '失业的汽车工人，为见女儿参加游戏',
            '成奇勋的儿时好友，精英阶层代表',
            '为寻找母亲而参加游戏的脱北者',
            '为养家糊口参加游戏的善良劳工',
            '游戏的最年长参与者，神秘老人',
            '善于利用美色的精明参与者',
            '暴力组织头目，游戏中的恶霸',
            '戴面具的游戏组织者'
        ],
        'survival_level': ['幸存者', '淘汰', '淘汰', '淘汰', '淘汰', '淘汰', '淘汰', '工作人员'],
        'survival_description': [
            '最终获胜者，在残酷游戏中保持人性',
            '聪明但自私，在最后一关选择自杀',
            '勇敢坚韧，在玻璃桥游戏中牺牲',
            '善良单纯，在弹珠游戏中被骗淘汰',
            '游戏设计者之一，因病主动退出',
            '在拔河游戏后与张德秀同归于尽',
            '暴力残忍，在玻璃桥游戏前被淘汰',
            '游戏组织者，维持游戏秩序'
        ],
        'mbti_type': ['ISFP', 'ENTJ', 'ISTP', 'ESFJ', 'INFJ', 'ESTP', 'ESTJ', 'INTJ'],
        'mbti_description': [
            'ISFP（探险家型）：善良敏感，重视情感，活在当下',
            'ENTJ（指挥官型）：聪明果断，目标导向，理性冷静',
            'ISTP（鉴赏家型）：独立坚强，行动派，生存能力强',
            'ESFJ（执政官型）：善良忠诚，重视家庭，乐于助人',
            'INFJ（提倡者型）：智慧深沉，富有洞察力，理想主义',
            'ESTP（企业家型）：大胆冒险，善于交际，机会主义者',
            'ESTJ（总经理型）：强势果断，重视规则，领导型',
            'INTJ（建筑师型）：理性冷酷，逻辑思维强，掌控欲强'
        ],
        'actor_name': ['李政宰', '朴海秀', '郑浩妍', '阿努帕姆·特里帕蒂', '吴永洙', '金周玲', '许成泰', '李炳宪'],
        'actor_bio': [
            '韩国国宝级演员，演技细腻真实，能够深刻演绎复杂角色',
            '韩国实力派演员，擅长演绎精英角色，表演富有层次感',
            '韩国新生代演员兼模特，首次演戏就展现出色演技',
            '印度籍演员，在韩国发展成功，演技自然生动',
            '韩国资深演员，戏骨级表演，能够驾驭各种角色类型',
            '韩国实力派女演员，擅长演绎性格复杂的女性角色',
            '韩国资深演员，多才多艺，演技扎实',
            '韩国顶级演员，能够完美演绎神秘复杂的角色'
        ],
        'famous_works': [
            ['鱿鱼游戏', '新世界', '暗杀'],
            ['鱿鱼游戏', '机智的医生生活', '狩猎'],
            ['鱿鱼游戏', '我的名字'],
            ['鱿鱼游戏', '请回答1988', 'Voice'],
            ['鱿鱼游戏', '六龙飞天', '树袋熊'],
            ['鱿鱼游戏', '王国', '黑钱胜地'],
            ['鱿鱼游戏', '犯罪都市', '魔女'],
            ['鱿鱼游戏', 'IRIS', '看见恶魔']
        ],
        'avg_rating': [9.1, 8.9, 9.3, 8.7, 8.8, 8.5, 8.4, 8.6],
        'rating_count': [18200, 16800, 17500, 15200, 15800, 14200, 13800, 14500],
        'image_url': [
            'https://via.placeholder.com/200x300/FF6B6B/FFFFFF?text=成奇勋',
            'https://via.placeholder.com/200x300/FF8E8E/FFFFFF?text=曹尚佑',
            'https://via.placeholder.com/200x300/FFAAAA/FFFFFF?text=姜晓',
            'https://via.placeholder.com/200x300/4A90E2/FFFFFF?text=阿里',
            'https://via.placeholder.com/200x300/357ABD/FFFFFF?text=吴一男',
            'https://via.placeholder.com/200x300/E91E63/FFFFFF?text=韩美女',
            'https://via.placeholder.com/200x300/795548/FFFFFF?text=张德秀',
            'https://via.placeholder.com/200x300/607D8B/FFFFFF?text=负责人'
        ],
        'actor_photo_url': [
            'https://via.placeholder.com/200x300/2196F3/FFFFFF?text=李政宰',
            'https://via.placeholder.com/200x300/4CAF50/FFFFFF?text=朴海秀',
            'https://via.placeholder.com/200x300/FF9800/FFFFFF?text=郑浩妍',
            'https://via.placeholder.com/200x300/F44336/FFFFFF?text=阿努帕姆',
            'https://via.placeholder.com/200x300/9C27B0/FFFFFF?text=吴永洙',
            'https://via.placeholder.com/200x300/607D8B/FFFFFF?text=金周玲',
            'https://via.placeholder.com/200x300/795548/FFFFFF?text=许成泰',
            'https://via.placeholder.com/200x300/009688/FFFFFF?text=李炳宪'
        ]
    }
    return pd.DataFrame(characters_data)

# 代表作品图片映射
def get_work_images(work_name):
    work_images = {
        '鱿鱼游戏': 'https://via.placeholder.com/200x300/FF6B6B/FFFFFF?text=鱿鱼游戏',
        '新世界': 'https://via.placeholder.com/200x300/2196F3/FFFFFF?text=新世界',
        '暗杀': 'https://via.placeholder.com/200x300/9C27B0/FFFFFF?text=暗杀',
        '机智的医生生活': 'https://via.placeholder.com/200x300/FF9800/FFFFFF?text=机医',
        '狩猎': 'https://via.placeholder.com/200x300/E91E63/FFFFFF?text=狩猎',
        '我的名字': 'https://via.placeholder.com/200x300/00BCD4/FFFFFF?text=我的名字',
        '请回答1988': 'https://via.placeholder.com/200x300/3F51B5/FFFFFF?text=1988',
        'Voice': 'https://via.placeholder.com/200x300/FF5722/FFFFFF?text=Voice',
        '六龙飞天': 'https://via.placeholder.com/200x300/8BC34A/FFFFFF?text=六龙',
        '树袋熊': 'https://via.placeholder.com/200x300/673AB7/FFFFFF?text=树袋熊',
        '王国': 'https://via.placeholder.com/200x300/009688/FFFFFF?text=王国',
        '黑钱胜地': 'https://via.placeholder.com/200x300/E91E63/FFFFFF?text=黑钱',
        '犯罪都市': 'https://via.placeholder.com/200x300/00BCD4/FFFFFF?text=犯罪都市',
        '魔女': 'https://via.placeholder.com/200x300/3F51B5/FFFFFF?text=魔女',
        'IRIS': 'https://via.placeholder.com/200x300/FF4081/FFFFFF?text=IRIS',
        '看见恶魔': 'https://via.placeholder.com/200x300/3F51B5/FFFFFF?text=看见恶魔'
    }
    return work_images.get(work_name, 'https://via.placeholder.com/200x300/666666/FFFFFF?text=默认作品')

# 角色相关的梗和热评
def get_character_memes(character_id):
    memes_dict = {
        1: ["456号", "木槿花开了", "最终获胜者", "人性之光"],
        2: ["首尔大学", "儿时好友", "精英的堕落", "最后一枪"],
        3: ["脱北者", "姜晓的刀", "玻璃桥牺牲", "坚韧少女"],
        4: ["阿里", "善良的阿里", "弹珠游戏", "被欺骗的心"],
        5: ["001号", "吴一男爷爷", "游戏设计者", "最后的夜晚"],
        6: ["韩美女", "蛇蝎美人", "同归于尽", "拔河游戏"],
        7: ["张德秀", "黑道老大", "暴力恶霸", "团队背叛"],
        8: ["负责人", "面具之下", "游戏组织", "李炳宪"]
    }
    
    comments_dict = {
        1: ["成奇勋的善良在残酷游戏中显得格外珍贵，最终获胜实至名归", "李政宰的演技太棒了，把小人物的挣扎和善良演绎得淋漓尽致"],
        2: ["曹尚佑这个角色太复杂了，聪明但自私，最后的自杀让人唏嘘", "朴海秀把精英的堕落演得太真实了，演技炸裂"],
        3: ["姜晓的坚韧和勇敢让人敬佩，她的牺牲是剧中最痛的一幕", "郑浩妍作为新人演员表现惊艳，未来可期"],
        4: ["阿里的善良单纯让人心疼，弹珠游戏那段看哭了", "阿努帕姆的表演真挚动人，把移民工人的艰辛演活了"],
        5: ["吴一男爷爷的反转太震撼了，原来他才是游戏的幕后之一", "吴永洙的演技老辣，把神秘老人的复杂性完美呈现"],
        6: ["韩美女这个角色虽然戏份不多但令人印象深刻，最后的复仇太解气了", "金周玲把蛇蝎美人演得入木三分"],
        7: ["张德秀是典型的恶霸角色，但演员演出了人物的多面性", "许成泰的表演很有张力，把黑道老大的凶狠演活了"],
        8: ["负责人的神秘感和压迫感太强了，面具下的李炳宪演技爆表", "这个角色虽然戏份少但存在感极强，不愧是顶级演员"]
    }
    
    memes = memes_dict.get(character_id, [])
    comments = comments_dict.get(character_id, [])
    return memes[:3], comments[:2]

# 五星评分系统
def star_rating_component(character_id, current_rating=0):
    rating_options = ["未评分", "1星 ⭐", "2星 ⭐⭐", "3星 ⭐⭐⭐", "4星 ⭐⭐⭐⭐", "5星 ⭐⭐⭐⭐⭐"]
    
    rating_key = f"rating_{character_id}"
    
    if current_rating > 0:
        st.markdown(f'<div style="text-align: center; background: #FF8E8E; color: white; padding: 8px; border-radius: 10px; margin: 10px 0;">您已评分: {current_rating}星</div>', unsafe_allow_html=True)
    
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
    st.markdown('<div class="main-header">🦑 鱿鱼游戏角色评分</div>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">✨ 虎扑风格评分系统 · 生存游戏主题 · 热评互动</p>', unsafe_allow_html=True)
    
    # 侧边栏 - 筛选器
    with st.sidebar:
        st.header("🔍 筛选设置")
        
        # 角色类型筛选
        roles = ['全部'] + list(st.session_state.characters_df['role'].unique())
        selected_role = st.selectbox("角色类型", roles)
        
        # 生存状态筛选
        survival_levels = ['全部'] + list(st.session_state.characters_df['survival_level'].unique())
        selected_survival = st.selectbox("生存状态", survival_levels)
        
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
        
        if selected_survival != '全部':
            filtered_characters = filtered_characters[filtered_characters['survival_level'] == selected_survival]
        
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
        sort_by = st.selectbox("排序方式", ["综合评分", "评分人数", "角色名称", "生存状态"])
        
        if sort_by == "综合评分":
            ranked_characters = filtered_characters.sort_values('avg_rating', ascending=False)
        elif sort_by == "评分人数":
            ranked_characters = filtered_characters.sort_values('rating_count', ascending=False)
        elif sort_by == "生存状态":
            # 自定义生存状态排序
            survival_order = {'工作人员': 0, '幸存者': 1, '淘汰': 2}
            ranked_characters = filtered_characters.copy()
            ranked_characters['survival_order'] = ranked_characters['survival_level'].map(survival_order)
            ranked_characters = ranked_characters.sort_values('survival_order')
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
                    
                    # 生存状态徽章
                    st.markdown(f'<div class="survival-badge" style="text-align: center; margin-top: 10px;">生存状态: {character["survival_level"]}</div>', 
                               unsafe_allow_html=True)
                    
                    st.markdown(f'<div class="score-highlight" style="text-align: center; margin-top: 10px;">评分: {character["avg_rating"]}</div>', 
                               unsafe_allow_html=True)
                    st.markdown(f'<div style="text-align: center; font-size: 0.9rem; color: #666; margin-top: 5px;">👥 {character["rating_count"]}人评分</div>', 
                               unsafe_allow_html=True)
                
                with col_b:
                    st.markdown(f"<h2 style='font-size: 1.8rem; margin-bottom: 10px;'>{character['name']}</h2>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size: 1.2rem; font-weight: bold; color: #FF6B6B; margin-bottom: 8px;'>身份: {character['role']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size: 1.1rem; line-height: 1.4; margin-bottom: 15px;'>{character['description']}</p>", unsafe_allow_html=True)
                    
                    # 生存描述
                    st.markdown(f"<p style='font-size: 1rem; color: #FF8E8E; margin-bottom: 15px;'><strong>生存分析:</strong> {character['survival_description']}</p>", unsafe_allow_html=True)
                    
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
        
        # 生存状态分布
        st.subheader("🔺 生存状态分布")
        survival_counts = filtered_characters['survival_level'].value_counts()
        for level, count in survival_counts.items():
            st.markdown(f"<div style='font-size: 1.2rem; margin-bottom: 10px;'>{level}: <strong>{count}</strong> 人</div>", unsafe_allow_html=True)
        
        # 排行榜
        st.subheader("🏆 角色排行榜")
        
        for i, (_, character) in enumerate(ranked_characters.head(5).iterrows(), 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            
            st.markdown(f"<div style='font-size: 1.2rem; margin-bottom: 10px;'>{medal} <strong>{character['name']}</strong></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 1.1rem; margin-bottom: 5px;'>  评分: <strong>{character['avg_rating']}</strong> 🌟</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 1.1rem; margin-bottom: 5px;'>  生存: {character['survival_level']}</div>", unsafe_allow_html=True)
            
            # 显示用户评分
            user_score = st.session_state.character_ratings.get(character['id'])
            if user_score:
                st.markdown(f"<div style='font-size: 1.1rem; margin-bottom: 10px;'>  我的评分: <strong>{user_score}</strong> 🌟</div>", unsafe_allow_html=True)
            
            st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)

# AI角色分析界面
def ai_character_analysis():
    st.markdown("## 🔮 AI角色深度解析")
    st.markdown("### 💫 让AI帮你分析角色特点和生存策略")
    
    # 角色选择
    character_names = [char['name'] for _, char in st.session_state.characters_df.iterrows()]
    selected_character = st.selectbox("选择要分析的角色", character_names, key="ai_character")
    
    # 获取角色数据
    character_data = st.session_state.characters_df[st.session_state.characters_df['name'] == selected_character].iloc[0]
    actor_name = character_data['actor_name']
    famous_works = character_data['famous_works']
    
    # 分析维度选择
    analysis_type = st.selectbox("分析维度", 
                                ["角色性格分析", "生存策略分析", "剧情作用分析", "演技评价", "观众共鸣点", "角色成长轨迹", "演员简介", "代表作品分析"])
    
    if st.button("🔮 启动AI分析", type="primary", key="ai_analyze"):
        with st.spinner('AI正在深度解析角色...'):
            time.sleep(2)
            
            # 模拟AI分析结果
            analysis_results = {
                "角色性格分析": [
                    f"**{selected_character}**的性格在《鱿鱼游戏》中极具特色，展现了在生存游戏中的独特表现",
                    f"**MBTI性格类型**: **{character_data['mbti_type']}** - {character_data['mbti_description']}",
                    f"**性格特点**: {character_data['mbti_description'].split('：')[1]}",
                    f"在生死存亡的极端环境下，{selected_character}的性格特点得到了充分展现",
                    f"角色的人际关系处理方式体现了其性格的核心特征",
                    f"面对死亡威胁，{selected_character}展现出了独特的应对策略",
                    f"性格中的优缺点在生存游戏中起到了关键作用",
                    f"与其他角色的互动展现了{selected_character}性格的多面性"
                ],
                "生存策略分析": [
                    f"**{selected_character}**的生存状态为: **{character_data['survival_level']}**",
                    f"**生存分析**: {character_data['survival_description']}",
                    f"在鱿鱼游戏中，{selected_character}的生存策略值得深入分析",
                    f"角色的游戏表现和决策过程反映了其生存智慧",
                    f"面对不同游戏挑战时，{selected_character}展现出了独特的应对方式",
                    f"与其他角色的合作与竞争也是生存策略的重要组成部分",
                    f"角色的心理承受能力和适应能力是生存关键"
                ],
                "剧情作用分析": [
                    f"**{selected_character}**在《鱿鱼游戏》剧情中扮演着重要角色",
                    f"作为{character_data['role']}，在生存游戏中发挥了独特作用",
                    f"与其他角色的互动推动了剧情的关键发展",
                    f"在人性考验过程中，{selected_character}代表了重要的价值立场",
                    f"角色的选择和行动往往成为剧情转折的关键",
                    f"成长轨迹与主线剧情发展高度契合",
                    f"在生存游戏中展现了不可替代的戏剧价值"
                ],
                "演技评价": [
                    f"**{actor_name}**的表演为{selected_character}注入了灵魂",
                    "表演特点与角色性格高度契合，增强了角色的可信度",
                    "情感表达的层次感丰富，能够准确传达角色的内心世界",
                    "在关键场景中的表演张力十足，给观众留下深刻印象",
                    "台词处理自然流畅，语气变化恰到好处",
                    "能够通过表演展现角色的成长和变化",
                    "整体表演风格与《鱿鱼游戏》的生存主题完美融合"
                ],
                "观众共鸣点": [
                    f"**{selected_character}**的角色设定引发了观众的强烈共鸣",
                    "在生存游戏的残酷背景下，角色的个人挣扎让观众感同身受",
                    "面对生死考验时的恐惧和勇气让观众揪心",
                    "与其他角色的友情和羁绊让人感动",
                    "在极端环境下的选择引发了观众的深度思考",
                    "角色的命运发展牵动着观众的心弦",
                    "人性光辉在黑暗环境中的闪耀让人动容"
                ],
                "角色成长轨迹": [
                    f"**{selected_character}**在《鱿鱼游戏》中经历了显著的成长",
                    "从普通参与者到生存战士，角色不断突破自我",
                    "心理承受能力/生存智慧/人性认知等方面都有明显提升",
                    "价值观和世界观随着残酷经历不断成熟和完善",
                    "与其他角色的关系发展也反映了角色的成长",
                    "面对死亡威胁时的应对方式展现了角色的心理成长",
                    "最终的角色定位与初期形成了鲜明对比"
                ],
                "演员简介": [
                    f"**{actor_name}**是韩国实力派演员，在《鱿鱼游戏》中成功塑造了**{selected_character}**这一经典角色",
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