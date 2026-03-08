# Ahorro Category Mapping Discussion

- Source JSON: `Ahorro_Backup_20190522144210.json`
- Purpose: 和你一起逐項確認「舊分類 -> 新分類」
- Rule: `status=confirmed` 才會進入最終轉換規則

## Status Legend

- `seeded`: 先前自動推估，等你確認
- `open`: 尚未討論
- `confirmed`: 你已確認可用
- `blocked`: 需要更多上下文才可判斷

## Mapping Table

| category_id | old_name | behavior | records | total_amount | sample_notes | proposed_new_category | status | discussion_notes |
|---:|---|---|---:|---:|---|---|---|---|
| 1 | type100 | expense | 524 | 17,994 |  | 早餐 | seeded |  |
| 2 | type101 | expense | 833 | 75,190 | 食材 | 午餐 | seeded |  |
| 3 | type102 | expense | 827 | 95,747 | 西堤; 高鐵票 | 晚餐 | seeded |  |
| 4 | type103 | expense | 271 | 11,072 | 水; 丹堤 熱帶水果茶; 百花蜜青 | 飲料 | seeded |  |
| 5 | type104 | expense | 40 | 2,632 | 冰棒; 蛋捲冰淇淋; 不二家棒棒糖 | 零食 | seeded |  |
| 6 | type105 | expense | 249 | 60,490 | 高鐵票; 電信悠遊卡; 停車 | 交通 | seeded |  |
| 7 | type106 | expense | 84 | 16,628 | 垃圾袋; 剪頭髮; 冷氣卡 | 日常用品 | seeded |  |
| 8 | type107 | expense | 89 | 68,426 | steam錢包; 巴哈姆特動畫瘋; 看電影 | 娛樂 | confirmed | 樣本高度集中在遊戲、影音訂閱、電影。 |
| 9 | type108 | expense | 2 | 274 | 請客; 宇治抹茶珍珠 | 禮品 | confirmed | 依你的使用情境確認為禮品。 |
| 10 | type109 | expense | 9 | 6,329 | lativ; lativ外套; 校運外套 | 服裝 | confirmed | 樣本明確是衣物與外套。 |
| 11 | type110 | expense | 27 | 86,556 | 畢業照; RX100座充電池組; 鍵盤：i-Rocks IRK01 | 電子產品 | confirmed | 多數樣本偏 3C/配件；雖含少量非 3C 項目，但整體仍可歸入電子產品。 |
| 12 | type111 | expense | 6 | 36,635 | 一個月押金，實際12000; 大資盃; 4月 | 房租 | confirmed | 依你的使用情境確認為房租；少數異常樣本不另拆分類。 |
| 13 | type112 | expense | 4 | 1,805 | 豆沙餅; 鮮乳坊牛奶x3; 口試貢品 | 禮品 | confirmed | 依你的使用情境確認為禮品。 |
| 14 | type113 | expense | 0 | 0 |  |  | open |  |
| 15 | type114 | expense | 7 | 3,531 | 掛號費; 照x光; 新生健檢 | 健康 | confirmed | 樣本明確是醫療與健檢支出。 |
| 16 | type115 | expense | 9 | 4,491 | 10月; 11月; 12月 | 電信費 | confirmed | 樣本含「中華電信2月」「中華電信3月」，且月費固定。 |
| 17 | type116 | expense | 0 | 0 |  |  | open |  |
| 18 | type117 | expense | 1 | 100 | 悠遊卡 | 交通 | confirmed | 雖僅一筆，但依你的決策併入交通。 |
| 19 | type118 | expense | 0 | 0 |  |  | open |  |
| 20 | type119 | expense | 41 | 4,734 | 成績單; 影印; 掃描成績單 | 其他 | confirmed | 依你的使用情境確認為其他。 |
| 21 | type200 | income | 28 | 380,493 | 研究生獎助學金 9月; 研究生獎助學金 10月; 研究生獎助學金 11月 | 薪水 | confirmed | 依你的說明，研究生獎助學金在你的記帳習慣中視為薪水。 |
| 22 | type201 | income | 10 | 1,321 | 統一發票; OK禮券; 7-11回饋金 | 其他 | confirmed | 樣本來源分散，暫時歸入其他合理。 |
| 23 | type202 | income | 0 | 0 |  |  | open |  |
| 24 | type203 | income | 0 | 0 |  |  | open |  |
| 25 | type204 | income | 9 | 1,455 | 7-11購物金; 影印卡退費; 冷氣卡退費 | 其他 | confirmed | 依你的決策確認為收入類的其他；新版 CSV 已區分收入與支出。 |
| 26 | 宵夜 | expense | 126 | 5,759 | 冰淇淋; 觀音拿鐵 |  | open |  |
| 27 | 書 | expense | 40 | 6,928 | 影印; 影印卡儲值; 印paper |  | open |  |
| 28 | 門票 | expense | 38 | 4,246 | 羽球館; 羽球場; 游泳 |  | open |  |
| 29 | 點心 | expense | 14 | 442 | 丹堤 耶加雪霏蛋糕; 冰炫風; 丹堤 濃情巧克力蛋糕 | 點心 | seeded |  |
