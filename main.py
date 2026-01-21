import os
import json
import base64
import shutil
import io  # 用于内存操作
from pathlib import Path
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
from PIL import Image
import piexif
import piexif.helper # <--- 🛠️ 修复报错：必须显式导入 helper

# 1. 加载环境变量
load_dotenv(override=True) 

# 2. 配置文件夹路径
INPUT_FOLDER = "input_photos"  
OUTPUT_FOLDER = "output_organized" 
SKILL_FOLDER = "." 

# 3. 初始化 AI 客户端
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
)

# --- 辅助函数 ---

def encode_image(image_path):
    """
    把图片压缩并转换成 AI 能看懂的编码
    (只压缩发送给 AI 的数据，不修改原图)
    """
    with Image.open(image_path) as img:
        # 1. 兼容性处理
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
            
        # 2. 缩放图片 (限制最大边长 1024)
        max_size = 1024
        if max(img.size) > max_size:
            img.thumbnail((max_size, max_size))
        
        # 3. 保存到内存
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        
        # 4. 转 Base64
        return base64.b64encode(buffer.getvalue()).decode('utf-8')

def read_skill_file(filename):
    path = Path(SKILL_FOLDER) / filename
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def write_metadata_to_image(image_path, json_data):
    """
    把 JSON 中的描述和标签写入图片属性
    """
    try:
        # 1. 准备数据
        description = json_data.get("description", "")
        tags = json_data.get("tags", [])
        keywords = ";".join(tags) 

        # 2. 读取图片的现有 EXIF
        exif_dict = piexif.load(image_path)

        # 3. 设置 Windows 属性
        exif_dict["0th"][piexif.ImageIFD.ImageDescription] = description.encode('utf-8')
        exif_dict["0th"][piexif.ImageIFD.XPComment] = description.encode('utf-16le')
        exif_dict["0th"][piexif.ImageIFD.XPKeywords] = keywords.encode('utf-16le')

        # 4. 保存回去
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, image_path)
        print(f"💾 元数据写入成功（描述+标签）")

    except Exception as e:
        print(f"❌ 写入元数据失败: {e}")
# =======================================

# --- 核心逻辑 ---

def process_image(image_path):
    print(f"🤖 正在思考: {image_path.name} ...")
    
    base64_image = encode_image(image_path)
    
    skill_content = read_skill_file("SKILL.md")
    stage_content = read_skill_file("stages/02-visual-analysis.md")
    
    system_prompt = f"""
    你是一个智能照片整理员。请阅读以下规则：
    {skill_content}
    
    参考分析逻辑：
    {stage_content}
    
    任务：请分析图片，并返回 JSON 格式数据。
    JSON 必须包含: date, location, tags, description, suggested_filename
    注意：date 字段请尽量精确，格式为 YYYY-MM-DD。
    """

    try:
        response = client.chat.completions.create(
            model="qwen-vl-max", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": [
                    {"type": "text", "text": "分析这张图"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                ]}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"❌ 分析出错: {e}")
        return None

def main():
    input_path = Path(INPUT_FOLDER)
    output_path = Path(OUTPUT_FOLDER)
    
    if not input_path.exists():
        input_path.mkdir()
        print(f"⚠️ 请把照片放入 '{INPUT_FOLDER}'")
        return

    output_path.mkdir(exist_ok=True)

    images = [f for f in input_path.iterdir() if f.suffix.lower() in {'.jpg', '.jpeg', '.png', '.webp'}]
    
    if not images:
        print(f"📭 '{INPUT_FOLDER}' 是空的。")
        return

    print(f"🔍 发现 {len(images)} 张照片，开始工作...")

    for img_file in images:
        metadata = process_image(img_file)
        
        if metadata:
            #new_name = metadata.get('suggested_filename', f"processed_{img_file.name}")
            #dest_file = output_path / new_name
                        # 1. 获取文件名主体（不带后缀）
            filename_base = metadata.get('suggested_filename', f"processed_{img_file.stem}")
            
            # 2. 拼接原文件的后缀（比如 .jpg）
            new_name = f"{filename_base}{img_file.suffix}"
            dest_file = output_path / new_name

            # 1. 复制原图 (保留高清)
            shutil.copy2(img_file, dest_file)
            print(f"✅ 整理完毕: {dest_file.name}")
            
            # 2. 保存 JSON
            # 3. 修改图片内部属性（写入中文描述和标签）
            # 注意：我们要把 dest_file 转成字符串，把 metadata 整个传进去
            write_metadata_to_image(str(dest_file), metadata)


    print("\n🎉 全部完成！")

if __name__ == "__main__":
    main()
