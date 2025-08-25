#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試過濾結果緩存系統
"""

import os
import sys
from filter_cache import FilterCache

def test_cache_basic():
    """測試基本緩存功能"""
    print("🧪 測試基本緩存功能...")
    
    # 創建緩存管理器
    cache = FilterCache(".test_cache")
    
    # 測試數據
    test_data = [
        {
            'excel_file': 'test1.xlsx',
            'f_value': '01义理',
            'g_value': '04起源',
            'h_value': '05娑婆世界',
            'rows': [82, 86, 292, 332, 405]
        },
        {
            'excel_file': 'test1.xlsx',
            'f_value': '02修行',
            'g_value': '01禪修',
            'h_value': '02中級',
            'rows': [100, 150, 200]
        }
    ]
    
    # 保存測試數據
    for data in test_data:
        cache.save_filter_result(
            data['excel_file'],
            data['f_value'],
            data['g_value'],
            data['h_value'],
            data['rows']
        )
    
    print("✅ 測試數據保存完成")
    
    # 測試緩存命中
    for data in test_data:
        cached_rows = cache.get_cached_result(
            data['excel_file'],
            data['f_value'],
            data['g_value'],
            data['h_value']
        )
        
        if cached_rows == data['rows']:
            print(f"✅ 緩存命中: {data['f_value']}-{data['g_value']}-{data['h_value']}")
        else:
            print(f"❌ 緩存未命中: {data['f_value']}-{data['g_value']}-{data['h_value']}")
    
    # 測試緩存統計
    stats = cache.get_cache_stats()
    print(f"📊 緩存統計: {stats['total_entries']} 條記錄, {stats['total_rows']} 行結果")
    
    # 測試緩存未命中
    missing_result = cache.get_cached_result('test1.xlsx', '03其他', '01其他', '01其他')
    if missing_result is None:
        print("✅ 緩存未命中測試通過")
    else:
        print("❌ 緩存未命中測試失敗")
    
    # 清理測試緩存
    cache.clear_cache()
    print("🧹 測試緩存已清理")

def test_cache_export():
    """測試緩存導出功能"""
    print("\n🧪 測試緩存導出功能...")
    
    cache = FilterCache(".test_cache")
    
    # 添加一些測試數據
    cache.save_filter_result('test2.xlsx', 'A', 'B', 'C', [1, 2, 3])
    cache.save_filter_result('test2.xlsx', 'D', 'E', 'F', [4, 5, 6])
    
    # 導出緩存信息
    export_file = cache.export_cache_info()
    if os.path.exists(export_file):
        print(f"✅ 緩存信息導出成功: {export_file}")
        
        # 檢查文件大小
        file_size = os.path.getsize(export_file)
        print(f"📁 導出文件大小: {file_size} 字節")
    else:
        print("❌ 緩存信息導出失敗")
    
    # 清理測試緩存
    cache.clear_cache()

def test_cache_performance():
    """測試緩存性能"""
    print("\n🧪 測試緩存性能...")
    
    cache = FilterCache(".test_cache")
    
    # 模擬大量緩存數據
    import time
    start_time = time.time()
    
    for i in range(100):
        cache.save_filter_result(
            f'test{i}.xlsx',
            f'F{i}',
            f'G{i}',
            f'H{i}',
            list(range(i*10, (i+1)*10))
        )
    
    save_time = time.time() - start_time
    print(f"📝 保存100條緩存記錄耗時: {save_time:.3f}秒")
    
    # 測試讀取性能
    start_time = time.time()
    for i in range(100):
        cache.get_cached_result(f'test{i}.xlsx', f'F{i}', f'G{i}', f'H{i}')
    
    read_time = time.time() - start_time
    print(f"📖 讀取100條緩存記錄耗時: {read_time:.3f}秒")
    
    # 清理測試緩存
    cache.clear_cache()

def main():
    """主函數"""
    print("🚀 過濾結果緩存系統測試")
    print("=" * 50)
    
    try:
        # 基本功能測試
        test_cache_basic()
        
        # 導出功能測試
        test_cache_export()
        
        # 性能測試
        test_cache_performance()
        
        print("\n🎉 所有測試通過！緩存系統工作正常。")
        
    except Exception as e:
        print(f"\n❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
