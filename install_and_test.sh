#!/bin/bash

echo "佛學問答精選系統安裝和測試腳本"
echo "=================================="

# 檢查Python版本
echo "檢查Python版本..."
python3 --version

# 安裝依賴包
echo "安裝依賴包..."
pip3 install -r requirements.txt

# 檢查安裝是否成功
echo "測試模塊載入..."
python3 -c "
try:
    import configparser
    import openpyxl
    print('✅ 基本模塊載入成功')
except ImportError as e:
    print(f'❌ 基本模塊載入失敗: {e}')

try:
    import openai
    print('✅ OpenAI模塊載入成功')
except ImportError as e:
    print(f'❌ OpenAI模塊載入失敗: {e}')
"

echo ""
echo "安裝完成！"
echo ""
echo "下一步："
echo "1. 編輯 config.ini 設置您的 OpenAI API Key 或 ChatMock 服務器"
echo "2. 根據需要調整 prompt_template.txt"
echo "3. 選擇評分模式：指定行號模式或過濾結果模式"
echo "4. 運行: python3 qa_curator.py"
echo ""
echo "使用說明："
echo "- 使用OpenAI API: python3 qa_curator.py --api-key YOUR_API_KEY --api-type openai"
echo "- 使用ChatMock: python3 qa_curator.py --api-type chatmock"
echo "- 將結果寫入Excel: python3 results_to_excel.py results_file.json"
echo ""
echo "評分模式："
echo "- 指定行號模式：設置 use_filter_mode = false，配置 start_row 和 end_row"
echo "- 過濾結果模式：設置 use_filter_mode = true，配置過濾條件和評分範圍"
echo ""
echo "測試系統："
echo "- 運行測試: python3 test_curator.py"
echo "- 創建示例: python3 example_usage.py"
echo "- 安裝和測試: bash install_and_test.sh"
