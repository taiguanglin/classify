# 佛學問答精選系統

## 📋 系統概述

這個系統可以自動對"答疑汇总"工作表中的佛學問答進行精選評分，使用AI模型根據"廣度"和"深度"兩個維度進行評分，並提供詳細的評論分析。**評選重點放在回答內容的質量上**，問題主要用於理解背景和上下文。

系統支持兩種評分模式：
- **指定行號模式**：直接指定Excel行號範圍進行評分
- **過濾結果模式**：根據過濾條件篩選問答，然後對篩選結果進行評分

## 🚀 快速開始

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 配置設定

#### 2.1 設置API

**使用OpenAI API：**
```bash
export OPENAI_API_KEY=你的_OPENAI_API_KEY
```

**使用ChatMock（推薦）：**
```bash
# 啟動ChatMock服務器
# 參考：https://github.com/RayBytes/ChatMock
```

#### 2.2 選擇評分模式

**模式1：指定行號模式（傳統模式）**
```ini
[processing]
use_filter_mode = false
start_row = 660
end_row = 660
```

**模式2：過濾結果模式（新功能）**
```ini
[processing]
use_filter_mode = true

[filter]
start_index = 0      # 從第一條過濾結果開始
end_index = 2        # 評分前3條過濾結果
question_keywords = 佛法,修行  # 問題包含關鍵詞
```

#### 2.3 調整配置參數

根據需要修改 `config.ini` 中的設定：

- **Excel文件設定**: 文件路徑、工作表名稱、列位置
- **輸出列設定**: 評分結果要寫入的列位置
- **評分模式**: 選擇使用傳統模式還是過濾模式
- **過濾條件**: 關鍵詞、行號範圍等過濾條件

### 3. 自定義Prompt

編輯 `prompt_template.txt` 文件來調整評分標準和要求。

### 4. 運行程序

```bash
# 使用OpenAI API
python3 qa_curator.py --api-key YOUR_API_KEY --api-type openai

# 使用ChatMock
python3 qa_curator.py --api-type chatmock

# 將結果寫入Excel
python3 results_to_excel.py results_file.json
```

## 📊 配置說明

### config.ini 重要參數

```ini
[excel]
file_path = 20250825.xlsx        # Excel文件名
sheet_name = 答疑汇总            # 工作表名稱
question_column = 18             # 問題所在列（第R列）
answer_column = 19               # 答案所在列（第S列）

[output]
breadth_score_column = 24        # 廣度評分寫入列（第X列）
depth_score_column = 25          # 深度評分寫入列（第Y列）
overall_score_column = 26        # 綜合評分寫入列（第Z列）
breadth_comment_column = 27      # 廣度評論寫入列（第AA列）
depth_comment_column = 28        # 深度評論寫入列（第AB列）
overall_comment_column = 29      # 總體評價寫入列（第AC列）

[processing]
use_filter_mode = false          # 評分模式選擇
start_row = 660                  # 開始處理的行（傳統模式）
end_row = 660                   # 結束行（傳統模式）

[filter]
start_index = 0                  # 過濾結果評分起始索引
end_index = 0                   # 過濾結果評分結束索引
question_keywords = 佛法,修行    # 問題關鍵詞過濾
answer_keywords =                # 答案關鍵詞過濾
row_range_start =                # 過濾行號範圍起始
row_range_end =                  # 過濾行號範圍結束
```

## 🔍 評分模式詳解

### 📋 模式1：指定行號模式（use_filter_mode = false）

**適用場景**：知道具體要評分的Excel行號
**配置方式**：設置 `start_row` 和 `end_row`
**工作流程**：直接對指定行號範圍的問答進行評分

```ini
[processing]
use_filter_mode = false
start_row = 660
end_row = 670
```

### 🔍 模式2：過濾結果模式（use_filter_mode = true）

**適用場景**：需要根據內容條件篩選問答
**配置方式**：在 `[filter]` 章節配置過濾條件
**工作流程**：先過濾，再對過濾結果進行評分

#### 過濾條件類型

1. **列值過濾（基於Excel列F、G、H的值）**
   ```ini
   [filter]
   column_f_value = I级      # 第F列（第6列）必須匹配的值
   column_g_value = 禪修     # 第G列（第7列）必須匹配的值
   column_h_value = 初級     # 第H列（第8列）必須匹配的值
   ```
   
   **說明**：
   - Column F（第6列）：通常包含I级、II级、III级等分類
   - Column G（第7列）：通常包含禪修、義理、修行等主題
   - Column H（第8列）：通常包含初級、中級、高級等難度
   - **注意：至少需要設置一個列值作為過濾條件**
   - 如果某個值為空，則該列不作為過濾條件

2. **組合過濾**
   ```ini
   [filter]
   column_f_value = I级
   column_g_value = 禪修
   row_range_start = 200
   row_range_end = 800
   ```

#### 評分範圍設定

```ini
[filter]
# 只評分第一條過濾結果（預設）
start_index = 0
end_index = 0

# 評分前3條過濾結果
start_index = 0
end_index = 2

# 評分第2-4條過濾結果
start_index = 1
end_index = 3
```

## 📊 Excel輸出模式

系統支持兩種Excel輸出模式，可根據需要在 `config.ini` 中配置：

### 📋 模式1：精簡模式（output_mode = compact）

**適用場景**：只需要評分結果，不需要保持原有Excel結構
**特點**：
- 只包含需要的行（標題行 + 評分行）
- 文件大小小，加載速度快
- 結構清晰，便於查看評分結果
- 自動調整列寬和行高

**配置**：
```ini
[excel_output]
output_mode = compact
include_title_row = true
include_empty_rows = false
```

### 📋 模式2：完整模式（output_mode = full）

**適用場景**：需要保持原有Excel結構和格式
**特點**：
- 保持原有Excel文件的完整結構
- 包含所有原始數據
- 只修改評分相關列
- 保持原有格式和樣式

**配置**：
```ini
[excel_output]
output_mode = full
preserve_formatting = true
preserve_structure = true
```

## 🎯 評分標準

系統根據以下標準進行評分：

### 廣度評分 (0-100分)
廣度評估回答內容所涵蓋的TaiGuangLin禪師教法概念和領域的範圍。

- **0-20分**：基礎名詞提及
- **21-40分**：初步概念了解
- **41-60分**：多領域涉獵
- **61-80分**：廣泛綜合認知
- **81-100分**：全面且系統的整合

### 深度評分 (0-100分)
深度評估回答內容對TaiGuangLin禪師教法義理的闡述是否透徹，是否能解釋概念間的內在邏輯、實踐細節及其獨特見解。

- **0-20分**：詞彙層面
- **21-40分**：淺層解釋
- **41-60分**：細節與初步邏輯
- **61-80分**：深入分析與關聯
- **81-100分**：洞悉底層原理與融會貫通

### 綜合評分
- 綜合評分 = (廣度評分 + 深度評分) ÷ 2
- 四捨五入到整數

## 🔧 功能特點

### ✅ 智能評分
- 基於廣度和深度兩個維度的客觀評分
- 自動計算綜合評分
- 提供詳細的評分依據和評論

### ✅ 雙模式支持
- **指定行號模式**：直接指定行號範圍
- **過濾結果模式**：智能篩選後評分
- 靈活切換，滿足不同使用場景

### ✅ 列值過濾
- **基於Excel列F、G、H的值進行精確過濾**
- 支持I级、II级、III级等分類過濾
- 支持禪修、義理、修行等主題過濾
- 支持初級、中級、高級等難度過濾
- **專注於列值精確匹配，過濾邏輯清晰簡單**

### ✅ 雙輸出模式
- **精簡模式**：只包含評分結果，文件小、加載快
- **完整模式**：保持原有結構，包含所有數據
- 根據需求靈活選擇輸出方式

### ✅ 重點在回答
- **評選重點放在回答內容的質量上**
- 問題主要用於理解背景和上下文
- 確保評分的客觀性和準確性

### ✅ 摘要生成
- 自動生成問題摘要（50字以內）
- 自動生成回答摘要（100字以內）
- 摘要以comment形式附加到Excel單元格上

### ✅ 安全可靠
- 自動跳過已評分的條目
- 定期保存避免數據丟失
- 詳細的日誌記錄

### ✅ 可配置
- 彈性的配置文件
- 可自定義的評分標準
- 可調整的過濾條件和評分範圍
- 可選擇的Excel輸出模式

### ✅ 批量處理
- 支持大量數據處理
- API調用頻率控制
- 中斷恢復機制

## 📝 使用注意事項

1. **API費用**: 使用OpenAI API會產生費用，建議先小範圍測試
2. **處理時間**: 大量數據需要較長時間，建議分批處理
3. **備份數據**: 處理前請備份原始Excel文件
4. **網絡穩定**: 確保網絡連接穩定，避免API調用中斷
5. **過濾條件**: 過濾條件過於嚴格可能導致沒有結果

## 🛠️ 進階使用

### 只處理特定範圍

```python
curator = BuddhistQACurator()
curator.process_batch(start_row=660, end_row=670)  # 只處理第660-670行
```

### 使用過濾模式

```ini
# 啟用過濾模式
[processing]
use_filter_mode = true

# 配置過濾條件
[filter]
question_keywords = 佛法,修行
start_index = 0
end_index = 4  # 評分前5條過濾結果
```

### 檢查日誌

系統會自動生成日誌文件：`qa_curation.log`

### 自定義評分標準

如需調整評分標準，請修改 `prompt_template.txt` 中的評分說明。

### 摘要功能

系統會自動生成問題和回答摘要，並以comment形式附加到Excel單元格上，開頭標註"大模型摘要:"。

## 🔍 故障排除

### 常見問題

1. **API Key錯誤**: 檢查環境變量或命令行參數中的API Key是否正確
2. **文件找不到**: 確認Excel文件路徑和工作表名稱
3. **列位置錯誤**: 檢查配置文件中的列號設定
4. **權限問題**: 確保對Excel文件有讀寫權限
5. **過濾無結果**: 檢查過濾條件是否過於嚴格

### 測試建議

1. 先設定小範圍測試（如前10行）
2. 檢查輸出結果是否符合預期
3. 確認配置無誤後再處理全部數據
4. 使用過濾模式時，先測試過濾條件是否有效

## 📄 文件說明

- `qa_curator.py`: 主程序（精選評分器，支持雙模式）
- `results_to_excel.py`: 結果寫入Excel工具
- `config.ini`: 配置文件
- `config_filter_example.ini`: 過濾模式配置示例
- `prompt_template.txt`: 評分標準模板
- `test_curator.py`: 系統測試腳本
- `example_usage.py`: 使用示例腳本
- `install_and_test.sh`: 安裝測試腳本
- `requirements.txt`: Python依賴包
- `README.md`: 使用說明

## 🔄 系統架構

```
Excel文件 → 精選評分器 → JSON結果 → Excel寫入器 → 最終Excel文件
    ↓              ↓           ↓           ↓
  問答內容    AI評分分析    評分結果    格式化輸出+摘要comment
```

**評分器支持兩種模式：**
- 指定行號模式：直接處理指定行
- 過濾結果模式：先過濾，再處理過濾結果

## 💡 使用場景

- **佛學教育**: 篩選高質量的問答內容用於教學
- **內容篩選**: 從大量問答中找出最有價值的內容
- **質量評估**: 對佛學問答進行客觀的質量評估
- **學習指導**: 幫助學習者識別高質量的學習材料
- **智能篩選**: 根據關鍵詞或條件自動篩選相關問答

## 🧪 測試和示例

### 運行測試
```bash
python3 test_curator.py
```

### 創建示例
```bash
python3 example_usage.py
```

### 安裝和測試
```bash
bash install_and_test.sh
```

### 過濾模式示例
```bash
# 使用過濾模式配置
cp config_filter_example.ini config.ini
python3 qa_curator.py --api-type chatmock
```
