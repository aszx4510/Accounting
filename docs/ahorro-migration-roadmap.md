# Ahorro Migration Roadmap

## Goal

- 把 Ahorro 舊 JSON 轉成與新記帳 CSV 同規格的檔案。
- 最終輸出格式目標：`日期, 收入/支出, 類別, 備註, 合計`。

## Working Files

- JSON 清單: `docs/ahorro-json-inventory.md`
- 分類 mapping 討論: `docs/ahorro-category-mapping.md`
- 未定案類別樣本: `docs/ahorro-unresolved-category-samples.md`

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
| 2026-03-08 | type107-type201 初次命名 | 先確認證據明確的分類，證據不足者標成 blocked 待你再決定 | 已更新 mapping 討論表 |
| 2026-03-08 | type108-type204 補充確認 | 依你提供的記帳語境，確認 `type108`、`type111`、`type112`、`type115`、`type117`、`type119`、`type200`、`type204` | 已更新 mapping 討論表與樣本文件 |

## Next Session Checklist

- 處理尚未命名的 `type113`、`type116`、`type118`、`type202`、`type203`。
- 討論既有自訂類別 `宵夜`、`書`、`門票` 是否保留原名或重新映射。
- 全部 `confirmed` 後再進入 CSV 最終輸出。
