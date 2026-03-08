# Ahorro Migration Roadmap

## Goal

- 把 Ahorro 舊 JSON 轉成與新記帳 CSV 同規格的檔案。
- 最終輸出格式目標：`日期, 收入/支出, 類別, 備註, 合計`。

## Working Files

- JSON 清單: `docs/ahorro-json-inventory.md`
- 分類 mapping 討論: `docs/ahorro-category-mapping.md`

## Agreed Process

- [x] Step 1: 盤點所有 Ahorro JSON 檔案。
- [x] Step 2: 建立 mapping 討論表，先逐項 review。
- [ ] Step 3: 與你逐項確認 `proposed_new_category`，把狀態改為 `confirmed`。
- [ ] Step 4: 鎖定最終 mapping 規則，保留版本化記錄。
- [ ] Step 5: 依規則輸出新的 CSV，可按年份切檔。
- [ ] Step 6: 抽樣驗證與修正。

## Discussion Log

| Date | Topic | Decision | Action |
|---|---|---|---|
| 2026-03-08 | 流程重排 | 先做 JSON 盤點與 mapping 設計，再做轉換 | 已建立三份 markdown |

## Next Session Checklist

- 從 `type107` 開始，逐項確認到 `type204`。
- 每確認一列就更新 `status` 與 `discussion_notes`。
- 全部 `confirmed` 後再進入 CSV 最終輸出。
