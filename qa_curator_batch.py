#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
佛學問答精選器 - 分批處理版本
支持每10個條目保存一次，避免數據丟失
"""

import sys
import os
import argparse
import logging
from datetime import datetime

# 添加當前目錄到Python路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from qa_curator import BuddhistQACurator
from batch_processor import BatchProcessor

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('qa_curation_batch.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BuddhistQACuratorBatch(BuddhistQACurator):
    """佛學問答精選器 - 分批處理版本"""
    
    def __init__(self, config_file: str = 'config.ini', api_key: str = None, 
                 api_type: str = None, chatmock_url: str = None, batch_size: int = 10):
        """初始化分批處理版本的精選器"""
        super().__init__(config_file, api_key, api_type, chatmock_url)
        self.batch_size = batch_size
        self.batch_processor = None
        logger.info(f"📦 分批處理版本初始化完成，批次大小: {batch_size}")
    
    def process_batch_safe(self, start_row: int = None, end_row: int = None, results_file: str = None):
        """安全的分批處理方法"""
        try:
            # 記錄開始時間
            overall_start_time = datetime.now()
            logger.info(f"🚀 開始安全分批處理 - 時間: {overall_start_time.strftime('%H:%M:%S')}")
            
            # 載入配置
            if start_row is None:
                start_row = self.config.getint('processing', 'start_row', fallback=2)
            if end_row is None:
                config_end_row = self.config.getint('processing', 'end_row', fallback=0)
                end_row = config_end_row if config_end_row > 0 else None
            
            # 設置結果文件名
            if results_file is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                results_file = f'qa_curation_results_{timestamp}.json'
            
            logger.info(f"📁 最終結果文件: {results_file}")
            logger.info(f"📦 分批大小: {self.batch_size} 條/批次")
            
            # 初始化分批處理器
            self.batch_processor = BatchProcessor(batch_size=self.batch_size)
            
            # 載入Excel數據
            logger.info("📊 載入Excel數據...")
            workbook, worksheet = self.load_excel_data()
            logger.info(f"✅ Excel數據載入完成")
            
            # 檢查處理模式
            use_filter_mode = self.config.getboolean('processing', 'use_filter_mode', fallback=False)
            
            if use_filter_mode:
                # 過濾模式
                logger.info("🔍 使用過濾模式...")
                rows_to_process = self.get_filtered_rows(worksheet)
                
                if not rows_to_process:
                    logger.warning("⚠️ 過濾模式下沒有找到符合條件的行")
                    return results_file
                
                logger.info(f"✅ 過濾完成，找到 {len(rows_to_process)} 行")
                
                # 獲取過濾結果的評分範圍
                filter_start_index = self.config.getint('filter', 'start_index', fallback=0)
                filter_end_index = self.config.getint('filter', 'end_index', fallback=0)
                score_all_filtered = self.config.getboolean('filter', 'score_all_filtered', fallback=False)
                
                if score_all_filtered:
                    logger.info("🎯 評分所有過濾結果")
                elif filter_end_index > 0:
                    start_idx = max(0, filter_start_index)
                    end_idx = min(len(rows_to_process), filter_end_index + 1)
                    rows_to_process = rows_to_process[start_idx:end_idx]
                    logger.info(f"🎯 過濾模式：處理第 {start_idx+1} 到第 {end_idx} 條過濾結果，共 {len(rows_to_process)} 條")
                else:
                    rows_to_process = rows_to_process[:1]
                    logger.info("🎯 過濾模式：只處理第一條過濾結果")
            else:
                # 傳統模式（指定行號）
                logger.info("📝 使用行號模式...")
                max_row = worksheet.max_row
                if end_row is None or end_row > max_row:
                    end_row = max_row
                
                rows_to_process = list(range(start_row, end_row + 1))
                logger.info(f"🎯 行號模式：處理第 {start_row} 到 {end_row} 行，共 {len(rows_to_process)} 條記錄")
            
            # 開始處理
            total_count = len(rows_to_process)
            processed_count = 0
            success_count = 0
            failed_count = 0
            skipped_count = 0
            
            logger.info(f"🚀 開始評分處理，總目標: {total_count} 條記錄")
            
            for i, row in enumerate(rows_to_process):
                try:
                    # 檢查是否已處理
                    if self.batch_processor.is_processed(row):
                        logger.info(f"⏭️ 第 {row} 行已處理，跳過")
                        skipped_count += 1
                        continue
                    
                    # 顯示進度
                    progress_percent = ((i + 1) / total_count) * 100
                    logger.info(f"📈 進度: {i+1}/{total_count} ({progress_percent:.1f}%)")
                    
                    # 提取問答內容
                    logger.info(f"📖 提取第 {row} 行問答內容...")
                    question, answer = self.extract_qa_content(worksheet, row)
                    
                    if not question and not answer:
                        logger.info(f"⚠️ 第 {row} 行無內容，跳過")
                        skipped_count += 1
                        continue
                    
                    logger.info(f"🔄 處理第 {row} 行: {question[:100]}...")
                    
                    # 進行精選評分
                    logger.info(f"🤖 開始AI評分...")
                    result = self.evaluate_qa_quality(question, answer)
                    logger.info(f"✅ AI評分完成")
                    
                    # 準備結果數據
                    result_data = {
                        'row_number': row,
                        'question': question[:500],  # 限制長度
                        'answer': answer[:1000],     # 限制長度
                        'breadth_score': result.get('breadth_score', ''),
                        'depth_score': result.get('depth_score', ''),
                        'uniqueness_score': result.get('uniqueness_score', ''),
                        'overall_score': result.get('overall_score', ''),
                        'breadth_comment': result.get('breadth_comment', ''),
                        'depth_comment': result.get('depth_comment', ''),
                        'uniqueness_comment': result.get('uniqueness_comment', ''),
                        'overall_comment': result.get('overall_comment', ''),
                        'question_summary': result.get('question_summary', ''),
                        'answer_summary': result.get('answer_summary', ''),
                        'status': result.get('status', 'success'),
                        'processed_time': datetime.now().isoformat()
                    }
                    
                    # 添加到分批處理器
                    success = self.batch_processor.add_result(row, result_data)
                    if success:
                        processed_count += 1
                        if result.get('status') == 'success':
                            success_count += 1
                        else:
                            failed_count += 1
                        
                        logger.info(f"✅ 第 {row} 行處理完成")
                    
                    # API調用間隔
                    if i < total_count - 1:
                        logger.info(f"⏸️ 等待1秒後處理下一條...")
                        import time
                        time.sleep(1)
                
                except Exception as e:
                    logger.error(f"❌ 處理第 {row} 行時發生錯誤: {e}")
                    failed_count += 1
                    processed_count += 1
                    continue
            
            # 完成處理並生成最終文件
            logger.info(f"🔄 完成處理，生成最終文件...")
            final_file = self.batch_processor.finalize(results_file)
            
            # 計算總統計
            total_time = (datetime.now() - overall_start_time).total_seconds()
            
            # 顯示統計
            stats = self.batch_processor.get_stats()
            logger.info(f"🎉 安全分批處理完成！")
            logger.info(f"📊 統計結果:")
            logger.info(f"   - 總計: {total_count} 條")
            logger.info(f"   - 成功: {success_count} 條")
            logger.info(f"   - 失敗: {failed_count} 條")
            logger.info(f"   - 跳過: {skipped_count} 條")
            logger.info(f"📦 分批處理統計:")
            logger.info(f"   - 批次大小: {stats['batch_size']} 條/批次")
            logger.info(f"   - 總批次數: {stats['batch_files']} 個")
            logger.info(f"   - 批次目錄: {stats['batch_directory']}")
            logger.info(f"⏱️ 總耗時: {total_time:.2f}秒 ({total_time/60:.1f}分鐘)")
            if processed_count > 0:
                logger.info(f"🚀 平均速度: {processed_count/total_time:.2f} 條/秒")
            
            return final_file
            
        except Exception as e:
            logger.error(f"❌ 安全分批處理失敗: {e}")
            raise
    
    def cleanup_batch_files(self, keep_final: bool = True):
        """清理批次文件"""
        if self.batch_processor:
            self.batch_processor.cleanup_batch_files(keep_final)

def main():
    """主函數"""
    parser = argparse.ArgumentParser(
        description="佛學問答精選自動化系統 - 分批處理版本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 使用ChatMock，每10條保存一次
  python3 qa_curator_batch.py --api-type chatmock --batch-size 10
  
  # 使用OpenAI API，每5條保存一次
  python3 qa_curator_batch.py --api-key YOUR_API_KEY --api-type openai --batch-size 5
  
  # 使用默認設置
  python3 qa_curator_batch.py
        """
    )
    
    parser.add_argument(
        '--api-key',
        type=str,
        help='OpenAI API Key'
    )
    
    parser.add_argument(
        '--api-type',
        type=str,
        choices=['openai', 'chatmock'],
        help='API類型選擇：openai 或 chatmock'
    )
    
    parser.add_argument(
        '--chatmock-url',
        type=str,
        help='ChatMock服務器URL'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='config.ini',
        help='配置文件路徑'
    )
    
    parser.add_argument(
        '--batch-size',
        type=int,
        default=10,
        help='分批大小（每批次保存的條目數，默認10）'
    )
    
    parser.add_argument(
        '--cleanup',
        action='store_true',
        help='處理完成後清理批次文件'
    )
    
    args = parser.parse_args()
    
    print("佛學問答精選自動化系統 - 分批處理版本")
    print("=" * 50)
    print(f"📦 分批大小: {args.batch_size} 條/批次")
    print(f"🔧 配置文件: {args.config}")
    
    try:
        # 創建精選器
        curator = BuddhistQACuratorBatch(
            config_file=args.config,
            api_key=args.api_key,
            api_type=args.api_type,
            chatmock_url=args.chatmock_url,
            batch_size=args.batch_size
        )
        
        # 執行處理
        results_file = curator.process_batch_safe()
        
        print(f"\n✅ 處理完成！")
        print(f"📁 結果文件: {results_file}")
        
        # 清理批次文件（如果需要）
        if args.cleanup:
            print(f"🧹 清理批次文件...")
            curator.cleanup_batch_files()
            print(f"✅ 清理完成")
        else:
            print(f"💡 批次文件已保留，可用於恢復或調試")
            stats = curator.batch_processor.get_stats()
            print(f"📁 批次目錄: {stats['batch_directory']}")
        
    except KeyboardInterrupt:
        print(f"\n⚠️ 用戶中斷處理")
        print(f"💡 已處理的數據已保存到批次文件中")
        print(f"💡 可以重新運行程序繼續處理")
        
    except Exception as e:
        logger.error(f"程序執行失敗: {e}")
        print(f"❌ 程序執行失敗: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
