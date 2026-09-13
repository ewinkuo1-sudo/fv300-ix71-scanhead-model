# FV300／IX71 展示模型

依實機照片與參考資料製作的展示用粗模；不是原廠 CAD。尺寸、隱藏面和部分機構仍為推估。

## 目前版本：Blender 掃描頭粗模 v0.3

- [照片對照與核對頁](v03_blender_blockout_20260913/review.html)（下載 repo 後以瀏覽器開啟）
- [可編輯 Blender 模型](v03_blender_blockout_20260913/FV300_round1.blend)
- [核對紀錄與限制](v03_blender_blockout_20260913/README.md)
- [分件表](v03_blender_blockout_20260913/parts.csv)

79 個獨立物件（73 網格、6 曲線），按區域命名與分組；打包四張內構參考照片。
以 Blender 4.5.3 重新載入模型，檢查五個視角並開啟 GUI。
修正右側調整桿的垂直方向，中央折板改為開口分件。
外框寬為 10 任意單位；所有高度仍為推估，IX71 尚未加入本版本。

## 版本保留

| 版本 | 目錄 | 說明 |
| --- | --- | --- |
| v0.1 | v01_scanhead/ | 三張斜拍照片的初版 |
| v0.2 | v02_overhead_revision/ | 加入俯視照；舊離線互動 viewer |
| v0.3 | v03_blender_blockout_20260913/ | Blender 獨立重建粗模，等待比例確認 |

根目錄 viewer.html 連到 v0.3 核對頁；舊版互動 viewer 保留在各版目錄。
根目錄 20260910_*.jpg 為實機照片。

## 重現

v0.3 使用 Blender Python：以 Blender 執行 build_blockout.py，再執行 inspect_saved_model.py 重新載入檢查。
腳本會寫入所在版本資料夾；要保留現有成果，請先複製到新的同層資料夾再執行。
v0.1/v0.2 的 build_model.py 使用 Manifold 等外部相依套件，不是 v0.3 的相依套件。

