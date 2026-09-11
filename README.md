# FV300 掃描頭內構模型

Olympus FV300 共軛焦掃描頭的開蓋內構重建，依 2026-09-10 拍攝的實機照片建模。
**不是原廠 CAD，也不是可列印或可成像的複製件。**

## 開啟

雙擊 `viewer.html`，會轉到目前版本的離線 3D 預覽（拖曳旋轉、縮放、拆解、查看單一零件）。

## 版本

| 版本 | 目錄 | 依據 |
| --- | --- | --- |
| v0.1 | `v01_scanhead/` | 三張開蓋斜拍照片 |
| v0.2（目前） | `v02_overhead_revision/` | 新增俯視照，修正配置 |

`CURRENT_VERSION.txt` 記錄目前狀態。`v02_overhead_revision/comparison.html` 可並排比對兩版。

## 每個版本的檔案

- `viewer.html` — 離線 3D 預覽
- `build_model.py` — 參數化 Python／Manifold 建模原始碼
- `model.json` — 產生出的幾何
- `parts.csv` — 零件清單
- `preview*.png` — 靜態預覽
- `validation.json` — 網格檢查結果

根目錄的 `20260910_*.jpg` 是建模依據的原始照片。

## 界線

- 尺寸、隱藏面、齒數與部分機構功能**未核實**
- 模型單位為暫定值，**不是實機尺寸**
- IX71 本體未建模
- 缺資料處留空，不建立臆測光路
- 未實體試印，非列印成品

## 重現建模

`build_model.py` 需要 Python 與 Manifold；原專案使用相鄰目錄的 `.deps`，該目錄未進版控，需自行安裝相依套件。
