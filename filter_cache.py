#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
過濾結果緩存管理系統
"""

import json
import os
import hashlib
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

class FilterCache:
    """過濾結果緩存管理類"""
    
    def __init__(self, cache_dir: str = ".filter_cache"):
        """
        初始化緩存管理器
        
        Args:
            cache_dir: 緩存文件存儲目錄
        """
        self.cache_dir = cache_dir
        self.cache_file = os.path.join(cache_dir, "filter_cache.json")
        self.cache_data = {}
        self._ensure_cache_dir()
        self._load_cache()
    
    def _ensure_cache_dir(self):
        """確保緩存目錄存在"""
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
            logger.info(f"創建緩存目錄: {self.cache_dir}")
    
    def _load_cache(self):
        """載入緩存數據"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.cache_data = json.load(f)
                logger.info(f"緩存載入成功，共 {len(self.cache_data)} 條記錄")
            else:
                self.cache_data = {}
                logger.info("緩存文件不存在，創建新的緩存")
        except Exception as e:
            logger.error(f"載入緩存失敗: {e}")
            self.cache_data = {}
    
    def _save_cache(self):
        """保存緩存數據"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache_data, f, ensure_ascii=False, indent=2)
            logger.debug("緩存保存成功")
        except Exception as e:
            logger.error(f"保存緩存失敗: {e}")
    
    def _generate_cache_key(self, excel_file: str, f_value: str, g_value: str, h_value: str) -> str:
        """
        生成緩存鍵值
        
        Args:
            excel_file: Excel文件名
            f_value: F列值
            g_value: G列值
            h_value: H列值
            
        Returns:
            緩存鍵值
        """
        # 使用文件名和列值的組合生成緩存鍵
        key_parts = [
            os.path.basename(excel_file),  # 文件名（不含路徑）
            f_value or "",
            g_value or "",
            h_value or ""
        ]
        
        # 生成MD5哈希作為緩存鍵
        key_string = "|".join(key_parts)
        cache_key = hashlib.md5(key_string.encode('utf-8')).hexdigest()
        
        logger.debug(f"生成緩存鍵: {key_string} -> {cache_key}")
        return cache_key
    
    def get_cached_result(self, excel_file: str, f_value: str, g_value: str, h_value: str) -> Optional[List[int]]:
        """
        獲取緩存的過濾結果
        
        Args:
            excel_file: Excel文件名
            f_value: F列值
            g_value: G列值
            h_value: H列值
            
        Returns:
            緩存的行號列表，如果沒有緩存則返回None
        """
        cache_key = self._generate_cache_key(excel_file, f_value, g_value, h_value)
        
        if cache_key in self.cache_data:
            cache_entry = self.cache_data[cache_key]
            
            # 檢查緩存是否有效
            if self._is_cache_valid(cache_entry, excel_file):
                logger.info(f"緩存命中: {cache_key}, 返回 {len(cache_entry['rows'])} 行結果")
                return cache_entry['rows']
            else:
                logger.info(f"緩存已過期: {cache_key}")
                # 刪除過期緩存
                del self.cache_data[cache_key]
                self._save_cache()
        
        return None
    
    def _is_cache_valid(self, cache_entry: Dict, excel_file: str) -> bool:
        """
        檢查緩存是否有效
        
        Args:
            cache_entry: 緩存條目
            excel_file: Excel文件名
            
        Returns:
            緩存是否有效
        """
        # 檢查文件名是否匹配
        if cache_entry.get('excel_file') != os.path.basename(excel_file):
            return False
        
        # 檢查緩存時間（可選：設置緩存過期時間）
        cache_time = cache_entry.get('cache_time')
        if cache_time:
            try:
                cache_datetime = datetime.fromisoformat(cache_time)
                # 緩存7天過期
                if (datetime.now() - cache_datetime).days > 7:
                    return False
            except:
                pass
        
        return True
    
    def save_filter_result(self, excel_file: str, f_value: str, g_value: str, h_value: str, 
                          rows: List[int], scan_stats: Dict = None):
        """
        保存過濾結果到緩存
        
        Args:
            excel_file: Excel文件名
            f_value: F列值
            g_value: G列值
            h_value: H列值
            rows: 過濾結果行號列表
            scan_stats: 掃描統計信息
        """
        cache_key = self._generate_cache_key(excel_file, f_value, g_value, h_value)
        
        cache_entry = {
            'excel_file': os.path.basename(excel_file),
            'f_value': f_value,
            'g_value': g_value,
            'h_value': h_value,
            'rows': rows,
            'cache_time': datetime.now().isoformat(),
            'scan_stats': scan_stats or {}
        }
        
        self.cache_data[cache_key] = cache_entry
        self._save_cache()
        
        logger.info(f"緩存保存成功: {cache_key}, {len(rows)} 行結果")
    
    def get_cache_stats(self) -> Dict:
        """獲取緩存統計信息"""
        total_entries = len(self.cache_data)
        total_rows = sum(len(entry.get('rows', [])) for entry in self.cache_data.values())
        
        # 按Excel文件分組統計
        file_stats = {}
        for entry in self.cache_data.values():
            file_name = entry.get('excel_file', 'unknown')
            if file_name not in file_stats:
                file_stats[file_name] = {'count': 0, 'rows': 0}
            file_stats[file_name]['count'] += 1
            file_stats[file_name]['rows'] += len(entry.get('rows', []))
        
        return {
            'total_entries': total_entries,
            'total_rows': total_rows,
            'file_stats': file_stats,
            'cache_size_mb': os.path.getsize(self.cache_file) / (1024 * 1024) if os.path.exists(self.cache_file) else 0
        }
    
    def clear_cache(self, excel_file: str = None):
        """
        清理緩存
        
        Args:
            excel_file: 指定Excel文件的緩存，如果為None則清理所有緩存
        """
        if excel_file:
            # 清理指定文件的緩存
            file_name = os.path.basename(excel_file)
            keys_to_remove = []
            for key, entry in self.cache_data.items():
                if entry.get('excel_file') == file_name:
                    keys_to_remove.append(key)
            
            for key in keys_to_remove:
                del self.cache_data[key]
            
            logger.info(f"清理文件 {file_name} 的緩存，共 {len(keys_to_remove)} 條記錄")
        else:
            # 清理所有緩存
            count = len(self.cache_data)
            self.cache_data = {}
            logger.info(f"清理所有緩存，共 {count} 條記錄")
        
        self._save_cache()
    
    def export_cache_info(self, output_file: str = None) -> str:
        """
        導出緩存信息
        
        Args:
            output_file: 輸出文件路徑，如果為None則使用默認路徑
            
        Returns:
            輸出文件路徑
        """
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(self.cache_dir, f"cache_info_{timestamp}.json")
        
        cache_info = {
            'export_time': datetime.now().isoformat(),
            'cache_stats': self.get_cache_stats(),
            'cache_entries': self.cache_data
        }
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(cache_info, f, ensure_ascii=False, indent=2)
            logger.info(f"緩存信息導出成功: {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"導出緩存信息失敗: {e}")
            raise
