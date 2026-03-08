# Ahorro JSON 初步剖析結果

## 來源資料
- JSON: `D:/Google 雲端硬碟/Memo/Accounting/Ahorro_Backup_20190522144210.json`
- 參考 CSV (推估分類用): `D:/Google 雲端硬碟/Memo/Accounting/2019-05-01-2019-06-01.csv`

## 核心統計
- 總筆數: 3,288
- 支出: 3,241 筆
- 收入: 47 筆
- 日期範圍: 2015-07-20 ~ 2019-05-21
- 支出總額: 510,010
- 收入總額: 383,269
- 淨額 (收入-支出): -126,741

## 已產出檔案
- 初版轉換 (5 欄): `analysis_output/ahorro_preliminary_converted.csv`
- 除錯版 (含舊類別/推定類別): `analysis_output/ahorro_preliminary_converted_debug.csv`
- 分類映射候選: `analysis_output/category_mapping_candidates.csv`
- 摘要文字: `analysis_output/summary.txt`

## 圖表 (SVG)
- 每月收支趨勢: `analysis_output/chart_monthly_income_expense.svg`
- 每月交易筆數: `analysis_output/chart_monthly_record_counts.svg`
- 支出前 15 類別: `analysis_output/chart_top_expense_categories.svg`

## 自動推估到新分類 (已採用)
- type100 -> 早餐
- type101 -> 午餐
- type102 -> 晚餐
- type103 -> 飲料
- type104 -> 零食
- type105 -> 交通
- type106 -> 日常用品
- 點心 -> 點心

## 尚未自動映射的舊類別代碼
- type107, type108, type109, type110, type111, type112, type114, type115, type117, type119
- type200, type201, type204 (收入類)

以上代碼仍保留在輸出 CSV 的 `類別` 欄，方便後續逐步定義最終映射規則。
