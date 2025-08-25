#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
過濾結果緩存系統演示
"""

import os
import sys
from filter_cache import FilterCache

def demo_cache_usage():
    """演示緩存系統的使用"""
    print("🚀 過濾結果緩存系統演示")
    print("=" * 60)
    
    # 創建緩存管理器
    cache = FilterCache(".demo_cache")
    
    # 模擬真實的過濾場景
    scenarios = [
        {
            'name': '佛學義理-起源-娑婆世界',
            'excel_file': '20250825.xlsx',
            'f_value': '01义理',
            'g_value': '04起源',
            'h_value': '05娑婆世界',
            'rows': [82, 86, 292, 332, 405, 463, 464, 466, 481, 492]
        },
        {
            'name': '修行方法-禪修-初級',
            'excel_file': '20250825.xlsx',
            'f_value': '02修行',
            'g_value': '01禪修',
            'h_value': '02中級',
            'rows': [100, 150, 200, 250, 300]
        },
        {
            'name': '經典解讀-心經-般若',
            'excel_file': '20250825.xlsx',
            'f_value': '03經典',
            'g_value': '02心經',
            'h_value': '01般若',
            'rows': [400, 450, 500, 550]
        }
    ]
    
    print("📋 模擬過濾場景:")
    for i, scenario in enumerate(scenarios, 1):
        print(f"  {i}. {scenario['name']}: {scenario['f_value']}-{scenario['g_value']}-{scenario['h_value']}")
    
    print("\n🔄 第一次執行過濾（無緩存）...")
    
    # 模擬第一次過濾，結果會保存到緩存
    for scenario in scenarios:
        print(f"\n📊 過濾: {scenario['name']}")
        
        # 檢查緩存
        cached_result = cache.get_cached_result(
            scenario['excel_file'],
            scenario['f_value'],
            scenario['g_value'],
            scenario['h_value']
        )
        
        if cached_result:
            print(f"  ✅ 緩存命中！直接返回 {len(cached_result)} 行結果")
        else:
            print(f"  🔍 緩存未命中，開始掃描Excel文件...")
            print(f"  📝 掃描完成，找到 {len(scenario['rows'])} 行匹配")
            print(f"  💾 保存結果到緩存")
            
            # 保存到緩存
            cache.save_filter_result(
                scenario['excel_file'],
                scenario['f_value'],
                scenario['g_value'],
                scenario['h_value'],
                scenario['rows']
            )
    
    print("\n🔄 第二次執行過濾（有緩存）...")
    
    # 模擬第二次過濾，應該全部命中緩存
    for scenario in scenarios:
        print(f"\n📊 過濾: {scenario['name']}")
        
        cached_result = cache.get_cached_result(
            scenario['excel_file'],
            scenario['f_value'],
            scenario['g_value'],
            scenario['h_value']
        )
        
        if cached_result:
            print(f"  ✅ 緩存命中！直接返回 {len(cached_result)} 行結果")
            print(f"  ⚡ 跳過Excel掃描，節省大量時間")
        else:
            print(f"  ❌ 緩存未命中，需要重新掃描")
    
    # 顯示緩存統計
    print("\n📊 緩存統計信息:")
    stats = cache.get_cache_stats()
    print(f"  總緩存條目: {stats['total_entries']}")
    print(f"  總緩存行數: {stats['total_rows']}")
    print(f"  緩存文件大小: {stats['cache_size_mb']:.2f} MB")
    
    print("\n📁 按文件分組統計:")
    for file_name, file_stats in stats['file_stats'].items():
        print(f"  {file_name}: {file_stats['count']} 個過濾條件, {file_stats['rows']} 行結果")
    
    # 導出緩存信息
    print("\n💾 導出緩存信息...")
    export_file = cache.export_cache_info()
    print(f"  緩存信息已導出到: {export_file}")
    
    # 清理演示緩存
    print("\n🧹 清理演示緩存...")
    cache.clear_cache()
    print("  演示緩存已清理")

def demo_cache_benefits():
    """演示緩存系統的優勢"""
    print("\n🎯 緩存系統優勢分析")
    print("=" * 60)
    
    # 模擬性能對比
    print("📊 性能對比（假設數據）:")
    print("  傳統掃描模式:")
    print("    - 掃描Excel文件: 2-5秒")
    print("    - 過濾處理: 1-3秒")
    print("    - 總耗時: 3-8秒")
    
    print("\n  緩存模式（首次）:")
    print("    - 掃描Excel文件: 2-5秒")
    print("    - 過濾處理: 1-3秒")
    print("    - 保存緩存: 0.01秒")
    print("    - 總耗時: 3-8秒")
    
    print("\n  緩存模式（後續）:")
    print("    - 檢查緩存: 0.001秒")
    print("    - 返回結果: 0.001秒")
    print("    - 總耗時: 0.002秒")
    
    print("\n🚀 性能提升:")
    print("  - 首次使用: 無提升（需要建立緩存）")
    print("  - 後續使用: 提升 1500-4000 倍")
    print("  - 大量重複過濾: 節省大量時間")
    
    print("\n💡 適用場景:")
    print("  - 重複使用相同過濾條件")
    print("  - 批量處理多個Excel文件")
    print("  - 需要快速響應的過濾查詢")
    print("  - 過濾條件相對固定的工作流程")

def main():
    """主函數"""
    try:
        # 基本使用演示
        demo_cache_usage()
        
        # 優勢分析演示
        demo_cache_benefits()
        
        print("\n🎉 演示完成！緩存系統可以大幅提升重複過濾的性能。")
        
    except Exception as e:
        print(f"\n❌ 演示失敗: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
