#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分批處理器
提供分批保存和恢復功能的獨立模塊
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class BatchProcessor:
    """分批處理器類"""
    
    def __init__(self, batch_size: int = 10, base_dir: str = None):
        """初始化分批處理器"""
        self.batch_size = batch_size
        self.base_dir = base_dir or f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.progress_file = os.path.join(self.base_dir, "progress.json")
        
        # 確保目錄存在
        os.makedirs(self.base_dir, exist_ok=True)
        
        # 初始化進度
        self.progress = self._load_progress()
        self.current_batch = {}
        self.current_batch_num = self._get_next_batch_number()
        
        logger.info(f"📦 分批處理器初始化: 批次大小={batch_size}, 目錄={self.base_dir}")
    
    def _load_progress(self) -> Dict:
        """載入進度文件"""
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    progress = json.load(f)
                logger.info(f"📂 載入進度: 已完成 {len(progress.get('completed_rows', []))} 條")
                return progress
            except Exception as e:
                logger.warning(f"⚠️ 載入進度失敗: {e}")
        
        return {
            'completed_rows': [],
            'batch_files': [],
            'start_time': datetime.now().isoformat(),
            'last_update': datetime.now().isoformat()
        }
    
    def _save_progress(self):
        """保存進度文件"""
        try:
            self.progress['last_update'] = datetime.now().isoformat()
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(self.progress, f, ensure_ascii=False, indent=2)
            logger.debug(f"💾 進度已保存: {len(self.progress.get('completed_rows', []))} 條完成")
        except Exception as e:
            logger.error(f"❌ 保存進度失敗: {e}")
    
    def _get_next_batch_number(self) -> int:
        """獲取下一個批次編號"""
        batch_files = self.progress.get('batch_files', [])
        if not batch_files:
            return 1
        
        # 從現有批次文件中找到最大編號
        max_num = 0
        for filename in batch_files:
            if filename.startswith('batch_') and filename.endswith('.json'):
                try:
                    num_str = filename[6:9]  # batch_XXX.json
                    num = int(num_str)
                    max_num = max(max_num, num)
                except:
                    continue
        
        return max_num + 1
    
    def is_processed(self, row_id: int) -> bool:
        """檢查行是否已處理"""
        return row_id in self.progress.get('completed_rows', [])
    
    def add_result(self, row_id: int, result_data: Dict[str, Any]):
        """添加處理結果到當前批次"""
        if self.is_processed(row_id):
            logger.info(f"⏭️ 第 {row_id} 行已處理，跳過")
            return False
        
        # 添加到當前批次
        self.current_batch[str(row_id)] = result_data
        self.progress['completed_rows'].append(row_id)
        
        logger.debug(f"➕ 添加到批次: 第 {row_id} 行")
        
        # 檢查是否需要保存批次
        if len(self.current_batch) >= self.batch_size:
            self._save_current_batch()
        
        return True
    
    def _save_current_batch(self):
        """保存當前批次"""
        if not self.current_batch:
            return
        
        try:
            batch_filename = f"batch_{self.current_batch_num:03d}.json"
            batch_filepath = os.path.join(self.base_dir, batch_filename)
            
            # 準備批次數據
            batch_data = {
                'metadata': {
                    'batch_number': self.current_batch_num,
                    'batch_size': len(self.current_batch),
                    'created_time': datetime.now().isoformat()
                },
                'results': self.current_batch
            }
            
            # 保存批次文件
            with open(batch_filepath, 'w', encoding='utf-8') as f:
                json.dump(batch_data, f, ensure_ascii=False, indent=2)
            
            # 更新進度記錄
            if batch_filename not in self.progress.get('batch_files', []):
                self.progress.setdefault('batch_files', []).append(batch_filename)
            
            # 保存進度
            self._save_progress()
            
            logger.info(f"💾 批次 {self.current_batch_num} 已保存: {batch_filename} ({len(self.current_batch)} 條)")
            
            # 重置當前批次
            self.current_batch = {}
            self.current_batch_num += 1
            
            return batch_filepath
            
        except Exception as e:
            logger.error(f"❌ 保存批次 {self.current_batch_num} 失敗: {e}")
            return None
    
    def finalize(self, final_filename: str = None) -> str:
        """完成處理，保存最後批次並合併所有結果"""
        # 保存最後一個批次
        if self.current_batch:
            logger.info(f"📦 保存最後批次 {self.current_batch_num} ({len(self.current_batch)} 條)")
            self._save_current_batch()
        
        # 合併所有批次
        return self._merge_all_batches(final_filename)
    
    def _merge_all_batches(self, final_filename: str = None) -> str:
        """合併所有批次到最終文件"""
        try:
            if final_filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                final_filename = f"qa_curation_results_{timestamp}.json"
            
            # 收集所有批次文件
            batch_files = self.progress.get('batch_files', [])
            batch_files.sort()  # 按文件名排序
            
            # 合併結果
            merged_results = {}
            total_processed = 0
            total_success = 0
            
            for batch_file in batch_files:
                batch_path = os.path.join(self.base_dir, batch_file)
                if not os.path.exists(batch_path):
                    logger.warning(f"⚠️ 批次文件不存在: {batch_file}")
                    continue
                
                try:
                    with open(batch_path, 'r', encoding='utf-8') as f:
                        batch_data = json.load(f)
                    
                    # 合併結果
                    batch_results = batch_data.get('results', {})
                    merged_results.update(batch_results)
                    
                    # 統計信息
                    total_processed += len(batch_results)
                    total_success += sum(1 for r in batch_results.values() if r.get('status') == 'success')
                    
                except Exception as e:
                    logger.warning(f"⚠️ 讀取批次文件 {batch_file} 失敗: {e}")
            
            # 準備最終數據
            final_data = {
                'metadata': {
                    'processing_start_time': self.progress.get('start_time', ''),
                    'processing_end_time': datetime.now().isoformat(),
                    'total_processed': total_processed,
                    'total_success': total_success,
                    'total_failed': total_processed - total_success,
                    'batch_processing': True,
                    'batch_count': len(batch_files),
                    'batch_size': self.batch_size,
                    'batch_directory': self.base_dir
                },
                'results': merged_results
            }
            
            # 保存最終文件
            with open(final_filename, 'w', encoding='utf-8') as f:
                json.dump(final_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ 合併完成: {final_filename}")
            logger.info(f"📊 總計: {total_processed} 條，成功: {total_success} 條，來自 {len(batch_files)} 個批次")
            
            return final_filename
            
        except Exception as e:
            logger.error(f"❌ 合併批次結果失敗: {e}")
            return None
    
    def get_stats(self) -> Dict[str, Any]:
        """獲取統計信息"""
        return {
            'batch_size': self.batch_size,
            'batch_directory': self.base_dir,
            'completed_rows': len(self.progress.get('completed_rows', [])),
            'batch_files': len(self.progress.get('batch_files', [])),
            'current_batch_size': len(self.current_batch),
            'next_batch_number': self.current_batch_num,
            'start_time': self.progress.get('start_time', ''),
            'last_update': self.progress.get('last_update', '')
        }
    
    def cleanup_batch_files(self, keep_final: bool = True):
        """清理批次文件"""
        try:
            batch_files = self.progress.get('batch_files', [])
            cleaned_count = 0
            
            for batch_file in batch_files:
                batch_path = os.path.join(self.base_dir, batch_file)
                if os.path.exists(batch_path):
                    os.remove(batch_path)
                    cleaned_count += 1
            
            # 清理進度文件
            if os.path.exists(self.progress_file):
                os.remove(self.progress_file)
            
            # 如果目錄為空，刪除目錄
            try:
                if not keep_final or not os.listdir(self.base_dir):
                    os.rmdir(self.base_dir)
                    logger.info(f"🗑️ 已清理批次目錄: {self.base_dir}")
                else:
                    logger.info(f"🧹 已清理 {cleaned_count} 個批次文件，保留目錄: {self.base_dir}")
            except OSError:
                logger.info(f"🧹 已清理 {cleaned_count} 個批次文件")
            
        except Exception as e:
            logger.error(f"❌ 清理批次文件失敗: {e}")


def test_batch_processor():
    """測試分批處理器"""
    print("🧪 測試分批處理器")
    print("=" * 40)
    
    # 創建處理器
    processor = BatchProcessor(batch_size=3)
    
    # 模擬添加結果
    test_data = [
        {'row': 1, 'score': 85, 'comment': '很好的回答'},
        {'row': 2, 'score': 92, 'comment': '優秀的分析'},
        {'row': 3, 'score': 78, 'comment': '不錯的見解'},
        {'row': 4, 'score': 88, 'comment': '深入的思考'},
        {'row': 5, 'score': 95, 'comment': '卓越的表現'},
        {'row': 6, 'score': 82, 'comment': '良好的理解'},
        {'row': 7, 'score': 90, 'comment': '精彩的回答'},
    ]
    
    print(f"📦 開始處理 {len(test_data)} 條數據...")
    
    for data in test_data:
        row_id = data['row']
        result_data = {
            'score': data['score'],
            'comment': data['comment'],
            'status': 'success',
            'processed_time': datetime.now().isoformat()
        }
        
        success = processor.add_result(row_id, result_data)
        if success:
            print(f"✅ 處理第 {row_id} 行: 分數 {data['score']}")
        else:
            print(f"⏭️ 跳過第 {row_id} 行: 已處理")
    
    # 完成處理
    final_file = processor.finalize()
    
    # 顯示統計
    stats = processor.get_stats()
    print(f"\n📊 處理統計:")
    print(f"   - 已完成: {stats['completed_rows']} 條")
    print(f"   - 批次數: {stats['batch_files']} 個")
    print(f"   - 批次大小: {stats['batch_size']} 條/批次")
    print(f"   - 最終文件: {final_file}")
    
    # 清理
    processor.cleanup_batch_files()
    
    return True

if __name__ == "__main__":
    test_batch_processor()
