import json
import os
import requests
import re

# 文件列表
json_files = {
    'part_1.json': 'book_1_localized.md',
    'part_2.json': 'book_2_localized.md',
    'part_3.json': 'book_3_localized.md'
}

# 创建一个保存图片的目录
image_dir = 'images'
os.makedirs(image_dir, exist_ok=True)

def download_image(url, save_dir):
    # 获取图片的文件名
    filename = url.split('/')[-1]
    filepath = os.path.join(save_dir, filename)
    
    # 下载图片
    response = requests.get(url)
    if response.status_code == 200:
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return filepath
    else:
        print(f"Failed to download image: {url}")
        return None

# 查找并替换 markdown 中的图片链接
def localize_images(markdown_content, image_dir):
    # 找到所有的图片链接
    image_urls = re.findall(r'!\[\]\((https://[^\)]+)\)', markdown_content)
    
    # 替换图片链接
    for url in image_urls:
        local_path = download_image(url, image_dir)
        if local_path:
            # 使用相对路径更新 Markdown 中的链接
            markdown_content = markdown_content.replace(url, local_path)
    
    return markdown_content

# 处理每本书的 JSON 文件
for json_file, output_markdown_file in json_files.items():
    # 读取 JSON 文件
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 提取并处理 markdown 内容
    markdown_content = data.get('markdown', '')
    localized_markdown = localize_images(markdown_content, image_dir)
    
    # 将每本书的 Markdown 内容保存到单独的文件
    with open(output_markdown_file, 'w', encoding='utf-8') as f:
        f.write(localized_markdown)

    print(f"Markdown 文件已生成并图片本地化完成，文件名为: {output_markdown_file}")
