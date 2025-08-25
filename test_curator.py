#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
佛學問答精選器測試腳本
用於測試精選器系統的基本功能
"""

import os
import sys
import json
from datetime import datetime

def test_prompt_template():
    """測試提示詞模板"""
    print("🧪 測試提示詞模板...")
    
    try:
        with open('prompt_template.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 檢查是否包含必要的關鍵詞
        required_keywords = ['廣度評分', '深度評分', '綜合評分', '廣度評論', '深度評論', '總體評價', '問題摘要', '回答摘要']
        missing_keywords = []
        
        for keyword in required_keywords:
            if keyword not in content:
                missing_keywords.append(keyword)
        
        if missing_keywords:
            print(f"❌ 提示詞模板缺少關鍵詞: {', '.join(missing_keywords)}")
            return False
        else:
            print("✅ 提示詞模板檢查通過")
            return True
            
    except Exception as e:
        print(f"❌ 讀取提示詞模板失敗: {e}")
        return False

def test_config_file():
    """測試配置文件"""
    print("🧪 測試配置文件...")
    
    try:
        import configparser
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8')
        
        # 檢查必要的配置項
        required_sections = ['excel', 'output', 'processing']
        missing_sections = []
        
        for section in required_sections:
            if section not in config:
                missing_sections.append(section)
        
        if missing_sections:
            print(f"❌ 配置文件缺少章節: {', '.join(missing_sections)}")
            return False
        
        # 檢查輸出列配置
        output_configs = [
            'breadth_score_column', 'depth_score_column', 'overall_score_column',
            'breadth_comment_column', 'depth_comment_column', 'overall_comment_column'
        ]
        
        missing_configs = []
        for config_name in output_configs:
            if not config.has_option('output', config_name):
                missing_configs.append(config_name)
        
        if missing_configs:
            print(f"❌ 配置文件缺少輸出列配置: {', '.join(missing_configs)}")
            return False
        
        print("✅ 配置文件檢查通過")
        return True
        
    except Exception as e:
        print(f"❌ 配置文件檢查失敗: {e}")
        return False

def test_python_modules():
    """測試Python模塊"""
    print("🧪 測試Python模塊...")
    
    required_modules = [
        'openai', 'openpyxl', 'pandas', 'configparser'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"❌ 缺少Python模塊: {', '.join(missing_modules)}")
        print("請運行: pip install -r requirements.txt")
        return False
    else:
        print("✅ Python模塊檢查通過")
        return True

def test_curator_class():
    """測試精選器類"""
    print("🧪 測試精選器類...")
    
    try:
        # 動態導入精選器類
        sys.path.append('.')
        from qa_curator import BuddhistQACurator
        
        # 創建實例（不初始化API）
        curator = BuddhistQACurator.__new__(BuddhistQACurator)
        
        # 檢查必要的方法
        required_methods = [
            'evaluate_qa_quality', 'parse_evaluation_result', 'process_batch'
        ]
        
        missing_methods = []
        for method in required_methods:
            if not hasattr(curator, method):
                missing_methods.append(method)
        
        if missing_methods:
            print(f"❌ 精選器類缺少方法: {', '.join(missing_methods)}")
            return False
        
        print("✅ 精選器類檢查通過")
        return True
        
    except Exception as e:
        print(f"❌ 精選器類檢查失敗: {e}")
        return False

def test_excel_writer():
    """測試Excel寫入器"""
    print("🧪 測試Excel寫入器...")
    
    try:
        # 動態導入Excel寫入器類
        sys.path.append('.')
        from results_to_excel import CurationResultsWriter
        
        # 創建實例
        writer = CurationResultsWriter.__new__(CurationResultsWriter)
        
        # 檢查必要的方法
        required_methods = [
            'write_curation_result', 'process_results'
        ]
        
        missing_methods = []
        for method in required_methods:
            if not hasattr(writer, method):
                missing_methods.append(method)
        
        if missing_methods:
            print(f"❌ Excel寫入器缺少方法: {', '.join(missing_methods)}")
            return False
        
        print("✅ Excel寫入器檢查通過")
        return True
        
    except Exception as e:
        print(f"❌ Excel寫入器檢查失敗: {e}")
        return False

def test_sample_prompt():
    """測試示例提示詞"""
    print("🧪 測試示例提示詞...")
    
    try:
        with open('prompt_template.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 測試格式化
        test_question = "什麼是佛法？"
        test_answer = "佛法是指佛陀的教法，包括四聖諦、八正道等核心教義。佛法涵蓋了宇宙人生的根本真理，指導眾生離苦得樂，最終達到涅槃解脫。"
        
        formatted_prompt = content.format(title=test_question, answer=test_answer)
        
        if test_question in formatted_prompt and test_answer in formatted_prompt:
            print("✅ 提示詞格式化測試通過")
            return True
        else:
            print("❌ 提示詞格式化測試失敗")
            return False
            
    except Exception as e:
        print(f"❌ 提示詞格式化測試失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("🚀 佛學問答精選器系統測試")
    print("=" * 50)
    
    tests = [
        test_python_modules,
        test_config_file,
        test_prompt_template,
        test_curator_class,
        test_excel_writer,
        test_sample_prompt
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ 測試執行失敗: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 測試結果: {passed}/{total} 通過")
    
    if passed == total:
        print("🎉 所有測試通過！系統準備就緒。")
        print("\n📝 下一步：")
        print("1. 設置API Key或啟動ChatMock服務器")
        print("2. 運行: python3 qa_curator.py --api-type chatmock")
        print("3. 將結果寫入Excel: python3 results_to_excel.py results_file.json")
    else:
        print("⚠️  部分測試失敗，請檢查上述錯誤信息。")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
