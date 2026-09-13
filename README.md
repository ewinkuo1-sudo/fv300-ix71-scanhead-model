# FV300／IX71 展示模型

依實機照片與 Olympus 型錄建立的展示用粗模；尺寸、隱藏面與部分機構仍為推估。

## 目前整機版本：v0.4

- [照片對照與核對頁](v04_fv300_ix71_assembly_20260913/review.html)（下載 repo 後以瀏覽器開啟）
- [可編輯 Blender 模型](v04_fv300_ix71_assembly_20260913/FV300_IX71_round1.blend)
- [尺寸依據、推估與重現說明](v04_fv300_ix71_assembly_20260913/README.md)
- [155 個分件](v04_fv300_ix71_assembly_20260913/parts.csv)

包含 FV300、側接筒、IX71 主體、目鏡、載物台、物鏡座及光纖照明柱。
Blender 內可切換掃描頭開蓋／閉蓋。模型已重新載入、檢視十一個視角並實際開啟 GUI。
本版保存為後續展示與動畫的基準；不代表尺寸已經實機量測。

## 版本保留

| 版本 | 目錄 | 說明 |
| --- | --- | --- |
| v0.1 | v01_scanhead/ | 三張斜拍照片的初版 |
| v0.2 | v02_overhead_revision/ | 加入俯視照；舊離線互動 viewer |
| v0.3 | v03_blender_blockout_20260913/ | Blender 掃描頭獨立重建粗模 |
| v0.4 | v04_fv300_ix71_assembly_20260913/ | FV300＋IX71 整機粗模里程碑 |

根目錄 viewer.html 連到 v0.4 核對頁；舊版模型與互動 viewer 留在各版目錄。
根目錄 20260910_*.jpg 為實機照片。
原廠型錄來源列於 v0.4 README；完整下載快取留在本機，repo 包含核對圖與來源連結。

## 重現

v0.3/v0.4 使用 Blender 4.5.3 Python；各版 README 列出腳本與執行順序。
腳本寫入所在版本資料夾；要保留现有成果，先複製到新的同層資料夾再執行。
v0.1/v0.2 的 Manifold 流程獨立，不是 Blender 版本的相依套件。
