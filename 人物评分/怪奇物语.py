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
    page_title="🎬 怪奇物语角色评分 - 虎扑风格",
    page_icon="🔮",
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
        background: linear-gradient(45deg, #8B0000, #B22222, #DC143C, #FF4500);
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
        background: linear-gradient(135deg, #8B0000 0%, #B22222 100%);
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
        background: linear-gradient(135deg, #8B0000 0%, #B22222 100%);
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
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
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

# 怪奇物语角色数据
def initialize_characters():
    characters_data = {
        'id': range(1, 9),
        'name': ['Eleven', 'Mike Wheeler', 'Will Byers', 'Dustin Henderson', 'Lucas Sinclair', 'Max Mayfield', 'Steve Harrington', 'Jim Hopper'],
        'role': ['超能力女孩', '团队领袖', '失踪男孩', '科学天才', '怀疑论者', '新成员', '前恶霸', '警长'],
        'description': [
            '拥有超能力的实验体女孩，能够用意念移动物体',
            '团队的核心领导者，勇敢且富有责任感',
            '被颠倒世界抓走的男孩，拥有特殊感知能力',
            '聪明机智的科学爱好者，擅长解决问题',
            '最初对Eleven持怀疑态度，后来成为忠实朋友',
            '勇敢独立的滑板女孩，加入团队后展现价值',
            '从校园恶霸成长为保护孩子们的可靠大哥',
            '霍金斯警长，外表粗犷内心温柔的保护者'
        ],
        'mbti_type': ['INFJ', 'ENFJ', 'ISFP', 'ENTP', 'ISTJ', 'ESTP', 'ESFJ', 'ISTP'],
        'mbti_description': [
            'INFJ（提倡者型）：直觉敏锐，富有同情心，追求深层意义',
            'ENFJ（主人公型）：天生的领导者，富有魅力，关心他人',
            'ISFP（探险家型）：艺术家性格，敏感细腻，活在当下',
            'ENTP（辩论家型）：聪明机智，好奇心强，善于创新',
            'ISTJ（物流师型）：务实可靠，注重规则，忠诚坚定',
            'ESTP（企业家型）：行动派，勇敢果断，适应力强',
            'ESFJ（执政官型）：社交达人，乐于助人，保护欲强',
            'ISTP（鉴赏家型）：实用主义者，冷静理性，行动派'
        ],
        'actor_name': ['Millie Bobby Brown', 'Finn Wolfhard', 'Noah Schnapp', 'Gaten Matarazzo', 'Caleb McLaughlin', 'Sadie Sink', 'Joe Keery', 'David Harbour'],
        'actor_bio': [
            '英国女演员，因饰演Eleven一角而闻名全球，演技备受赞誉',
            '加拿大演员兼音乐人，在怪奇物语中展现出色的表演天赋',
            '美国演员，成功塑造了Will Byers这一复杂角色',
            '美国演员，以独特的表演风格和幽默感深受观众喜爱',
            '美国演员，在剧中展现了出色的舞蹈和表演才能',
            '美国女演员，以勇敢独立的Max形象深入人心',
            '美国演员，成功演绎了Steve从恶霸到英雄的转变',
            '美国资深演员，演技扎实，完美诠释了警长角色'
        ],
        'famous_works': [
            ['怪奇物语', '哥斯拉大战金刚', '福尔摩斯小姐'],
            ['怪奇物语', '小丑回魂', '超能敢死队'],
            ['怪奇物语', '等待安雅', '夏日友晴天'],
            ['怪奇物语', '悲惨世界', '荣誉学生'],
            ['怪奇物语', '具体目标', '新城市'],
            ['怪奇物语', '恐惧街', '鲸鱼'],
            ['怪奇物语', '蜘蛛头', '自由之声'],
            ['怪奇物语', '黑寡妇', '地狱男爵']
        ],
        'avg_rating': [9.4, 8.8, 8.6, 9.1, 8.4, 8.9, 9.2, 9.3],
        'rating_count': [18500, 16200, 14800, 17200, 13500, 15800, 16800, 17500],
        'image_url': [
            # Eleven - 使用真实的怪奇物语角色图片
            'https://upload.wikimedia.org/wikipedia/en/5/52/Eleven_%28Stranger_Things%29.jpg',
            # Mike Wheeler - 使用真实的怪奇物语角色图片
            'https://upload.wikimedia.org/wikipedia/en/3/38/An_image_of_the_character_Mike_Wheeler_%28portrayed_by_Finn_Wolfhard%29_from_season_3_of_the_Netflix_series_%22Stranger_Things%22.png',
            # Will Byers - 使用真实的怪奇物语角色图片
            'https://upload.wikimedia.org/wikipedia/en/b/b4/Will_Byers.jpg',
            # Dustin Henderson - 使用真实的怪奇物语角色图片
            'https://static.wikia.nocookie.net/strangerthings8338/images/0/07/Dustin_S4.png/revision/latest/scale-to-width-down/1000?cb=20220531050146',
            # Lucas Sinclair - 使用真实的怪奇物语角色图片
            'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSbGjQheT203HufCqDZsQ5jqjbXCpHJ4Q02Vc2YfeScm93tfgJiMbn7WosaUYfozhk3a13vt_ppIzBB-p0tBgG7SloCDTMoHE9LGQ9uG-A&s=10',
            # Max Mayfield - 使用真实的怪奇物语角色图片
            'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRz60kGj9quQAfnP11SEHu_tAzjuOT5a6haneb1gF8SuTZWI95wPVjRyY_g4TvbllLPIIeUoOEEoMhNKDQtMy4QfPfJUeLP7plpTu66Mw&s',
            # Steve Harrington - 使用真实的怪奇物语角色图片
            'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRP_FaefNOYhgYDGwKBGYYBIld5mGM3UEx3cP_B65eZnxzbe2xupK5i4TxfF5ouFMET_A4PJ2Ab3s8xYQRr_C-aWdklxbkVXTjXjAmzm6Q&s',
            # Jim Hopper - 使用真实的怪奇物语角色图片
            'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQAGoMcMYdyPH-n55mTSZ5w_2nULnyfe0az2YdwbbzM97SzP3USUnZhwFuJzyavSYfnzmU6mLtibPRwQShKmtg7a8VECZotveAEWSU89ts&s'
        ],
        'actor_photo_url': [
            # Millie Bobby Brown - 使用真实的演员照片
            'data:image/webp;base64,UklGRs4aAABXRUJQVlA4IMIaAAAwYgCdASrXAJMAPtlWokwoJKMiMBTe8QAbCWM966GDhCAmQk+yYEyBxxWYmkDoH7uEwDPJmNPs/gf++/p/i3+l9gBcj+I8Ce0V2U/vWXygD7sD9HzT/kefHvw/xn/Z9gT9Kesl37/3no4faX+5nsxBWdyNjuUZQj3lB52EzKtED8WgLlgiQSqEB1sDp5NbC4/4xlNgUBuDomh3+EM1BW//pnImzBKEjg+/scUVvG1cwngULYN1yzxSrW1t5rtmbuIHJhbK41ZLhc8369/zPMB8dB6R8HemKS1IYrtlxELVOWsskbxYskjID/npRcpXnFQQZcgsrzCz/uA6N21CjbCzaxhM01P+MNbvYsr+0dHjdg0ihy8VfuOLhhlWi7zgs9R9z8SQSp+L1TW+ki8z5vRqvgNSGGJu3dkehCJu+yg2n4IcxsAhitBD/8y4OqTRm6tpj1zV2NcpmEG3WJnFQWodQVO76lq7Pr9Zs7FNgQUVsE0NVJh89JnbBf1F5etm3cXBGyLxyHSFznTn9u1RO0mh5id5QkKESlNmUl+siaKcTqDv/5Lf46y0H7qGZeHmMeJ7YVyXZb9GQVTWkMRa94Nuy0zIoo8aCrxYt9coBfLFWC/F4cM150H98LWaTve7Ct4IjbUNkKw9YGwobg53449AaRioZHFTMUAhvg2FTyVBAVym+zJvxtOzbZWy1juq+aypYc+q6pi7yHr9+4Oar2sFjGntTZ7hYWCLERtOUiyWA90h+YB30Bt1l+XFgjTFD6W6ym9+tI6qSXOHhD6Lp+uwl75vCxQQmX5idQVpehM6q06GL4Sg+CRYCInjor5IkJHjgSNi8mbdojjyDZn/1TAMc4KZvUUwryPf3PvSXPeqIbZ00FaE5d/KjQqwLfHB/tCERP7LtAbR6HVw5Wry5FsrXM0Aei6mIPzdSBdW8C9cIhKIz7J9FohkfXv1si/WK7zOjyqQ4lgHKgq4Fq/SxLDP47+6zt4LWNjq6PeQRXfk0beGiSD8R+WWtBkSK6H8VCDljU875hb37rss75hXjK7zj5LrqDVTO9dxQAD+5uWd8iTZ+V9/jg1lq6c1zYqb3UV80hUUTIsKEqgXwiFz/a8uO2wHFY4dW4WDjfBj+ggqCdA/RYhfQw8Y8fBjAxYBlDiFD//Ha7rXqmowSt1TIyh3/AqMY+r3ZpJAYJuU9QKOsmAfcbrKKQDl1Uv6CeuLUeDsiUaE+QS2lzJlN/AhJyvMdZ1Dxd7DbN8MMIraBPlxBSbqZyX0TVWN1pluT09OJHBhPbRQ3c8yTKmj4O5iM1DkzH8EpsZshYB1lZOe+Dn0j4EMjih130dw/u/263Dgmq0RTfGy22IhbIpxn83aspIHwSbOlCcJ+UfQC6yJZbUQ28tPop3rZ5Y3UCuNdYQkjonYlwWZij1vos/N2Le8oBWWW2aUCFNT4EtRlky+4hAI0625TX9Il3kHNBPLHd8upVxBmn9BII3zjp+zDEVP3HitsBgE4tXPpYDpOeZBYcy78LvEaV8Ax7dLf25B83IXMcE0n6ztzn6Y3aKRZ91bYBUtPfnz0ozv7l4owiOBYGyRs9z7MsD7Utxr7Nx7k6yGASiDUDwJ7XxhQjanyUZVQmaDjCL8sIlhOHDLXrLJdyOElUVydBdPe7fi5NCq72SXcyGxlwRux1JNcpqAiGQqoKn1dyi1/YsK91fk5ocx3pNpcNUp0N17JmGYX7g+UQBdCU11IzOme3/819J8XhXtVtQopw+QcK/0RzoWUGni7IOAjvlY5uuQQg/cCizMw+usAMhskNAzwP2MEgPBP4Z3IG/PEuiZDj0xNbqd3is4ZOe5jjBQdg0z2qNSk2w4KHO3cgDPn21h/wjJyy4+2/17+QOp7t2P7mvwMUQ79RLMZfbPbzD4nQbbJaqn2o+/aMjUqiilKykGQjxD/pk2stkxyFT0I0o9HV67pr2CmYogVxhkr6PfQ8fBGvCIsy76BMY3kLcMYH92tG8J3gLn8Axg7qTUsK2+hS0ukGUjh6mCIHiC1TL50U4NLFPSJ0Q1G0OUiyjomxn0Ufb7WXov/Ip2k/k6pbgnuubGxlG17dGLE2qa6kM4sKyw3mNjttrS4/o7VrQiomyv5R/fSNTuCmyfFuFJEGE9MN1HLH9bADq5mge9WPfu4N3x05JRaDhvcp3xk9G5QAAkYWyNMazi0CHTLIWSGnUb1vbEar0Njq7jt+tIUoN9yijqB+rlWuk4sSBVPipI2a5n74FhWWe7Qho4CW/eiIH9v2tX2P1XW74YovYap1ilez2DPt34tHUSWYLn8V9wVThoL4sPgZcgXvEck7s1/XBtQj7MOxbrMg10ytb14aVVzk7My0MgKi4kP5/W8b3LaUZsOc7h2e7oA/V8CWEl0cWeRx+PaxHfNOgvNOu34xlB/ZEFISwK8GpwMS93/E0FSZ1F4vTWTMuR1241kxkvfg2cAc0veaUxN3mIauZjYfwc1HebzCf41R5A/znxVjbjqsnXAU6xevGglsB/fzH88qeI4AVE4VLiXo0QYngJC0dXvuTN63dbEuH9y+jr9FuE7Sv10bBrfRiAuYabrLGnSvcK1rVgWkGZY7oVyNfMEWkTyzZSIt6BOknMoXTk+ssWB7n1UB5hiYfJyInqKMv4p4zOWvJsQWUGHNTNUVtdQbio4FC46ZAVLCBT6LcLtMC4tW4N0qzJC/SOwxecG1WjS096hzzpVy1N5x8PMclbxoYLcNlYyVohxCTLJO0pzry68UUtj64GeOWj0WXPZX5XZKxwp1qZMWM2tdLmCu2FQgpW6hNH9qABgH5OEdXwHeKRB6ZmimZcBqPrbGYb7ZKEKPxoFXzllwpnu8cW7KcuZ9pQnjZeaUdX09xSrG6YqK5iDiDM0VUpUSFTvcma5BRkB7LvM/hAu3tdIXhMvhCFzYewPC2JFi/s/5Qo+I+uDsXTy3TO52lOvR/bMrqDx5txkhBZqzZE+yOQl1ozCIGNtITmFUJ4zPWYPbA5DKEldIiXTVRoxGEVinuYiEgPmiJ+iy7Xf89STqScV3X2tp3GPGjKSes4gAnneJjK8O6AqshIo6YETe34uC9GFIPjds9ch7Bu2MqMoeRARbcW9MriOlvxhjf6AyW0v+gazMEpDnS+O1F9qkb69dfsIAl0z5hF5oaUSh3marwxcEsTqoNIlyG/ZrQtNRjSt0kpe9LprsuEijdatbJ2Vbryl8rvSDZARRulAZaIhH/E8d1fM74sKcm+wEbwf0bQYSQ87urDABKJHT6tT7MC2mXkhLSKkiwWHPnSsoeQ0hyFxM8uBhj7UI/8YqewGPzQKQYdx80sA7sEiu52C3dAcF3fQG9EiQxS6gjfD09UWpbAG1bOLAaFfwTSyp5Z8HbKh1a/AwxGI1ZpwnsSZOVSVeccClPKcY8fjjZSRw8hfcRXwUISWfyRm27HFdy3o0ONpUs0mzja+/KI17htQtr7LD/QDHyTmHfAaPT6LWnd19oyIBSgo78NusR6lekaLsK/Hr0zgfB2jKPTSWV+vExcgPZvu42GEEtkKrRGtG4xJbyY2t5BVOgEYMlPwCeAl8I9e1ufOLd3qWZ7NO+RDBtnOWofxYZ6Op5ULjknnlSi92/gpq7GmWP7WhU5ZlM7m0yz4tBmU4y0v7p7378a/7doy+I7Knhdo8Gh61Y3bOv+34dlMazDTeKYD4rAM8u4QaUO/2md57F73WXlyPLXYsLz7Hb4Ieo3nIUAD8uxsofexPw9TvTxWoWX6UDpRgPVxbbfG3H/CLzWgMoBlNpefNFuCWuoiFuxMIwdX7KlF6wwSUFnI/zPGBbq8ctArorhF05gmQAXBX6GekQahxGQXJr0VkzWfaar3zyLBkf1BQPRj5i+IDEfoZZy40kNbwHHJsEFprs76bXJUtGw6so47VQYewj1fU+J/CLVUniFgjzj3//K4YXI4Q/5ogfiU/ehZEi3bZA8J0zRHpo4AmL4ChfmLJ9MLGbjD8o7B6BimPLpe3hPQG/7I9i3BT4KgewqfaXWnIewMSAUUzc6ZjHGZQM7y51FmSsJi4yd7KJK7bVZrzCD0BbEvi4YIjHPd4XTf8RtyUP05RYjysBZqO6XgXJ8dCuU6hpvTkL+m/CHAN4UUW9NxNrDjZVLWoqrcw4WKKoLlv6BYVhc45Cj0XMjQoorQ7FCr1QgPbciy9emRRVEr7+Be468711GodLYClZN1ZLkA4aSdjaTskBffTBUHnX3y1bHQrcYjC26SaIyiO990aSM9Mwlsg2E3THF6V6BKpFvXvFsud8n0aZXGNIaQ2PJUbXwBIQNUdzAT9UbfZ5p0DQGBwFwiqr4i93KQGAwa98itt9DnSiRyxzqOxKLXzmab55t3kduI3nDVPYpgLKwwHpuSYs0vYa+9GDBL0T8qPktyzf26Qr5Sk+YZel8c6xS6ZHL5zjeOoAqo9EpHkWhx6TD+ybzoRiyAat7UrwwCOIIlAdUJMRzBmqGmW/Odq3+BI/w4eCmNRvlW9vxtG9kYathAQ6RayfsnMcDF6VEX+05jFnxzE1dMbPJYkt0/BgBLHTvW7LHSzLqBp8bNBhXQPEFYEW+OWYQMlXwG/YGISzayK62PHxiqMm6Ou5qaqJmJZfZ/SPreUx8sHOJ0Hlrv5od0xLpRWjEmqTy4mAcWJ3+84KhF/0kb0iZEbBHjppW0dzQLQrUpTqW/Q6hfglDxw+ZGRCQwdRrz2hfahrUuF+158kVImdJ4c8XKsJiBBRHb5EqgU4RtDh8U5RifWpDxiXpb6ZQmI3Zzb37k+f/GaF5Yi5fD+Eop3lTxKEjixNuM7LWK71OxkuCwo2VQY2VE2OH3HbLGIAE0mn46/sDfuVD0rU5t2alW+kCqGzXRcluxqwkTWnjI785j4tkyxZvw4LnB2TxZvUxb8Y0B/NfuE1Cy2Q6RPJ86RkwHTbPu32X3aXQRlqOUOYDX2IBMn6naMpYWrirSrMemDIPnpIWqxvPjniDG8ub8kQfwMOYzM841ysNGFGUKNQiq6OOTK3TTvTgmI1QtTkOqno8DZm7ZGqzsYA40BMMLClJv9gtt9YNxrWBi1tfIXmz2jWQ1iNNZd4JGv0BICZiIkpAhESiP3hM+MIye80b7PbQ31NJIEIjGvzUlz9OlBEFmYDgCcAfBsCLNZAM/mYvWpEzkpHm/X97+KrZ+3i2Uwtby8+M/Otf5FSAlDZUQqSE0JfmMHplnfG2tIfmKSe8zbvZN+/rftHMOdZ+HZ4Pf0hm2z7LWkVZ9E2hvwzjf9Ffl6hY6IHxUdR/5sU5LwzxU6hircueEY5jnzHV4UUkpaz3vNh+T4I0QpwqynPQterVfLMUS1nWZRz4bH+6RIa/LfTazGJNK3UN573rBd8DE23MnU7/B2Bt6wB/kwM8B9VGEt5uk3EHSKtJucKvg9RkIPXxL9Mz3VNXySVksR6qeTwNQt/0Vrf/6t/tnEhkC1Wk9iCpde3DXwCL91dJQxajvHDddQEqwGoCvIh3lL2eUE2qfVWcwRgcKWONinSXLKYqlXedZN8/Teei9qmc5he55HyWchbCN3tEsw0JU9jEsU1rY84zZbccXhZaswILmDFYrjWbWY1fLlLWHoLOIFzWW/Hm6BfksdKhQcN/2iq3laH0K+0YEiKFlSXdFz9+q1pON00Eqe2WCOq4P5uEJ1w643DeVGGSpmHpVthkDjJMkRD7222KmEWsNlX2uUXKexXb2X0Z1UnIjLvhhY9m8Fqzx4UGv/5I2Min+tGSXkaxOGOFYEF+Hv+r+SA46bRiUUgxTH9mfl7fv5KBPqqdM6AHnT7xhVskX5z0cHualMvDpNHWEwWjr6Zh6n3p2Qo1YhvHS4KF8Bo4MxdnAYYstzm3WAPMJAcznAk1xKLbpKjCRuB1GPxLf4qzT8JvqU7MVtvaN9CbVzzQLaeGg2Xp76qpqZK7mw/7k1726JPDUr7wMDWtsVYT0NxgFDiEMchp0T0B9tl2OGyGfI+BoLmGF2Lpg8phAgtA4dMCqocY8EhoAW7RwV612AdoZ/1NEPsEWXp535M37yI3fBXGI1BSpRkIQVAiAMh+z4hHfJQJXS75GY6FqAh3ezYkA037tm9Q+vhc09vVV7PEUvtqUJGiOJvdogCm/KLqz3KFFjv8T6WzX4cJkBKRTi6hQBvf7DNnlKUGS+7y0EUnGFVFgzeqv7fYPlvQhV5QiCp9CwGbbQPvzfsbHpqYtXF0xovbf7bv42oPbbnnMSU7pQ47kjK+TznOi2MgKaSPWcCFFhnqVaObVaNMof77Ugq5deSJy19CRMQljRYQ0M3WwnPI+nbkaYzYQm1JFGIJ1AN8KYiL8e1dtxdpOu+0DBeMfljBqgHaG3kzEoFbH/tQ5E3o4nFQjdjyqV1Muwp1Xy/ia5sQwpgm4XEwh7mgQS+nDbZsn+Db11F+f3zPeGk2Iocp7GQnbaYmDfMRwzviuBp0yXonuwvL7mVAS2BHVvC5W3T/7XFHV0UrUSFFvDcMIKnfjm5Kj30kAZ6MMmmrnooxXkOkI8iyZD52/tXHYAchBosYAencqK2Kn3Om5oCV+dfTu1jZU/4GPO7o+jhFHNEM3lybHo8uZ2BECMcvhSb64WJ5Qhsatwu6cidYZkEssu+2URTlFq+I5x63U3lT5Ib5gzm0X91HmksxsCB9/e+cGEqcKj4YZuqKILd3n1+uVLasqPX85WElHHCvWyQG9Qv1e9s2kHas3pyAugYGkcAmTqMBs5N8k2vnxV2Uw+UbZnBFV/LLeSDFGx+SckHdH7UGQb2iz6Kk9fmB8uzPPUYA6l4g9JaNYnZY0intj4SGXR0llW9PRv991WPKKJNrheZfXODUBsrZ+L/+pjIj5XBGCteGrEL0Fk/up2DlLjynVHU3k+drJWwh00kUfylsr5/sleU5WijmhFfEOsIWWokTkq2+3Iy41PW/g6U5uxU6M4Tr4VODWEg5+sxtObqKMqBanLsVUWAqcCHMNSPvFHLjGyr19NIruHjarA30QTy3vAJhSvynvMkTNGHNufIT+7EGNL/1PGK+xWqNWXCcvO7kboJAm2B1Ne7uWuRHwRFRik9seIJv4UhOHpZ052dyHYcig4FJQNUeqWjZHcOzoRcQ6/fbE1RYkBRS46pdGygyk45xJfxplQOx1nkU9+Szyek9c58D9KAwV/X1DAKiYB0YvykXCikwUXTbPqFVUfj1+oQ3cLm8XlYVfsDWney3M/uq0BY9+ZNItfH3i3DaPbIj0Hvt4dVHfMke71lt1B0jo/7UeHVRLqGnJpDvBfehFZhPFmNLdaSfGs1FP8hs26x58pdFLrkPeV13e7SWTxYOtDQuI6kTcGUEOtRYYhSw06wrByK6ZKiesOUKi9ley/of8t8rStwyViIcrAsEkfGSx6XUt+Hprn1ImO/iStLi8mV5HElt75D5f1VNX5wxk5+p/9NQPbNHH+gft9M0aIZ5EZ2IJ+iHGDek6dxjMwp1GCHAdQFzrsdlIRgSpsvrvAhTwVNh4kxJ6b99falMjForeZe/e1PMfrvqvLzgp6Rt8S/8DH0fSziAa/coT4Eex2DFctGPln1APIRzTIDiCQSPviC509w36iwXOH2fvSsHkvIPm2WYK1P9INt5/7eFc72MVQD8nL1H9qwWTZmOyIn8cHVLEE0wLJHCD4eJwp0ZhD/VOk/lq9QrZRUKswbyZHLdazn5dIRziSPgKM3R10e8neAGZVeIp75Fpfmt8ZpoKFg9V64ADSPLJpUpwAAdNEQKwwiGXXmEXQ0eORSFPpByDZ4g45u6HrVioZ/zSgw8hShgrMDg2XAIMsT164brO0GNFoak83jfKMI8tR0oi3qQ0PMQD6i6lhx7ywOAKekHfcqHjY7AwwGOFFD+LuckCkXKbzyboVJznnnM6BxL0XN1/V74lW1uvzMo1277EtafMqW/zjHpsMoeSsSn9sIVABBVvDbQYkJ+ETXxfWlvA3ilL7BbdKi5toIVPUS7gcCpmk2zt22GdM52gbbpsaNp9r9mqayp0F5/54qt4Gu/eN+qgCMBRgJoqUVTq9RcmV9EBpHTcOjqB1u2T22GBexpzWxnauE+pyWGrNjs+9SoRA9YXq1XOUsijDM6Qic9eJYLHsieL9/0cb/Bv+PZipJLujXamT536Wi3IY2VxR74RFuQoS4oCuNAjMdXHZjk9+A9UGENS7mfH6qvIgZTE0QxTVDCHvzFXDEFM2BEMoNFPd94dNnCkHdnj95Mvq5Vy+Yuv3TljqBj4FzDNpm7LSVdTkUwtmonBZMqoqBzEAUOmajFlWmwNSkMXaJye2wo9dYRKnLqTVqQiH9rgMHjWZXbbxuTWnQZUdN7Flxo9OvoABC5xb9dntcbqp4fnx2kWYjaeeAH1jfLUmjdJ9Al7dR6iU6o0q/ePjPqexXRC3bHlauyN1T0RFe76DmJwu2eC61LeO6sXnaAmkHYDel6TgyFplFiUbOk39kFghRMD7b9g59D7LHOwMWGBzW2FEZBKidHMsMd3xvQDr5u8lij6hIGt8YH4f11oEmKKXGQQFMPf0phcqMh/9CEgwTHx8X8N3K3rUuG25SasA+jebInFvywN79luP77t+es196A3hAoYiqU7p9UoLkZ3Ysfqwgc2vpbNKHZtNAGUtk/W5taHOiSP7uIu28WoenFqxXmSKzMIiDwNDyHfn18eym+ahZY3PmRB1ZjO8iemGI9UqrFsHZAtHXuEPlqgvGJI1Q5Jk/XZPAHhvQ3ORSrhgDxeFN9WdQWRGEvODO+ZbyHZUJVuXXqsF7xAZuXBgTeM/LBQlismOpkaBhZBDtcFx5f+TLI1+2R/jLckwb5LZv+8ctI6PTrRZMqptR++XYzktI3YkS+4/empybJbZMS1Zmvv3tvL3twrP6qUA14URTOQxeoAKBUOAHG7Ipi4Vkha8e30DqBnzVAHKdaiViN3B8COFf0vLCqmR3bxVgcaIfsxTwbfDopqkAHt9T8YAH7EGqHkedKCimNu0nTR1UYghqppre3IAKnreUAq70EwyLD0f3UpyJgqymXv86CN6RYKLKCnSc8KQIp1BvTorlXou4sMDfOzIRx7XYDBlPWjxHKDyuWRPDExdDVNKiAVaAYHojhNYNXFyGU6qa26DxkACtfYAAA',
            # Finn Wolfhard - 使用真实的演员照片
            'https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcSjViV9cvOklc282FSo62Ep4EMQ_bz-LtQ7cPyC5hWAQOimrJwFxYC29M1YRo8dr0zErW6mkmJHNkUxdImvUp-GBeGrynCeES2QDN2_fhr53yfwEwfxZqtffpK8JfTxLAjxzBl9BJoBYTE&s=19',
            # Noah Schnapp - 使用真实的演员照片
            'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTrkkWkihivMwnhJZuIZLfoSfrAPjwk6Tp_3izFy9cGoxo_PyHDOAcGdOyzttKM-DPr45GBRV28d4UPd3GwAR-AWzNqsZr2UV1Pviyes9w&s=10',
            # Gaten Matarazzo - 使用真实的演员照片
            'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRF98O_vp87fMrjqOXE2sVrfaBxQ5qlWa9-5IlBRHkRjSVrkUPZIEsgZ7CS7uyoLwwDzTsBh2DkTwB3mGKVwUA98gC4g1YhpVxnx7AuQ6Ab4w&s=10',
            # Caleb McLaughlin - 使用真实的演员照片
            'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRF98O_vp87fMrjqOXE2sVrfaBxQ5qlWa9-5IlBRHkRjSVrkUPZIEsgZ7CS7uyoLwwDzTsBh2DkTwB3mGKVwUA98gC4g1YhpVxnx7AuQ6Ab4w&s=10',
            # Sadie Sink - 使用真实的演员照片
            'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTJbc-9MmtggoeTDyjQm4BdYAYL5kT9Jv7F0Ho3bhhZBUVGZIrVRXZN66WbRwpNvUFHu6h_Sq7dU_4_h8AgGuV7XyVYy5DZtC2VM00_mBq5bw&s=10',
            # Joe Keery - 使用真实的演员照片
            'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSmdNhW64ehkN1tXxqBw2lZNZ144XDoOF0e7-KUkJid-9szeYOzvL5GYBKtJ1AnsjZDf6z-o7ZxmEPY_IN39bEsQzohmwMFs89fjh9VbbO4&s=10',
            # David Harbour - 使用真实的演员照片
            'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSjYW034o0UGJ6vBIoy_TUHc6Aw5YypI2bZsX3_wMQ063q_n7InLfjqAIMhVdayGABC7_6hGl8zmleFH5mUvwlZGD0BTc4JEJUq5kgObPPW5g&s=10'
        ]
    }
    return pd.DataFrame(characters_data)

# 代表作品图片映射
def get_work_images(work_name):
    work_images = {
        # 使用真实的电影海报图片
        '怪奇物语': 'https://upload.wikimedia.org/wikipedia/en/d/d4/Stranger_Things_season_4.jpg',
        '哥斯拉大战金刚': 'https://upload.wikimedia.org/wikipedia/en/6/63/Godzilla_vs._Kong.png',
        '福尔摩斯小姐': 'https://upload.wikimedia.org/wikipedia/en/0/0a/Enola_Holmes_poster.jpg',
        '小丑回魂': 'https://upload.wikimedia.org/wikipedia/en/5/5a/It_%282017%29_poster.jpg',
        '超能敢死队': 'https://upload.wikimedia.org/wikipedia/en/a/af/Ghostbusters_Afterlife_poster.jpg',
        '等待安雅': 'https://upload.wikimedia.org/wikipedia/en/7/7f/Waiting_for_Anya_poster.jpg',
        '夏日友晴天': 'https://upload.wikimedia.org/wikipedia/en/3/33/Luca_%282021_film%29.png',
        '悲惨世界': 'https://upload.wikimedia.org/wikipedia/en/8/8f/Les_Mis%C3%A9rables_%282019_film%29_poster.jpg',
        '荣誉学生': 'https://upload.wikimedia.org/wikipedia/en/9/9c/The_Honor_List_poster.jpg',
        '具体目标': 'https://upload.wikimedia.org/wikipedia/en/4/4c/Concrete_Cowboy_poster.jpg',
        '新城市': 'https://upload.wikimedia.org/wikipedia/en/1/1e/New_City_poster.jpg',
        '恐惧街': 'https://upload.wikimedia.org/wikipedia/en/6/6d/Fear_Street_Part_One_1994_poster.jpg',
        '鲸鱼': 'https://upload.wikimedia.org/wikipedia/en/2/2f/The_Whale_poster.jpg',
        '蜘蛛头': 'https://upload.wikimedia.org/wikipedia/en/7/7e/Spiderhead_poster.jpg',
        '自由之声': 'https://upload.wikimedia.org/wikipedia/en/3/33/Sound_of_Freedom_poster.jpg',
        '黑寡妇': 'https://upload.wikimedia.org/wikipedia/en/e/e9/Black_Widow_%282021_film%29_poster.jpg',
        '地狱男爵': 'https://upload.wikimedia.org/wikipedia/en/a/a7/Hellboy_%282019_film%29_poster.jpg'
    }
    # 使用可靠的备用图片
    return work_images.get(work_name, 'https://upload.wikimedia.org/wikipedia/en/d/d4/Stranger_Things_season_4.jpg')

# 角色相关的梗和热评
def get_character_memes(character_id):
    memes_dict = {
        1: ["Eleven的鼻血", "Eggo华夫饼", "超能力女孩", "011号实验体"],
        2: ["Mike的执着", "团队领袖", "对Eleven的爱", "勇敢的男孩"],
        3: ["Will的感知", "失踪的男孩", "颠倒世界的幸存者", "敏感的灵魂"],
        4: ["Dustin的科学", "无牙仔的爸爸", "机智的天才", "幽默的伙伴"],
        5: ["Lucas的怀疑", "最初的谨慎", "忠诚的朋友", "弓箭手"],
        6: ["Max的滑板", "新成员的勇气", "独立女孩", "Running Up That Hill"],
        7: ["Steve的发型", "从恶霸到英雄", "可靠的哥哥", "棒球棍战士"],
        8: ["Hopper的咖啡", "粗犷的警长", "温柔的保护者", "父亲形象"]
    }
    
    comments_dict = {
        1: ["Millie Bobby Brown的表演太出色了，Eleven的角色塑造非常成功", "超能力女孩的形象深入人心，演技炸裂"],
        2: ["Finn Wolfhard完美演绎了团队领袖的角色，勇敢且富有责任感", "Mike对Eleven的感情线让人感动"],
        3: ["Noah Schnapp成功塑造了Will这一复杂角色，表演细腻感人", "Will的遭遇让人心疼，演员演技在线"],
        4: ["Gaten Matarazzo的幽默感和机智让Dustin成为最受欢迎的角色之一", "科学天才的形象塑造得非常成功"],
        5: ["Caleb McLaughlin展现了Lucas从怀疑到忠诚的转变，表演自然", "弓箭手的设定很有特色"],
        6: ["Sadie Sink的Max形象勇敢独立，加入团队后展现重要价值", "Running Up That Hill的场景太经典了"],
        7: ["Joe Keery成功演绎了Steve从恶霸到英雄的成长历程", "可靠的哥哥形象深受观众喜爱"],
        8: ["David Harbour的警长角色外表粗犷内心温柔，表演非常有层次感", "父亲形象的保护者让人感动"]
    }
    
    memes = memes_dict.get(character_id, [])
    comments = comments_dict.get(character_id, [])
    return memes[:3], comments[:2]

# 五星评分系统（使用Streamlit原生组件）
def star_rating_component(character_id, current_rating=0):
    # 使用Streamlit的selectbox模拟五星评分
    rating_options = ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"]
    selected_rating = st.selectbox(
        "选择评分",
        options=rating_options,
        index=current_rating-1 if current_rating > 0 else 0,
        key=f"rating_select_{character_id}"
    )
    
    # 显示当前评分
    rating_value = rating_options.index(selected_rating) + 1
    st.write(f"当前评分: {rating_value}/5")
    
    return rating_value

# 显示角色卡片
def display_character_card(character):
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # 显示角色图片
        st.image(character['image_url'], width=200, caption=character['name'], use_container_width=False)
    
    with col2:
        st.markdown(f"### {character['name']} - {character['role']}")
        st.markdown(f"**{character['description']}**")
        
        # MBTI信息
        st.markdown(f"**MBTI类型**: {character['mbti_type']}")
        st.markdown(f"*{character['mbti_description']}*")
        
        # 评分信息
        col3, col4 = st.columns(2)
        with col3:
            st.markdown(f"<div class='score-highlight'>平均评分: {character['avg_rating']}/10</div>", unsafe_allow_html=True)
        with col4:
            st.markdown(f"<div class='score-badge'>评分人数: {character['rating_count']}</div>", unsafe_allow_html=True)

# 显示演员信息
def display_actor_info(character):
    st.markdown("<div class='actor-section'>", unsafe_allow_html=True)
    st.markdown("### 🎭 演员信息")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image(character['actor_photo_url'], width=120, caption=character['actor_name'], use_container_width=False)
    
    with col2:
        st.markdown(f"**{character['actor_name']}**")
        st.markdown(f"*{character['actor_bio']}*")
        
        # 代表作品
        st.markdown("**代表作品:**")
        works_html = "<div class='works-grid'>"
        for work in character['famous_works']:
            works_html += f"<div class='work-item'>{work}</div>"
        works_html += "</div>"
        st.markdown(works_html, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# 显示梗和热评
def display_memes_and_comments(character_id):
    memes, comments = get_character_memes(character_id)
    
    if memes:
        st.markdown("**🔥 相关梗:**")
        meme_html = ""
        for meme in memes:
            meme_html += f"<span class='meme-tag'>{meme}</span>"
        st.markdown(meme_html, unsafe_allow_html=True)
    
    if comments:
        st.markdown("**💬 热门评论:**")
        for comment in comments:
            st.markdown(f"<div class='hot-comment'>{comment}</div>", unsafe_allow_html=True)

# 角色评分界面
def character_rating_interface():
    # 页面标题
    st.markdown("<h1 class='main-header'>🎬 怪奇物语角色评分</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>虎扑风格 · 专业评分 · 深度解析</p>", unsafe_allow_html=True)
    
    # 角色筛选
    col_filter1, col_filter2 = st.columns([1, 1])
    
    with col_filter1:
        role_filter = st.multiselect(
            "筛选角色类型",
            options=['超能力女孩', '团队领袖', '失踪男孩', '科学天才', '怀疑论者', '新成员', '前恶霸', '警长'],
            default=['超能力女孩', '团队领袖', '失踪男孩', '科学天才', '怀疑论者', '新成员', '前恶霸', '警长']
        )
    
    with col_filter2:
        search_name = st.text_input("搜索角色名称")
    
    # 筛选角色
    filtered_characters = st.session_state.characters_df.copy()
    if role_filter:
        filtered_characters = filtered_characters[filtered_characters['role'].isin(role_filter)]
    if search_name:
        filtered_characters = filtered_characters[filtered_characters['name'].str.contains(search_name, case=False)]
    
    # 按评分排序
    ranked_characters = filtered_characters.sort_values('avg_rating', ascending=False)
    
    # 主内容区域
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # 显示筛选后的角色
        for _, character in ranked_characters.iterrows():
            st.markdown("<div class='character-card'>", unsafe_allow_html=True)
            
            # 角色信息行
            col_char1, col_char2 = st.columns([2, 3])
            
            with col_char1:
                # 角色图片 - 放大图片让宽边与文字紧邻
                st.image(character['image_url'], width=280, caption=character['name'])
            
            with col_char2:
                st.markdown(f"### {character['name']} - {character['role']}")
                st.markdown(f"**{character['description']}**")
                
                # MBTI信息
                st.markdown(f"**MBTI类型**: {character['mbti_type']}")
                st.markdown(f"*{character['mbti_description']}*")
                
                # 评分信息
                col_rating1, col_rating2 = st.columns(2)
                with col_rating1:
                    st.markdown(f"<div class='score-highlight'>平均评分: {character['avg_rating']}/10</div>", unsafe_allow_html=True)
                with col_rating2:
                    st.markdown(f"<div class='score-badge'>评分人数: {character['rating_count']}</div>", unsafe_allow_html=True)
                
                # 评分区域
                st.markdown("<div class='rating-section'>", unsafe_allow_html=True)
                st.markdown("### ⭐ 为角色评分")
                
                # 当前评分
                current_rating = st.session_state.character_ratings.get(character['id'], 0)
                
                # 使用新的五星评分组件
                rating = star_rating_component(character['id'], current_rating)
                
                if st.button("提交评分", key=f"submit_{character['id']}"):
                    st.session_state.character_ratings[character['id']] = rating
                    st.session_state.rating_sessions += 1
                    st.success(f"✅ 已为 {character['name']} 评分 {rating} 星！")
                    st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # 显示演员信息
                display_actor_info(character)
                
                # 显示梗和热评
                display_memes_and_comments(character['id'])
            
            st.markdown("</div>", unsafe_allow_html=True)
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
    actor_name = character_data['actor_name']
    famous_works = character_data['famous_works']
    
    # 分析维度选择
    analysis_type = st.selectbox("分析维度", 
                                ["角色性格分析", "剧情作用分析", "演技评价", "观众共鸣点", "角色成长轨迹", "演员简介", "代表作品分析", "演艺生涯发展"])
    
    if st.button("🔮 启动AI分析", type="primary", key="ai_analyze"):
        with st.spinner('AI正在深度解析角色...'):
            time.sleep(2)
            
            # 模拟AI分析结果
            analysis_results = {
                "角色性格分析": [
                    f"**{selected_character}**的性格复杂而立体，展现了人性的多面性和深度",
                    f"**MBTI性格类型**: **{character_data['mbti_type']}** - {character_data['mbti_description']}",
                    f"**{character_data['mbti_type']}性格特点**: 这种性格类型在剧中得到了完美体现，角色行为与MBTI特征高度一致",
                    f"角色动机和行为逻辑清晰合理，每个决定都有其内在的心理依据",
                    f"**{selected_character}**的性格转变自然流畅，从开始到结束都有明显的发展轨迹",
                    f"角色内心的矛盾与挣扎被刻画得淋漓尽致，让观众能够深刻理解其行为",
                    f"**{selected_character}**的性格特点与剧情发展高度契合，相互促进",
                    f"角色的性格缺陷也被真实呈现，增加了人物的立体感和可信度",
                    f"通过**{selected_character}**的性格塑造，展现了人性的复杂性和多样性",
                    f"**MBTI分析**: {character_data['mbti_type']}类型的特点在角色决策、人际关系和情感表达中都有明显体现"
                ],
                "剧情作用分析": [
                    f"**{selected_character}**在剧情中起到关键推动作用，是故事发展的核心动力",
                    f"与其他角色的互动富有戏剧张力，每次交锋都推动剧情向前发展",
                    f"对主题表达有重要贡献，通过角色的经历深刻揭示了社会问题",
                    f"**{selected_character}**的存在使剧情更加丰富多元，增加了观赏性",
                    f"角色的选择和行动往往成为剧情转折的关键节点",
                    f"通过**{selected_character}**的视角，观众能够更深入地理解剧情内涵",
                    f"角色在剧情中的定位精准，既不过分突出也不被边缘化"
                ],
                "演技评价": [
                    "演员的表演细腻而富有层次感，每个细节都经过精心设计",
                    "情感表达真实自然，能够让观众产生强烈的代入感",
                    "角色塑造深入人心，表演风格与角色设定高度契合",
                    "台词功底扎实，语气语调的变化恰到好处",
                    "肢体语言丰富自然，能够准确传达角色的内心世界",
                    "眼神戏特别出色，能够通过眼神传递复杂的情感变化",
                    "整体表演收放自如，既有爆发力又有细腻的情感表达"
                ],
                "观众共鸣点": [
                    "角色经历引发观众强烈共情，许多观众表示感同身受",
                    "情感表达真实可信，角色的喜怒哀乐都能打动人心",
                    "角色命运牵动人心，观众对角色命运的关注度很高",
                    "角色的成长历程让观众产生代入感，仿佛亲身经历",
                    "角色的坚持和勇气激励了许多观众，产生了积极影响",
                    "角色的困境和选择引发了广泛的社会讨论和思考",
                    "通过角色的经历，观众能够反思自身的生活和价值观"
                ],
                "角色成长轨迹": [
                    "角色经历了显著的成长和变化，从开始到结束判若两人",
                    "性格发展合理且有说服力，每个转变都有充分的铺垫",
                    "最终命运与角色设定高度契合，结局令人信服",
                    "成长过程中的每个阶段都有明显的标志性事件",
                    "角色的价值观和世界观随着经历不断调整和成熟",
                    "与其他角色的关系变化也反映了角色的成长轨迹",
                    "角色的成长不仅体现在外在行为，更体现在内心的成熟"
                ],
                "演员简介": [
                    f"**{actor_name}**是实力派演员，在《怪奇物语》中成功塑造了**{selected_character}**这一经典角色",
                    f"**{actor_name}**的表演细腻入微，对角色的理解和诠释非常到位",
                    f"通过**{selected_character}**这一角色，**{actor_name}**展现了出色的演技实力和角色塑造能力",
                    f"**{actor_name}**在演艺圈拥有良好的口碑，是备受观众喜爱的演员之一",
                    f"**演员简介**: {character_data['actor_bio']}",
                    f"**代表作品**: {', '.join(famous_works)}",
                    f"**演艺特点**: 擅长演绎复杂角色，表演富有层次感和情感深度",
                    f"**角色突破**: 在《怪奇物语》中展现了与以往作品不同的表演风格",
                    f"**观众评价**: 演技精湛，角色塑造深入人心，备受好评",
                    f"**专业素养**: 对角色的准备工作充分，能够深入理解角色内心",
                    f"**行业地位**: 在演艺圈拥有重要地位，是公认的实力派演员"
                ],
                "代表作品分析": [
                    f"**{actor_name}**的代表作品包括：**{famous_works[0]}**、**{famous_works[1]}**、**{famous_works[2]}**",
                    f"在**{famous_works[0]}**中，**{actor_name}**展现了出色的演技和角色塑造能力",
                    f"**{famous_works[1]}**是**{actor_name}**的另一部重要作品，展现了其多样化的表演风格",
                    f"通过**{famous_works[2]}**，**{actor_name}**进一步巩固了在演艺圈的地位",
                    f"**{famous_works[0]}**中的表现获得了观众和评论界的一致好评",
                    f"**{famous_works[1]}**展现了**{actor_name}**在不同类型作品中的适应能力",
                    f"**{famous_works[2]}**的成功证明了**{actor_name}**的票房号召力和演技实力",
                    f"这三部作品共同构成了**{actor_name}**演艺生涯的重要里程碑"
                ],
                "演艺生涯发展": [
                    f"**{actor_name}**的演艺生涯发展稳健，作品质量普遍较高",
                    f"从早期作品到《怪奇物语》，**{actor_name}**的演技不断进步和成熟",
                    f"**{actor_name}**在角色选择上展现了良好的眼光和判断力",
                    f"未来**{actor_name}**有望在演艺事业上取得更大的成就",
                    f"职业生涯中的每个阶段都有代表性的作品和角色",
                    f"**{actor_name}**不断挑战自我，尝试不同类型的角色和作品",
                    f"在演艺圈的地位和影响力随着作品的积累不断提升",
                    f"未来的发展前景广阔，有望成为演艺界的代表性人物"
                ]
            }
            
            # 显示演员照片和评论布局
            if analysis_type in ["演员简介", "代表作品分析", "演艺生涯发展"]:
                # 第一行：图片和评论并排
                col_img, col_comments = st.columns([1, 2])
                
                with col_img:
                    # 调整图片大小，使长边与四条文本框宽度一致
                    st.image(character_data['actor_photo_url'], width=300, caption=f"演员: {actor_name}")
                
                with col_comments:
                    st.success(f"### 🎯 AI对**{selected_character}**的{analysis_type}")
                    
                    # 显示前4条评论
                    points_to_show = analysis_results[analysis_type][:4]
                    for point in points_to_show:
                        st.info(f"✨ {point}")
                
                # 如果有更多评论，在第二行显示
                remaining_points = analysis_results[analysis_type][4:]
                if remaining_points:
                    st.markdown("---")
                    st.markdown("### 📝 更多分析")
                    for point in remaining_points:
                        st.info(f"✨ {point}")
            else:
                # 非演员相关分析的布局
                st.success(f"### 🎯 AI对**{selected_character}**的{analysis_type}")
                
                # 显示角色图片和评论
                col_img, col_comments = st.columns([1, 2])
                
                with col_img:
                    st.image(character_data['image_url'], width=300, caption=selected_character)
                
                with col_comments:
                    # 显示前4条评论
                    points_to_show = analysis_results[analysis_type][:4]
                    for point in points_to_show:
                        st.info(f"✨ {point}")
                
                # 如果有更多评论，在第二行显示
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