# 佛學問答精選器配置指南

## 🎯 過濾模式配置說明

### 基本概念

過濾模式允許您根據Excel列F、G、H的值來選擇要評分的問答，而不是按行號選擇。

### 配置選項

#### 1. 評分範圍設定

```ini
[filter]
# 方式1：評分所有過濾結果
score_all_filtered = true

# 方式2：評分指定範圍的過濾結果
score_all_filtered = false
start_index = 0    # 開始索引（從0開始，0表示第一條）
end_index = 2      # 結束索引（包含此條，0表示只評分第一條）
```

#### 2. 過濾條件設定

```ini
[filter]
# 列值過濾條件
column_f_value = 01义理    # 第F列（第6列）必須匹配的值
column_g_value = 04起源    # 第G列（第7列）必須匹配的值  
column_h_value = 05娑婆世界 # 第H列（第8列）必須匹配的值
```

### 配置示例

#### 示例1：評分所有過濾結果
```ini
[filter]
score_all_filtered = true
# start_index 和 end_index 將被忽略
column_f_value = 01义理
column_g_value = 04起源
column_h_value = 05娑婆世界
```

#### 示例2：只評分第一條過濾結果
```ini
[filter]
score_all_filtered = false
start_index = 0
end_index = 0
column_f_value = 01义理
column_g_value = 04起源
column_h_value = 05娑婆世界
```

#### 示例3：評分前3條過濾結果
```ini
[filter]
score_all_filtered = false
start_index = 0
end_index = 2
column_f_value = 01义理
column_g_value = 04起源
column_h_value = 05娑婆世界
```

### 常見問題

#### Q1：為什麼沒有條目被評分？
**可能原因：**
1. `start_index` 設置過大，超過了過濾結果的數量
2. 過濾條件沒有匹配到任何行
3. `score_all_filtered = false` 但索引範圍設置不當

**解決方案：**
- 使用 `score_all_filtered = true` 評分所有過濾結果
- 或者將 `start_index` 設置為 0，`end_index` 設置為合理的值

#### Q2：如何知道過濾結果的數量？
**方法：**
1. 查看日誌中的 "過濾完成，共找到 X 行" 信息
2. 過濾結果的索引範圍是 0 到 (X-1)

#### Q3：索引從0開始還是從1開始？
**答案：** 索引從0開始
- 第1條過濾結果的索引是 0
- 第2條過濾結果的索引是 1
- 以此類推

### 推薦配置

對於大多數使用場景，推薦使用：

```ini
[filter]
score_all_filtered = true
column_f_value = 01义理
column_g_value = 04起源
column_h_value = 05娑婆世界
```

這樣可以：
1. 避免索引範圍的複雜性
2. 確保不會遺漏任何過濾結果
3. 簡化配置管理

### 性能優化

系統會自動緩存過濾結果，重複使用相同過濾條件時會大幅提升性能：
- 首次使用：正常掃描Excel文件
- 後續使用：直接從緩存返回結果，響應時間從秒級降低到毫秒級
