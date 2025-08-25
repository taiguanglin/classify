# 佛學問答精選系統

## 📋 系統概述

這個系統可以自動對"答疑汇总"工作表中的佛學問答進行精選評分，使用AI模型根據"廣度"和"深度"兩個維度進行評分，並提供詳細的評論分析。**評選重點放在回答內容的質量上**，問題主要用於理解背景和上下文。

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

#### 2.2 調整配置參數

根據需要修改 `config.ini` 中的設定：

- **Excel文件設定**: 文件路徑、工作表名稱、列位置
- **輸出列設定**: 評分結果要寫入的列位置
- **處理範圍**: 要處理的行數範圍

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
start_row = 660                  # 開始處理的行
end_row = 660                   # 結束行（0表示處理到最後）
```

## 🎯 評分標準

系統根據以下標準進行評分：

### 廣度評分 (0-100分)
- **90-100分**：涵蓋多個佛學領域，涉及義理、修行、生活等多個維度
- **80-89分**：涉及2-3個主要佛學領域，有一定的廣度
- **70-79分**：主要涉及1-2個領域，有一定的廣度但相對集中
- **60-69分**：主要聚焦在單一領域，廣度有限
- **50-59分**：內容較為狹窄，缺乏廣度
- **0-49分**：內容過於單一或偏頗，廣度不足

### 深度評分 (0-100分)
- **90-100分**：深入探討佛學核心概念，有獨到見解，理論深度極高
- **80-89分**：對佛學概念有較深的理解和闡述，有一定的理論深度
- **70-79分**：對佛學概念有基本理解，有一定的深度
- **60-69分**：對佛學概念有初步理解，深度一般
- **50-59分**：對佛學概念理解較淺，深度不足
- **0-49分**：對佛學概念理解很淺，缺乏深度

### 綜合評分
- 綜合評分 = (廣度評分 + 深度評分) ÷ 2
- 四捨五入到整數

## 🔧 功能特點

### ✅ 智能評分
- 基於廣度和深度兩個維度的客觀評分
- 自動計算綜合評分
- 提供詳細的評分依據和評論

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
- 可調整的處理範圍

### ✅ 批量處理
- 支持大量數據處理
- API調用頻率控制
- 中斷恢復機制

## 📝 使用注意事項

1. **API費用**: 使用OpenAI API會產生費用，建議先小範圍測試
2. **處理時間**: 大量數據需要較長時間，建議分批處理
3. **備份數據**: 處理前請備份原始Excel文件
4. **網絡穩定**: 確保網絡連接穩定，避免API調用中斷

## 🛠️ 進階使用

### 只處理特定範圍

```python
curator = BuddhistQACurator()
curator.process_batch(start_row=660, end_row=670)  # 只處理第660-670行
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

### 測試建議

1. 先設定小範圍測試（如前10行）
2. 檢查輸出結果是否符合預期
3. 確認配置無誤後再處理全部數據

## 📄 文件說明

- `qa_curator.py`: 主程序（精選評分器）
- `results_to_excel.py`: 結果寫入Excel工具
- `config.ini`: 配置文件
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

## 💡 使用場景

- **佛學教育**: 篩選高質量的問答內容用於教學
- **內容篩選**: 從大量問答中找出最有價值的內容
- **質量評估**: 對佛學問答進行客觀的質量評估
- **學習指導**: 幫助學習者識別高質量的學習材料

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
