# 📸 AI Photo Organizer Agent
> 智能照片整理助手：利用多模态大模型，自动识别照片内容、重命名并打标签。

## 📖 项目简介
作为一个摄影/生活记录爱好者，你是否也面临照片文件名混乱（如 `IMG_2839.jpg`）、难以检索的痛点？

本项目是一个基于 LLM (如Qwen-VL-Max) 的智能体脚本。它能“看懂”你的照片，提取关键信息（时间、场景、物品），并自动完成以下工作：
*   **智能重命名**：将文件名改为易读格式（如 `20250519_海边_喝椰子.jpg`）。
*   **元数据写入**：将 AI 生成的详细描述和标签写入照片的 EXIF/IPTC 属性中。
*   **本地检索增强**：整理后，你可以直接在 Windows/Mac 搜索框中输入“海边”或“办公桌”直接找到照片。

## ✨ 核心功能 (Features)
- [x] **视觉识别**：自动识别图片主体、场景、文字。
- [x] **中文描述**：生成符合人类直觉的中文文件命名。
- [x] **系统级搜索**：通过写入 Windows 属性标签，支持系统原生自然语言搜索。
- [x] **自动化处理**：一键处理整个文件夹。

## 🛠️ 快速开始

### 1. 环境准备
确保你的电脑安装了 Python 3.8+。

~~~bash
# 安装依赖库
pip install -r requirements.txt
~~~

### 2. 配置 API Key
本项目使用 OpenAI 格式的 API（支持 DeepSeek, 阿里通义, OpenAI 等）。

1. 将项目中的 `.env.example` 文件重命名为 `.env`。
2. 用记事本打开 `.env`，填入你的 API Key：

~~~ini
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_BASE_URL=https://api.deepseek.com  # 如果是用 DeepSeek 或其他模型
~~~

### 3. 运行整理
把需要整理的照片放入 `input_photos` 文件夹（如果没有请新建），然后在 `main.py` 所在的 terminal 运行：

~~~bash
python main.py
~~~

整理好的照片将会出现在 `output_organized` 文件夹中。

---

### 📂 项目结构
*   `main.py`: 智能体主程序
*   `SKILL.md`: 定义 AI 角色的核心 Prompt (Skills)
*   `requirements.txt`: 项目依赖
