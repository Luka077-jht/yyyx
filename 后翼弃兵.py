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
    page_icon="👑",
    layout="wide"
)

# 自定义CSS样式 - 国际象棋主题风格
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
    
    .main-header {
        font-family: 'Noto Sans SC', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(45deg, #8B4513, #A0522D, #CD853F, #8B4513);
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
        border-left: 4px solid #8B4513;
        transition: all 0.3s ease;
    }
    .character-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    .rating-section {
        background: linear-gradient(135deg, #A0522D 0%, #8B4513 100%);
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
        background-color: #F5DEB3;
        color: #8B4513;
        padding: 0.4rem 1rem;
        margin: 0.3rem;
        border-radius: 15px;
        font-size: 1rem;
        font-weight: bold;
    }
    .hot-comment {
        background-color: #FFF8DC;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid #8B4513;
        color: #8B4513;
        font-weight: 500;
    }
    .score-badge {
        background-color: #A0522D;
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
        background: linear-gradient(135deg, #A0522D, #8B4513);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 1.2rem;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
        box-shadow: 0 4px 8px rgba(160, 82, 45, 0.3);
    }
    .stat-card {
        background: linear-gradient(135deg, #A0522D 0%, #8B4513 100%);
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
        border: 4px solid #8B4513;
        margin: 0 auto;
        display: block;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .actor-section {
        background: linear-gradient(135deg, #CD853F 0%, #A0522D 100%);
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
    .chess-badge {
        background: linear-gradient(135deg, #2F4F4F, #708090);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
        display: inline-block;
        margin: 0.2rem;
    }
    .chess-section {
        background: linear-gradient(135deg, #2F4F4F 0%, #708090 100%);
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

# 后翼弃兵角色数据
def initialize_characters():
    characters_data = {
        'id': range(1, 9),
        'name': ['贝丝·哈蒙', '本尼·瓦茨', '阿尔玛·惠特利', '乔琳', '哈里·贝尔蒂克', '汤斯', '博尔戈夫', '卢申科'],
        'role': ['天才棋手', '街头棋王', '养母', '孤儿院好友', '肯塔基州冠军', '记者男友', '苏联冠军', '世界冠军'],
        'description': [
            '孤儿院长大的国际象棋天才，在男性主导的棋坛闯出一片天',
            '纽约顶尖棋手，贝丝的导师和竞争对手',
            '贝丝的养母，支持她的象棋事业',
            '贝丝在孤儿院的好友，一直支持着她',
            '贝丝早期遇到的强大对手，后来成为朋友',
            '《肯塔基人报》记者，贝丝的男友',
            '苏联顶尖棋手，冷静理性的对手',
            '苏联世界冠军，贝丝的终极对手'
        ],
        'chess_level': ['天才级', '大师级', '初学者', '爱好者', '专家级', '爱好者', '大师级', '世界级'],
        'chess_description': [
            '拥有超凡的象棋天赋，能在脑海中模拟棋局，风格激进而富有创意',
            '街头象棋高手，风格务实，擅长快速对局',
            '对象棋了解有限，但全力支持贝丝的象棋事业',
            '了解象棋但不下棋，是贝丝的情感支持',
            '实力强劲的地区冠军，风格传统但有效',
            '象棋爱好者，欣赏贝丝的才华',
            '苏联顶尖棋手，风格严谨理性，计算精确',
            '世界冠军，经验丰富，风格全面无懈可击'
        ],
        'mbti_type': ['INTJ', 'ENTP', 'ESFJ', 'ISFJ', 'ISTJ', 'ENFJ', 'ISTJ', 'INTJ'],
        'mbti_description': [
            'INTJ（建筑师型）：战略思维强，独立自主，目标明确',
            'ENTP（辩论家型）：聪明机智，善于创新，喜欢挑战',
            'ESFJ（执政官型）：温暖关怀，重视家庭，支持他人',
            'ISFJ（守护者型）：忠诚体贴，默默支持，重视友情',
            'ISTJ（物流师型）：务实可靠，遵守传统，执行力强',
            'ENFJ（主人公型）：富有魅力，善于沟通，支持伴侣',
            'ISTJ（物流师型）：严谨理性，遵守规则，专业专注',
            'INTJ（建筑师型）：战略大师，冷静理性，经验丰富'
        ],
        'actor_name': ['安雅·泰勒-乔伊', '托马斯·布罗迪-桑斯特', '玛丽埃尔·海勒', '摩西·英格拉姆', '哈里·梅林', '雅各布·福琼·劳埃德', '马尔辛·多罗辛斯基', '谢尔盖·波卢宁'],
        'actor_bio': [
            '新生代实力派女演员，演技细腻，能够深刻演绎复杂角色',
            '英国实力派演员，演技自然，角色塑造力强',
            '美国资深女演员，演技精湛，能够演绎细腻情感',
            '美国新生代演员，表演真挚自然，富有感染力',
            '英国演员，演技扎实，能够驾驭各种角色类型',
            '英国年轻演员，表演生动，角色形象鲜明',
            '波兰演员，演技沉稳，能够演绎深沉复杂的角色',
            '乌克兰演员兼舞者，能够完美演绎冷静理性的棋手'
        ],
        'famous_works': [
            ['后翼弃兵', '女巫', '爱玛'],
            ['后翼弃兵', '权力的游戏', '魔法保姆麦克菲'],
            ['后翼弃兵', '你能原谅我吗', '戏剧训练班'],
            ['后翼弃兵', '皇后赌局', '大学新生'],
            ['后翼弃兵', '王冠', '雀起乡到烛镇'],
            ['后翼弃兵', '黑暗物质', '神秘博士'],
            ['后翼弃兵', '冷战', '修女艾达'],
            ['后翼弃兵', '胡桃夹子', '舞者']
        ],
        'avg_rating': [9.6, 8.9, 8.7, 8.5, 8.4, 8.3, 8.6, 8.8],
        'rating_count': [18500, 16200, 14800, 13500, 12800, 12200, 14200, 15500],
        'image_url': [
            '贝丝·哈蒙.png',
            '本尼·瓦茨.webp',
            '阿尔玛·惠特利.webp',
            '乔琳.webp',
            '哈里·贝尔蒂克.webp',
            '汤斯.webp',
            '博尔戈夫.webp',
            '卢申科.webp'
        ],
        'actor_photo_url': [
           '贝丝·哈蒙.png',
            '本尼·瓦茨.webp',
            '阿尔玛·惠特利.webp',
            '乔琳.webp',
            '哈里·贝尔蒂克.webp',
            '汤斯.webp',
            '博尔戈夫.webp',
            '卢申科.webp'
        ]
    }
    return pd.DataFrame(characters_data)

# 代表作品图片映射
def get_work_images(work_name):
    work_images = {
        '后翼弃兵': 'https://via.placeholder.com/200x300/8B4513/FFFFFF?text=后翼弃兵',
        '女巫': 'https://via.placeholder.com/200x300/2196F3/FFFFFF?text=女巫',
        '爱玛': 'https://via.placeholder.com/200x300/9C27B0/FFFFFF?text=爱玛',
        '权力的游戏': 'https://via.placeholder.com/200x300/FF9800/FFFFFF?text=权游',
        '魔法保姆麦克菲': 'https://via.placeholder.com/200x300/E91E63/FFFFFF?text=保姆',
        '你能原谅我吗': 'https://via.placeholder.com/200x300/00BCD4/FFFFFF?text=原谅我',
        '戏剧训练班': 'https://via.placeholder.com/200x300/3F51B5/FFFFFF?text=戏剧班',
        '皇后赌局': 'https://via.placeholder.com/200x300/FF5722/FFFFFF?text=皇后赌局',
        '大学新生': 'https://via.placeholder.com/200x300/8BC34A/FFFFFF?text=大学新生',
        '王冠': 'https://via.placeholder.com/200x300/673AB7/FFFFFF?text=王冠',
        '雀起乡到烛镇': 'https://via.placeholder.com/200x300/009688/FFFFFF?text=雀起乡',
        '黑暗物质': 'https://via.placeholder.com/200x300/E91E63/FFFFFF?text=黑暗物质',
        '神秘博士': 'https://via.placeholder.com/200x300/00BCD4/FFFFFF?text=神秘博士',
        '冷战': 'https://via.placeholder.com/200x300/3F51B5/FFFFFF?text=冷战',
        '修女艾达': 'https://via.placeholder.com/200x300/FF4081/FFFFFF?text=修女艾达',
        '胡桃夹子': 'https://via.placeholder.com/200x300/3F51B5/FFFFFF?text=胡桃夹子',
        '舞者': 'https://via.placeholder.com/200x300/009688/FFFFFF?text=舞者'
    }
    return work_images.get(work_name, 'https://via.placeholder.com/200x300/666666/FFFFFF?text=默认作品')

# 角色相关的梗和热评
def get_character_memes(character_id):
    memes_dict = {
        1: ["天才少女", "绿色药丸", "天花板棋局", "国际象棋女王"],
        2: ["街头棋王", "贝丝导师", "快速对局", "纽约风格"],
        3: ["养母", "支持者", "经纪人", "酗酒问题"],
        4: ["孤儿院好友", "黑人女孩", "情感支持", "永远的朋友"],
        5: ["肯塔基冠军", "早期对手", "后来朋友", "传统棋风"],
        6: ["记者男友", "象棋爱好者", "感情支持", "理解贝丝"],
        7: ["苏联冠军", "冷静理性", "强大对手", "计算精确"],
        8: ["世界冠军", "终极对手", "经验丰富", "无懈可击"]
    }
    
    comments_dict = {
        1: ["贝丝的象棋天赋太惊人了，在男性主导的领域闯出一片天", "安雅的演技太棒了，把天才的孤独和挣扎演绎得淋漓尽致"],
        2: ["本尼这个角色太有魅力了，既是导师又是竞争对手", "托马斯的表演很自然，把街头棋王的随性和才华都演活了"],
        3: ["阿尔玛对贝丝的支持太感人了，虽然不是亲生母亲但胜似母亲", "玛丽埃尔的演技细腻，把复杂的情感关系演绎得很好"],
        4: ["乔琳和贝丝的友情是剧中的温暖亮点，跨越种族和阶层的真挚友谊", "摩西的表演真挚动人，为剧集增添了很多温情"],
        5: ["哈里的角色展现了贝丝成长过程中的重要阶段，从对手到朋友", "哈里的演技扎实，把传统棋手的风范演绎得很好"],
        6: ["汤斯对贝丝的理解和支持很难得，在天才身边不容易", "雅各布的表演生动，把记者的敏锐和男友的温柔结合得很好"],
        7: ["博尔戈夫是贝丝遇到的最强对手之一，苏联棋手的严谨让人印象深刻", "马尔辛的表演沉稳，把冷静理性的棋手形象塑造得很成功"],
        8: ["卢申科作为终极对手，展现了世界冠军的风范和气度", "谢尔盖的表演很有分量，把经验丰富的老将形象演绎得很到位"]
    }
    
    memes = memes_dict.get(character_id, [])
    comments = comments_dict.get(character_id, [])
    return memes[:3], comments[:2]

# 五星评分系统
def star_rating_component(character_id, current_rating=0):
    rating_options = ["未评分", "1星 ⭐", "2星 ⭐⭐", "3星 ⭐⭐⭐", "4星 ⭐⭐⭐⭐", "5星 ⭐⭐⭐⭐⭐"]
    
    rating_key = f"rating_{character_id}"
    
    if current_rating > 0:
        st.markdown(f'<div style="text-align: center; background: #A0522D; color: white; padding: 8px; border-radius: 10px; margin: 10px 0;">您已评分: {current_rating}星</div>', unsafe_allow_html=True)
    
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
    st.markdown('<div class="main-header">♟️ 后翼弃兵角色评分</div>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">✨ 虎扑风格评分系统 · 国际象棋主题 · 热评互动</p>', unsafe_allow_html=True)
    
    # 侧边栏 - 筛选器
    with st.sidebar:
        st.header("🔍 筛选设置")
        
        # 角色类型筛选
        roles = ['全部'] + list(st.session_state.characters_df['role'].unique())
        selected_role = st.selectbox("角色类型", roles)
        
        # 棋艺等级筛选
        chess_levels = ['全部'] + list(st.session_state.characters_df['chess_level'].unique())
        selected_chess = st.selectbox("棋艺等级", chess_levels)
        
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
        
        if selected_chess != '全部':
            filtered_characters = filtered_characters[filtered_characters['chess_level'] == selected_chess]
        
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
        sort_by = st.selectbox("排序方式", ["综合评分", "评分人数", "角色名称", "棋艺等级"])
        
        if sort_by == "综合评分":
            ranked_characters = filtered_characters.sort_values('avg_rating', ascending=False)
        elif sort_by == "评分人数":
            ranked_characters = filtered_characters.sort_values('rating_count', ascending=False)
        elif sort_by == "棋艺等级":
            # 自定义棋艺等级排序
            chess_order = {'世界级': 0, '天才级': 1, '大师级': 2, '专家级': 3, '爱好者': 4, '初学者': 5}
            ranked_characters = filtered_characters.copy()
            ranked_characters['chess_order'] = ranked_characters['chess_level'].map(chess_order)
            ranked_characters = ranked_characters.sort_values('chess_order')
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
                    
                    # 棋艺等级徽章
                    st.markdown(f'<div class="chess-badge" style="text-align: center; margin-top: 10px;">棋艺等级: {character["chess_level"]}</div>', 
                               unsafe_allow_html=True)
                    
                    st.markdown(f'<div class="score-highlight" style="text-align: center; margin-top: 10px;">评分: {character["avg_rating"]}</div>', 
                               unsafe_allow_html=True)
                    st.markdown(f'<div style="text-align: center; font-size: 0.9rem; color: #666; margin-top: 5px;">👥 {character["rating_count"]}人评分</div>', 
                               unsafe_allow_html=True)
                
                with col_b:
                    st.markdown(f"<h2 style='font-size: 1.8rem; margin-bottom: 10px;'>{character['name']}</h2>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size: 1.2rem; font-weight: bold; color: #8B4513; margin-bottom: 8px;'>身份: {character['role']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size: 1.1rem; line-height: 1.4; margin-bottom: 15px;'>{character['description']}</p>", unsafe_allow_html=True)
                    
                    # 棋艺描述
                    st.markdown(f"<p style='font-size: 1rem; color: #A0522D; margin-bottom: 15px;'><strong>棋艺分析:</strong> {character['chess_description']}</p>", unsafe_allow_html=True)
                    
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
        
        # 棋艺等级分布
        st.subheader("♟️ 棋艺等级分布")
        chess_counts = filtered_characters['chess_level'].value_counts()
        for level, count in chess_counts.items():
            st.markdown(f"<div style='font-size: 1.2rem; margin-bottom: 10px;'>{level}: <strong>{count}</strong> 人</div>", unsafe_allow_html=True)
        
        # 排行榜
        st.subheader("🏆 角色排行榜")
        
        for i, (_, character) in enumerate(ranked_characters.head(5).iterrows(), 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            
            st.markdown(f"<div style='font-size: 1.2rem; margin-bottom: 10px;'>{medal} <strong>{character['name']}</strong></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 1.1rem; margin-bottom: 5px;'>  评分: <strong>{character['avg_rating']}</strong> 🌟</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 1.1rem; margin-bottom: 5px;'>  棋艺: {character['chess_level']}</div>", unsafe_allow_html=True)
            
            # 显示用户评分
            user_score = st.session_state.character_ratings.get(character['id'])
            if user_score:
                st.markdown(f"<div style='font-size: 1.1rem; margin-bottom: 10px;'>  我的评分: <strong>{user_score}</strong> 🌟</div>", unsafe_allow_html=True)
            
            st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)

# AI角色分析界面
def ai_character_analysis():
    st.markdown("## 🔮 AI角色深度解析")
    st.markdown("### 💫 让AI帮你分析角色特点和棋艺风格")
    
    # 角色选择
    character_names = [char['name'] for _, char in st.session_state.characters_df.iterrows()]
    selected_character = st.selectbox("选择要分析的角色", character_names, key="ai_character")
    
    # 获取角色数据
    character_data = st.session_state.characters_df[st.session_state.characters_df['name'] == selected_character].iloc[0]
    actor_name = character_data['actor_name']
    famous_works = character_data['famous_works']
    
    # 分析维度选择
    analysis_type = st.selectbox("分析维度", 
                                ["角色性格分析", "棋艺分析", "剧情作用分析", "演技评价", "观众共鸣点", "角色成长轨迹", "演员简介", "代表作品分析"])
    
    if st.button("🔮 启动AI分析", type="primary", key="ai_analyze"):
        with st.spinner('AI正在深度解析角色...'):
            time.sleep(2)
            
            # 模拟AI分析结果
            analysis_results = {
                "角色性格分析": [
                    f"**{selected_character}**的性格在《后翼弃兵》中极具特色，展现了在象棋世界中的独特表现",
                    f"**MBTI性格类型**: **{character_data['mbti_type']}** - {character_data['mbti_description']}",
                    f"**性格特点**: {character_data['mbti_description'].split('：')[1]}",
                    f"在男性主导的象棋世界中，{selected_character}的性格特点得到了充分展现",
                    f"角色的人际关系处理方式体现了其性格的核心特征",
                    f"面对象棋挑战和人生困境，{selected_character}展现出了独特的应对策略",
                    f"性格中的优缺点在剧情发展中起到了关键作用",
                    f"与其他角色的互动展现了{selected_character}性格的多面性"
                ],
                "棋艺分析": [
                    f"**{selected_character}**的棋艺等级为: **{character_data['chess_level']}**",
                    f"**棋艺分析**: {character_data['chess_description']}",
                    f"在象棋比赛中，{selected_character}的棋艺风格独具特色",
                    f"角色的开局选择、中局战术和残局技巧值得深入研究",
                    f"面对不同对手时，{selected_character}展现出了灵活的应对策略",
                    f"棋艺的成长和发展也是角色塑造的重要组成部分",
                    f"角色在关键比赛中的表现往往成为剧情高潮"
                ],
                "剧情作用分析": [
                    f"**{selected_character}**在《后翼弃兵》剧情中扮演着重要角色",
                    f"作为{character_data['role']}，在贝丝的成长道路上发挥了独特作用",
                    f"与其他角色的互动推动了剧情的关键发展",
                    f"在贝丝的象棋生涯中，{selected_character}代表了重要的影响力量",
                    f"角色的选择和行动往往成为剧情转折的关键",
                    f"成长轨迹与主线剧情发展高度契合",
                    f"在贝丝的人生旅程中展现了不可替代的价值"
                ],
                "演技评价": [
                    f"**{actor_name}**的表演为{selected_character}注入了灵魂",
                    "表演特点与角色性格高度契合，增强了角色的可信度",
                    "情感表达的层次感丰富，能够准确传达角色的内心世界",
                    "在关键场景中的表演张力十足，给观众留下深刻印象",
                    "台词处理自然流畅，语气变化恰到好处",
                    "能够通过表演展现角色的成长和变化",
                    "整体表演风格与《后翼弃兵》的文艺气质完美融合"
                ],
                "观众共鸣点": [
                    f"**{selected_character}**的角色设定引发了观众的强烈共鸣",
                    "在象棋世界的背景下，角色的个人挣扎让观众感同身受",
                    "面对性别偏见和社会压力时的坚持让观众敬佩",
                    "与其他角色的友情和羁绊让人感动",
                    "在成长过程中的选择引发了观众的深度思考",
                    "角色的命运发展牵动着观众的心弦",
                    "在追求梦想道路上的坚持让人动容"
                ],
                "角色成长轨迹": [
                    f"**{selected_character}**在《后翼弃兵》中经历了显著的成长",
                    "从初始状态到最终定位，角色不断突破自我",
                    "棋艺水平/人际关系/自我认知等方面都有明显提升",
                    "价值观和世界观随着经历不断成熟和完善",
                    "与其他角色的关系发展也反映了角色的成长",
                    "面对挫折时的应对方式展现了角色的心理成长",
                    "最终的角色定位与初期形成了鲜明对比"
                ],
                "演员简介": [
                    f"**{actor_name}**是实力派演员，在《后翼弃兵》中成功塑造了**{selected_character}**这一经典角色",
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