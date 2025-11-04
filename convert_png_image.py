import base64
import os

# 读取cheese.png图片并转换为base64编码
with open('cheese.png', 'rb') as img_file:
    img_data = base64.b64encode(img_file.read()).decode('utf-8')
    
print(f"PNG图片base64编码获取成功，长度: {len(img_data)} 字符")

# 创建CSS样式代码
css_code = f"""
/* 动漫奶酪风格背景 - 使用base64编码的cheese.png图片 */
.stApp {{
    background-image: url('data:image/png;base64,{img_data}');
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
    background-attachment: fixed;
}}
"""

print("CSS样式代码已生成")
print("前100个字符:", css_code[:100])

# 保存到文件
with open('background_png_css.txt', 'w', encoding='utf-8') as f:
    f.write(css_code)

print("CSS样式已保存到 background_png_css.txt 文件")
print("请将这段CSS代码替换到go.py文件的相应位置")