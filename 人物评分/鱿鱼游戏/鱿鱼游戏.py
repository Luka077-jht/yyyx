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
    page_title="🎮 鱿鱼游戏角色评分 - 虎扑风格",
    page_icon="🔺",
    layout="wide"
)

# 自定义CSS样式 - 保持66.7%文件的风格
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
    
    .main-header {
        font-family: 'Noto Sans SC', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(45deg, #FF0000, #FF6B6B, #FF8E53, #FFD93D);
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
        border-left: 4px solid #FF0000;
        transition: all 0.3s ease;
    }
    .character-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    .rating-section {
        background: linear-gradient(135deg, #FF0000 0%, #FF6B6B 100%);
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
        background-color: #FFE082;
        color: #333;
        padding: 0.4rem 1rem;
        margin: 0.3rem;
        border-radius: 15px;
        font-size: 1rem;
        font-weight: bold;
    }
    .hot-comment {
        background-color: #BBDEFB;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid #1976D2;
        color: #1565C0;
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
        background: linear-gradient(135deg, #FF6B6B, #FF8E53);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 1.2rem;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
        box-shadow: 0 4px 8px rgba(255, 107, 107, 0.3);
    }
    .stat-card {
        background: linear-gradient(135deg, #FF0000 0%, #FF6B6B 100%);
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
        border: 4px solid #FF0000;
        margin: 0 auto;
        display: block;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
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
        'id': range(1, 10),
        'name': ['成奇勋', '曹尚佑', '姜晓', '阿里', '韩美女', '张德秀', '吴一男', '黄仁昊', '黄俊昊'],
        'role': ['主角', '反派', '主角', '配角', '配角', '反派', '配角', '组织者', '警察'],
        'description': [
            '456号参赛者，前汽车厂工人，善良但运气不佳',
            '218号参赛者，首尔大学高材生，聪明但冷酷',
            '067号参赛者，脱北者，为了寻找母亲而参赛',
            '199号参赛者，巴基斯坦外籍劳工，善良诚实',
            '212号参赛者，机智灵活的女参赛者',
            '101号参赛者，黑帮老大，暴力残忍',
            '001号参赛者，老年脑瘤患者，游戏的关键人物',
            '游戏幕后组织者，前冠军',
            '潜入游戏的警察，寻找失踪的哥哥'
        ],
        'avg_rating': [9.1, 8.8, 9.0, 8.7, 8.3, 8.0, 8.5, 8.2, 8.4],
        'rating_count': [18500, 16800, 17200, 14500, 12800, 11200, 13500, 11800, 12500],
        'image_url': [
            'c:/Users/17347/Desktop/人物评分/鱿鱼游戏/成奇勋.jpg',
            'c:/Users/17347/Desktop/人物评分/鱿鱼游戏/曹尚佑.jpg',
            'c:/Users/17347/Desktop/人物评分/鱿鱼游戏/姜晓.jpg',
            'c:/Users/17347/Desktop/人物评分/鱿鱼游戏/阿里.jpg',
            'c:/Users/17347/Desktop/人物评分/鱿鱼游戏/韩美女.jpeg',
            'c:/Users/17347/Desktop/人物评分/鱿鱼游戏/张德秀.jpeg',
            'c:/Users/17347/Desktop/人物评分/鱿鱼游戏/吴一男.jpg',
            'c:/Users/17347/Desktop/人物评分/鱿鱼游戏/黄仁昊.jpg',
            'c:/Users/17347/Desktop/人物评分/鱿鱼游戏/黄俊昊.jpg'
        ]
    }
    return pd.DataFrame(characters_data)

# 角色相关的梗和热评
def get_character_memes(character_id):
    memes_dict = {
        1: ["456号", "木槿花开了", "善良的赌徒", "最后的赢家"],
        2: ["218号", "首尔大学", "高智商反派", "人性的选择"],
        3: ["067号", "脱北者", "寻找母亲", "坚强的女性"],
        4: ["199号", "巴基斯坦", "诚实的人", "悲剧的命运"],
        5: ["212号", "机智美女", "生存智慧", "团队合作"],
        6: ["101号", "黑帮老大", "暴力残忍", "权力的游戏"],
        7: ["001号", "老年患者", "游戏真相", "关键人物"],
        8: ["幕后组织者", "前冠军", "游戏设计", "人性的考验"],
        9: ["警察", "寻找哥哥", "正义使者", "真相调查"]
    }
    
    comments_dict = {
        1: ["李政宰的演技太棒了，成奇勋的善良和挣扎让人心疼", "从失败者到赢家，角色的成长很有说服力"],
        2: ["朴海秀把曹尚佑演活了，高智商反派的复杂性很到位", "这个角色展现了人性的黑暗面"],
        3: ["郑好娟的姜晓太让人心疼了，脱北者的坚强很感人", "为了母亲参赛的动机很真实"],
        4: ["阿里的善良和诚实让人印象深刻，结局很悲剧", "外籍劳工的处境很有现实意义"],
        5: ["韩美女的机智和生存智慧很精彩", "女性在极端环境下的表现很有看点"],
        6: ["张德秀的暴力残忍让人不寒而栗", "黑帮老大的形象塑造很成功"],
        7: ["吴一男是游戏的关键，老人的智慧很深刻", "001号角色的反转很精彩"],
        8: ["黄仁昊作为组织者展现了游戏的残酷本质", "前冠军的身份很有戏剧性"],
        9: ["黄俊昊的警察角色为剧情增添了悬疑元素", "寻找哥哥的线索很关键"]
    }
    
    memes = memes_dict.get(character_id, [])
    comments = comments_dict.get(character_id, [])
    return memes[:3], comments[:2]

# 五星评分系统
def star_rating_component(character_id, current_rating=0):
    stars_html = f"""
    <div class="star-rating" id="stars-{character_id}">
    """
    
    for i in range(1, 6):
        filled = "🌟" if i <= current_rating else "⚪"
        star_class = "star" if i <= current_rating else "star empty"
        stars_html += f'<span class="{star_class}" onclick="setRating({character_id}, {i})">{filled}</span>'
    
    stars_html += f"""
        <span class="score-highlight" style="margin-left: 15px;">{current_rating}/5</span>
    </div>
    <script>
        function setRating(charId, rating) {{
            // 更新星星显示
            const stars = document.querySelectorAll('#stars-' + charId + ' .star');
            stars.forEach((star, index) => {{
                if (index < rating) {{
                    star.textContent = '🌟';
                    star.classList.remove('empty');
                }} else {{
                    star.textContent = '⚪';
                    star.classList.add('empty');
                }}
            }});
            
            // 更新评分显示
            const ratingSpan = document.querySelector('#stars-' + charId + ' span:last-child');
            ratingSpan.textContent = rating + '/5';
            
            // 发送评分到Streamlit
            window.parent.postMessage({{
                type: 'streamlit:starRating',
                data: {{ characterId: charId, rating: rating }}
            }}, '*');
        }}
    </script>
    """
    
    return stars_html

# 角色评分界面
def character_rating_interface():
    st.markdown('<div class="main-header">🔺 鱿鱼游戏角色评分</div>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">✨ 虎扑风格评分系统 · 实时统计 · 热评互动</p>', unsafe_allow_html=True)
    
    # 侧边栏 - 筛选器
    with st.sidebar:
        st.header("🔍 筛选设置")
        
        # 角色类型筛选
        roles = ['全部'] + list(st.session_state.characters_df['role'].unique())
        selected_role = st.selectbox("角色类型", roles)
        
        # 评分范围
        min_score, max_score = st.slider(
            "评分范围", 
            min_value=0.0, 
            max_value=10.0, 
            value=(7.0, 9.5),
            step=0.1
        )
        
        # 搜索框
        search_term = st.text_input("🔎 搜索角色", placeholder="输入角色名或描述...")
        
        # 应用筛选
        filtered_characters = st.session_state.characters_df.copy()
        if selected_role != '全部':
            filtered_characters = filtered_characters[filtered_characters['role'] == selected_role]
        
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
        sort_by = st.selectbox("排序方式", ["综合评分", "评分人数", "角色名称"])
        
        if sort_by == "综合评分":
            ranked_characters = filtered_characters.sort_values('avg_rating', ascending=False)
        elif sort_by == "评分人数":
            ranked_characters = filtered_characters.sort_values('rating_count', ascending=False)
        else:
            ranked_characters = filtered_characters.sort_values('name', ascending=True)
        
        # 角色展示和评分
        for _, character in ranked_characters.iterrows():
            with st.container():
                st.markdown(f'<div class="character-card">', unsafe_allow_html=True)
                
                # 角色信息布局 - 优化图片和评分布局
                col_a, col_b = st.columns([2, 3])
                
                with col_a:
                    # 角色图片 - 放大到与评分框等宽
                    st.image(character['image_url'], width='stretch', caption=character['name'])
                    
                    # 评分显示 - 与图片宽度对齐
                    st.markdown(f'<div class="score-highlight" style="text-align: center; margin-top: 10px;">评分: {character["avg_rating"]}</div>', 
                               unsafe_allow_html=True)
                    st.markdown(f'<div style="text-align: center; font-size: 0.9rem; color: #666; margin-top: 5px;">👥 {character["rating_count"]}人评分</div>', 
                               unsafe_allow_html=True)
                
                with col_b:
                    # 角色基本信息 - 放大字体
                    st.markdown(f"<h2 style='font-size: 1.8rem; margin-bottom: 10px;'>{character['name']}</h2>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size: 1.2rem; font-weight: bold; color: #FF0000; margin-bottom: 8px;'>身份: {character['role']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size: 1.1rem; line-height: 1.4; margin-bottom: 15px;'>{character['description']}</p>", unsafe_allow_html=True)
                    
                    # 虎扑式热评和梗 - 放大字体
                    memes, comments = get_character_memes(character['id'])
                    
                    if memes:
                        st.markdown("<h4 style='font-size: 1.3rem; margin-bottom: 10px;'>🔥 角色热梗</h4>", unsafe_allow_html=True)
                        meme_cols = st.columns(len(memes))
                        for i, meme in enumerate(memes):
                            with meme_cols[i]:
                                st.markdown(f'<div class="meme-tag" style="font-size: 1rem;">{meme}</div>', unsafe_allow_html=True)
                    
                    # 五星评分系统 - 优化布局
                    st.markdown("### ⭐ 为角色评分")
                    current_user_rating = st.session_state.character_ratings.get(character['id'], 0)
                    
                    # 创建五星评分组件
                    stars_html = star_rating_component(character['id'], current_user_rating)
                    components.html(stars_html, height=60)
                    
                    # 显示用户评分（如果有）
                    if current_user_rating > 0:
                        st.markdown(f'<div style="text-align: center; background: #4CAF50; color: white; padding: 8px; border-radius: 10px; margin: 10px 0;">您已评分: {current_user_rating}星</div>', 
                                   unsafe_allow_html=True)
                    
                    # 显示热评 - 放大字体
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
        
        # 排行榜
        st.subheader("🏆 角色排行榜")
        
        for i, (_, character) in enumerate(ranked_characters.head(5).iterrows(), 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            
            st.markdown(f"<div style='font-size: 1.2rem; margin-bottom: 10px;'>{medal} <strong>{character['name']}</strong></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 1.1rem; margin-bottom: 5px;'>  评分: <strong>{character['avg_rating']}</strong> 🌟</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 1.1rem; margin-bottom: 5px;'>  身份: {character['role']}</div>", unsafe_allow_html=True)
            
            # 显示用户评分
            user_score = st.session_state.character_ratings.get(character['id'])
            if user_score:
                st.markdown(f"<div style='font-size: 1.1rem; margin-bottom: 10px;'>  我的评分: <strong>{user_score}</strong> 🌟</div>", unsafe_allow_html=True)
            
            st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)

# AI角色分析界面
def ai_character_analysis():
    st.markdown("## 🔮 AI角色深度解析")
    st.markdown("### 💫 让AI帮你分析角色特点和观剧体验")
    
    # 角色选择
    character_names = [char['name'] for _, char in st.session_state.characters_df.iterrows()]
    selected_character = st.selectbox("选择要分析的角色", character_names, key="ai_character")
    
    # 获取角色数据
    character_data = st.session_state.characters_df[st.session_state.characters_df['name'] == selected_character].iloc[0]
    
    # 分析维度选择
    analysis_type = st.selectbox("分析维度", 
                                ["角色性格分析", "剧情作用分析", "演技评价", "观众共鸣点", "角色成长轨迹"])
    
    if st.button("🔮 启动AI分析", type="primary", key="ai_analyze"):
        with st.spinner('AI正在深度解析角色...'):
            time.sleep(2)
            
            # 模拟AI分析结果
            analysis_results = {
                "角色性格分析": [
                    f"**{selected_character}**的性格复杂而立体",
                    "展现了人性的多面性和深度",
                    "角色动机和行为逻辑清晰合理"
                ],
                "剧情作用分析": [
                    f"**{selected_character}**在剧情中起到关键推动作用",
                    "与其他角色的互动富有戏剧张力",
                    "对主题表达有重要贡献"
                ],
                "演技评价": [
                    "演员的表演细腻而富有层次感",
                    "情感表达真实自然",
                    "角色塑造深入人心"
                ],
                "观众共鸣点": [
                    "角色经历引发观众强烈共情",
                    "情感表达真实可信",
                    "角色命运牵动人心"
                ],
                "角色成长轨迹": [
                    "角色经历了显著的成长和变化",
                    "性格发展合理且有说服力",
                    "最终命运与角色设定高度契合"
                ]
            }
            
            st.success(f"### 🎯 AI对**{selected_character}**的{analysis_type}")
            
            for point in analysis_results[analysis_type]:
                st.info(f"✨ {point}")
            
            # 显示角色图片
            st.image(character_data['image_url'], width=200, caption=selected_character)
            
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