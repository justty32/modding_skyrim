# CHIM 對 ModForge 有什麼可借鑑？

最值得借的是「另一套 reader 驗輸出」「驗收後才發布」「每包附可追溯 manifest」。ModForge 已有 spec authoring、headless CLI、JSON catalog 與完整組包，沒有理由換掉 Mutagen 或重造這些能力。這是研究候選，尚未裁定開工。版本、方法與授權見 [研究入口](../README.md)。

## 先扣除已有能力

見 [已有能力與研究邊界](modforge-fit/README.md#先扣除已有能力)。

## 1. 用獨立結構 reader 驗證寫出的 plugin

見 [一般出貨驗收候選](modforge-fit/output-gates.md#1-用獨立結構-reader-驗證寫出的-plugin)。

## 2. 一般出貨路徑保住最後一份可用產物

見 [一般出貨驗收候選](modforge-fit/output-gates.md#2-一般出貨路徑保住最後一份可用產物)。

## 3. 一般 package 附可追溯 manifest

見 [一般出貨驗收候選](modforge-fit/output-gates.md#3-一般-package-附可追溯-manifest)。

## 不值得順勢擴張的部分

見 [已有能力與研究邊界](modforge-fit/README.md#不值得順勢擴張的部分)。
