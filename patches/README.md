# patches — 可套用的外部修補

這裡放給外部專案套用的獨立 patch。每個資料夾會說明目標版本、修改原因、套用方式和驗證方法。

## 現有 patch

- [`subtitles-dangling-string-fix/`](subtitles-dangling-string-fix/PATCH.md)：修正 Subtitles 0.6.2 偶發亂碼的懸空字串問題。
  - [修改內容與影響範圍](subtitles-dangling-string-fix/PATCH.md)
  - [套用、建置與回退方式](subtitles-dangling-string-fix/APPLY.md)
  - [靜態驗證腳本](subtitles-dangling-string-fix/tests/check_patch.py)
