# Stage 3: 归档标准化 (Archiving)

**目标**：综合前两步信息，生成标准化的档案记录。
**输入**：Stage 1 的时间信息 + Stage 2 的视觉信息。
**输出**：完整的元数据 JSON 和重命名建议。

---

## 步骤 1: 数据整合

**动作**：
将 `Target Date` (来自 Stage 1) 和 `Visual Info` (来自 Stage 2) 合并。
如果 EXIF 中有 GPS 数据，优先使用 EXIF 地点；否则使用视觉推断的地点。

---

## 步骤 2: 生成重命名建议

**规则**：
文件名必须包含 `Target Date`，格式为 `YYYYMMDD`。
格式：`{Date}_{Location}_{Tags/Keywords}_{OriginalName}`

**逻辑**：
1. **Date**: 使用 `Target Date` 格式化为 `YYYYMMDD`。
2. **Location**: 如果有地点信息，取城市名或地标名 (如 `Beijing`, `Yosemite`)。若无，省略。
3. **Tags**: 取最重要的 1-2 个标签 (如 `Sunset`, `Meeting`)。
4. **Original**: 保留原始文件名的一部分 (如 `IMG8821`) 以防重名。

**示例**：
- 原名: `IMG_8821.JPG`
- 日期: `2023-05-20`
- 地点: `Beijing`
- 标签: `Sunset`
- **建议文件名**: `20230520_Beijing_Sunset_IMG8821.JPG`

---

## 步骤 3: 生成元数据 JSON

**动作**：
填充 `templates/metadata-result.json` 模板。

**字段说明**：
- `analyzed_date`: 最终确定的 Target Date。
- `date_source`: 时间来源 (EXIF/Filename/OCR)。
- `location`: 优先 GPS，其次 Visual 推断。
- `description`: Stage 2 生成的描述。

---

## 结束

**输出**：
展示最终的 JSON 结果，并询问用户：
"是否按照建议的文件名进行重命名？"
