import base64

# 读取桌面上的cheese.png图片并转换为base64
with open('C:\\Users\\17347\\Desktop\\cheese.png', 'rb') as f:
    img_data = f.read()
    base64_data = base64.b64encode(img_data).decode('utf-8')

print(f'图片base64编码长度: {len(base64_data)}')

# 读取go.py文件
with open('C:\\Users\\17347\\Desktop\\go.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 查找并替换背景图片的base64编码
# 找到背景图片的起始位置
start_marker = "background-image: url('data:image/png;base64,"
start_pos = content.find(start_marker)

if start_pos != -1:
    # 找到base64编码的结束位置（单引号）
    end_pos = content.find("'", start_pos + len(start_marker))
    
    if end_pos != -1:
        # 替换base64编码部分
        old_bg = content[start_pos:end_pos + 1]
        new_bg = f"background-image: url('data:image/png;base64,{base64_data}'"
        
        content = content.replace(old_bg, new_bg)
        
        # 写回文件
        with open('C:\\Users\\17347\\Desktop\\go.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print('背景图片已成功更新为桌面上的cheese.png')
        print('注释已更新为：使用桌面上的cheese.png图片')
    else:
        print('未找到base64编码的结束位置')
else:
    print('未找到背景图片的起始位置')