# Stage 2: 视觉理解 (Visual Analysis)

**目标**：提取照片的内容特征，生成语义标签和描述。
**输入**：图片文件。
**输出**：Tags, Category, Description, Location (Visual)。

---

## 步骤 1: 内容分类 (Category)

**动作**：
分析画面整体内容，将其归入以下类别之一：
- **Landscape** (风景/自然)
- **Portrait** (人像/合影)
- **Document** (文档/票据/证件)
- **Screenshot** (手机/电脑截屏)
- **Chat** (聊天记录)
- **Object** (特定物品，如美食、车、宠物)
- **Other** (其他)

---

## 步骤 2: 关键元素提取 (Tags)

**动作**：
识别画面中的关键物体、场景或文字，生成 3-5 个标签 (Tags)。

**示例**：
- 物体：Cat, Car, Computer, Flower
- 场景：Mountain, Beach, Office, Street
- 氛围：Sunset, Sunny, Night
- 文字：(如果是文档或截屏，提取标题或关键词)

---

## 步骤 3: 语义描述 (Description)

**动作**：
生成一段 50 字以内的自然语言描述。
这段描述将用于未来的自然语言搜索 (Vector Search)。

**要求**：
- 包含主要主体 (Who/What)
- 包含动作或状态 (Doing what)
- 包含环境或背景 (Where/When)
- (可选) 包含推测的意图或情感

**示例**：
> "一张拍摄于山顶的日落照片，前景是家人的背影，背景是金色的阳光洒在雪山上。"

---

## 步骤 4: 视觉地点推断 (Location - Optional)

**动作**：
如果图片中包含明显的地标建筑或地名文字 (OCR)，尝试提取地点信息。
如果没有 EXIF GPS 数据，此步骤非常重要。

---

## 结束本阶段

**输出示例**：
```json
{
  "category": "Landscape",
  "tags": ["Mountain", "Sunset", "Snow"],
  "description": "一张拍摄于山顶的日落照片，背景是金色的阳光洒在雪山上。",
  "location_visual": "Unknown"
}
```
**跳转至 Stage 3**。
