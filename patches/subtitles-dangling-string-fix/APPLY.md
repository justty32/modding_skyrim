# APPLY.md — Subtitles 0.6.2 dangling-string fix

## 摘要

保存 `bigSubtitle.str()` 的結果直到 Scaleform `Invoke` 完成，避免偶發亂碼。

## 前置條件

- 目標 repo：`https://github.com/WaterFace/subtitles`
- checkout：`a378de88aceac3c6a11d84d50760378784b03ab0`
- 初始化 submodule：`git submodule update --init --recursive`
- 套用前確認工作樹乾淨，且 `src/SubtitleManager.cpp` 仍含原始三行模式。

## 套用步驟

1. 在目標 repo 根目錄執行：

   ```sh
   git apply /path/to/subtitles-dangling-string-fix/src/SubtitleManager.cpp.patch
   ```

2. 執行靜態驗證：

   ```sh
   python /path/to/subtitles-dangling-string-fix/tests/check_patch.py \
     src/SubtitleManager.cpp
   ```

3. 使用目標專案既有的 Windows MSVC preset 編譯，或依下方已驗證的 Linux
   clang-cl/xwin 說明建置。

4. 確認成品是 x86-64 PE DLL，且仍匯出 `SKSEPlugin_Load`、
   `SKSEPlugin_Query`、`SKSEPlugin_Version`。

## Linux clang-cl/xwin 建置備註

本次已成功用 workspace 的 `projects/agent-bridge/cmake/` triplet/toolchain 與
`ports/directxtk` overlay 建置。上游原始碼另需下列 host-only 相容處理：

- `cmake/Version.rc.in` 的檔名大小寫。
- CLibUtil 下載內容的 `CLIBUtil`／include 使用的 `ClibUtil` 大小寫。
- 定義 `UNICODE`、`_UNICODE` 與空的 `FMT_CONSTEVAL`。
- 套用 workspace 既有的 CommonLibSSE-NG clang `operator delete` patch。
- RC include path 指向 xwin SDK，並設 `VCPKG_APPLOCAL_DEPS=OFF`。

這些是 Linux host 相容調整；用 Visual Studio/MSVC 時不需要。

## 回退方式

- 原始碼：`git apply -R src/SubtitleManager.cpp.patch`。
- MO2：停用獨立的 `Subtitles 0.6.2 Dangling String Fix` 覆蓋 mod；原版
  `Subtitles` 與它的 INI 不需變更。

## 已知限制

- 已完成靜態檢查與 Windows x64 交叉編譯。
- 遊戲內需以 Skyrim 1.6.1170 測試連續、多 NPC、多行字幕，確認不再重現。

