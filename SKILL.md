---
name: photo-insight-expert
description: 智能照片档案员 - 提取照片真实时间、地点和核心内容，建立标准化档案。
---

# Photo Insight Expert (智能照片档案员)

## 触发方式

当用户执行以下操作时触发：
- 上传一张或一批图片
- 说 "帮我整理照片"
- 说 "这些照片是什么时候拍的"
- 提到 "归档" 或 "照片整理"

---

## 流程概览

| 阶段 | 名称 | 目标 | 详细文件 |
|---|---|---|---|
| 1 | 时间取证 (Time Forensics) | *核心难点突破* 确定照片的最可信拍摄时间 | `stages/01-time-forensics.md` |
| 2 | 视觉理解 (Visual Analysis) | 提取特征标签、OCR内容、语义描述 | `stages/02-visual-analysis.md` |
| 3 | 归档标准化 (Archiving) | 生成标准化元数据和重命名建议 | `stages/03-archiving.md` |

---

## 调度规则

**如何判断当前阶段：**

1. **进入阶段1** — 用户刚上传图片，尚未提取时间信息。
2. **进入阶段2** — 时间取证完成，已确定 `Target Date`。
3. **进入阶段3** — 视觉分析完成，已提取标签和描述。
4. **结束** — 输出最终的归档建议 JSON。

**每个阶段开始时：**
- 明确当前处理的照片（如果是多张，按顺序处理或并行处理）。
- 读取对应的阶段文件，按照里面的步骤执行。

---

## 文件结构

```
stages/
├── 01-time-forensics.md    # 时间取证的详细步骤
├── 02-visual-analysis.md   # 视觉理解的详细步骤
└── 03-archiving.md         # 归档标准化的详细步骤

templates/
└── metadata-result.json    # 输出结果模板
```

---

## 注意事项

- **准确性优先**：时间是归档的核心，必须按优先级严格取证。
- **隐私保护**：仅处理用户上传的照片，不主动扫描本地文件。
- **容错性**：如果无法确定时间，应标记为 "Unknown" 并提示用户手动确认。

...
## 输出要求
请严格按照 templates/metadata-result.json 的 JSON 格式输出。
- description: 必须使用中文，详细描述画面内容。
- tags: 必须使用中文。
- suggested_filename: 可以使用英文或拼音，方便系统兼容。
...
