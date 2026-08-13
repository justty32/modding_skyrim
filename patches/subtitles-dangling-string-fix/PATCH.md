# Subtitles 0.6.2 dangling-string fix

## 目標專案

- 專案：WaterFace/Subtitles
- 上游：https://github.com/WaterFace/subtitles
- 基底 commit：`a378de88aceac3c6a11d84d50760378784b03ab0`（0.6.2）
- CommonLibSSE-NG submodule：`b17ee0a896cb4235a44060b071fbb5f1a7ee34a5`

## 修改類型

Bug 修正。`SubtitleManager.cpp` 原本把 `bigSubtitle.str()` 臨時字串的
`c_str()` 指標交給 `RE::GFxValue`；臨時字串在該 statement 結束時銷毀，
下一行 `Invoke` 因此可能讀到 dangling pointer。

## 影響範圍

- 行為修改：`src/SubtitleManager.cpp` 一處。
- 不修改字幕合併、顏色、格式、INI 或 UI 資產。
- `cmake`、CLibUtil 與 CommonLibSSE-NG 的額外調整只用於 Linux
  clang-cl/xwin 交叉編譯，不屬於產品行為 patch。

## 預期結果

合併後的字幕字串在 `GFxValue` 建立及 `ShowSubtitle` 呼叫期間保持有效，
消除同一字幕偶爾顯示亂碼的未定義行為。

## 分析依據

- 上游 `src/SubtitleManager.cpp` 的臨時字串使用方式。
- 固定版 CommonLibSSE-NG `GFxValue(const char*)` 只保存傳入指標，不複製字串。
- 使用者實機現象為繁中字型已正常、但多行字幕仍偶發亂碼，與 dangling
  pointer 的非決定性特徵一致。

