#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
佛學問答精選器使用示例
展示如何使用精選器系統進行問答評分，包括新的過濾模式
"""

import json
from datetime import datetime

def create_sample_results():
    """創建示例結果文件"""
    print("📝 創建示例精選評分結果...")
    
    # 示例數據
    sample_data = {
        "metadata": {
            "source_file": "20250825.xlsx",
            "sheet_name": "答疑汇总",
            "llm_model": "chat-gpt-5",
            "processing_start_time": datetime.now().isoformat(),
            "processing_mode": "filter_mode",
            "total_processed": 2,
            "total_success": 2,
            "total_failed": 0
        },
        "results": {
            "660": {
                "row_number": 660,
                "question": "什麼是佛法？",
                "answer": "佛法是指佛陀的教法，包括四聖諦、八正道等核心教義。佛法涵蓋了宇宙人生的根本真理，指導眾生離苦得樂，最終達到涅槃解脫。",
                "breadth_score": "85",
                "depth_score": "90",
                "overall_score": "88",
                "breadth_comment": "此問答涉及佛法的基本概念和核心教義，涵蓋了義理、修行等多個維度，廣度較好。",
                "depth_comment": "對佛法的解釋深入淺出，準確闡述了四聖諦、八正道等核心概念，理論深度很高。",
                "overall_comment": "這是一個高質量的佛學問答，既有廣度又有深度，對學習者很有幫助。",
                "question_summary": "詢問佛法的基本定義和內涵",
                "answer_summary": "詳細闡述佛法的核心教義，包括四聖諦、八正道等，強調其指導眾生解脫的價值。",
                "status": "success",
                "processed_time": datetime.now().isoformat()
            },
            "661": {
                "row_number": 661,
                "question": "如何修行？",
                "answer": "修行要從持戒開始，然後修定，最後修慧。具體包括打坐、念佛、誦經等方法。",
                "breadth_score": "75",
                "depth_score": "70",
                "overall_score": "73",
                "breadth_comment": "涉及修行的基本方法，包括戒定慧三學，有一定的廣度。",
                "depth_comment": "對修行方法有基本說明，但缺乏深入闡述，深度一般。",
                "overall_comment": "提供了修行的基本框架，適合初學者參考。",
                "question_summary": "詢問修行的具體方法和步驟",
                "answer_summary": "說明修行的三個階段：持戒、修定、修慧，並列舉具體的修行方法。",
                "status": "success",
                "processed_time": datetime.now().isoformat()
            }
        }
    }
    
    # 保存示例結果
    filename = "sample_curation_results.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 示例結果已保存到: {filename}")
    return filename

def show_usage_instructions():
    """顯示使用說明"""
    print("\n📖 佛學問答精選器使用說明")
    print("=" * 70)
    
    print("\n🎯 系統功能：")
    print("- 對佛學問答進行廣度和深度評分（0-100分）")
    print("- 自動計算綜合評分")
    print("- 提供詳細的評分評論")
    print("- 生成問題和回答摘要")
    print("- 支持兩種評分模式：指定行號模式和過濾結果模式")
    print("- 支持兩種Excel輸出模式：精簡模式和完整模式")
    print("- 支持批量處理Excel文件")
    
    print("\n🚀 快速開始：")
    print("1. 使用ChatMock（推薦）：")
    print("   python3 qa_curator.py --api-type chatmock")
    print("")
    print("2. 使用OpenAI API：")
    print("   export OPENAI_API_KEY=YOUR_API_KEY")
    print("   python3 qa_curator.py --api-type openai")
    print("")
    print("3. 將結果寫入Excel：")
    print("   python3 results_to_excel.py results_file.json")
    
    print("\n⚙️  配置說明：")
    print("- 編輯 config.ini 調整Excel文件路徑和列位置")
    print("- 編輯 prompt_template.txt 調整評分標準")
    print("- 設置 use_filter_mode 選擇評分模式")
    print("- 傳統模式：設置 start_row 和 end_row 控制處理範圍")
    print("- 過濾模式：設置過濾條件和評分範圍")
    print("- Excel輸出：設置 output_mode 選擇輸出模式")
    
    print("\n🔍 評分模式詳解：")
    print("\n📋 模式1：指定行號模式（use_filter_mode = false）")
    print("- 直接指定Excel行號範圍進行評分")
    print("- 適用於：知道具體行號的情況")
    print("- 配置：start_row, end_row")
    
    print("\n🔍 模式2：過濾結果模式（use_filter_mode = true）")
    print("- 根據過濾條件篩選問答，然後對篩選結果進行評分")
    print("- 適用於：需要根據內容條件篩選的情況")
    print("- 過濾條件：列值、關鍵詞、行號範圍等")
    print("- 評分範圍：可設定評分前幾條過濾結果")
    print("- 配置：filter章節的各種過濾條件")
    
    print("\n🔧 過濾條件類型：")
    print("\n1. 列值過濾（基於Excel列F、G、H的值）")
    print("   column_f_value: 第F列（第6列）必須匹配的值")
    print("   column_g_value: 第G列（第7列）必須匹配的值")
    print("   column_h_value: 第H列（第8列）必須匹配的值")
    print("   例如：column_f_value = I级, column_g_value = 禪修")
    print("   注意：至少需要設置一個列值作為過濾條件")
    
    print("\n📊 Excel輸出模式：")
    print("\n📋 模式1：精簡模式（output_mode = compact）")
    print("- 只生成包含JSON條目的Excel文件")
    print("- 適用於：只需要評分結果的情況")
    print("- 特點：文件小、加載快、結構清晰")
    
    print("\n📋 模式2：完整模式（output_mode = full）")
    print("- 輸出完整Excel文件，包含JSON條目的修改")
    print("- 適用於：需要保持原有Excel結構的情況")
    print("- 特點：保持原有格式、包含所有數據")
    
    print("\n📊 輸出格式：")
    print("- 廣度評分：反映回答涉及的佛學領域範圍")
    print("- 深度評分：反映回答的理論深度")
    print("- 綜合評分：(廣度+深度)/2")
    print("- 廣度評論：具體說明廣度評分依據")
    print("- 深度評論：具體說明深度評分依據")
    print("- 總體評價：綜合評價和特點總結")
    print("- 問題摘要：提取問題的核心重點")
    print("- 回答摘要：提取回答的核心重點和主要觀點")
    
    print("\n💡 評選重點：")
    print("- 評選重點放在回答內容的質量上")
    print("- 問題主要用於理解背景和上下文")
    print("- 摘要以comment形式附加到問題和答案單元格上")
    
    print("\n🔧 配置示例：")
    print("\n# 列值過濾模式")
    print("[processing]")
    print("use_filter_mode = true")
    print("")
    print("[filter]")
    print("column_f_value = I级")
    print("column_g_value = 禪修")
    print("column_h_value = 初級")
    print("start_index = 0")
    print("end_index = 2")
    
    print("\n# Excel輸出模式")
    print("[excel_output]")
    print("output_mode = full  # 或 compact")
    
    print("\n# 只評分第一條過濾結果（預設）")
    print("[filter]")
    print("start_index = 0")
    print("end_index = 0")
    
    print("\n# 評分前3條過濾結果")
    print("[filter]")
    print("start_index = 0")
    print("end_index = 2")
    
    print("\n# 評分第2-4條過濾結果")
    print("[filter]")
    print("start_index = 1")
    print("end_index = 3")

def main():
    """主函數"""
    print("🚀 佛學問答精選器使用示例（含過濾模式）")
    print("=" * 60)
    
    # 創建示例結果
    sample_file = create_sample_results()
    
    # 顯示使用說明
    show_usage_instructions()
    
    print(f"\n💡 提示：")
    print(f"- 示例結果文件: {sample_file}")
    print(f"- 可以運行: python3 results_to_excel.py {sample_file}")
    print(f"- 來測試Excel寫入功能")
    
    print(f"\n✅ 示例創建完成！")

if __name__ == "__main__":
    main()
