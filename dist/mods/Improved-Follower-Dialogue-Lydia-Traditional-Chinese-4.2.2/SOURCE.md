# Source provenance

## 官方 4.2.2 baseline

- 官方 archive：`Improved Follower Dialogue - Lydia-38473-4-2-2-1722555312.zip`
- archive SHA-256：`b8f6cf7e8e8dabcd1ea3a6b4d44764057dc56e4b8cb8f7386166bf8a3051e7b4`
- `00 Core/ImprovedCompanionsBoogaloo.esp`：1,474,749 bytes，SHA-256
  `b1f7482ba331618aec8194e154f28eb2e0c78c9ca2ce4d2a09e35668c7f85a8d`
- 現役安裝的同名 ESP 與 archive 內 baseline 逐 byte 相同。
- 官方 `ImprovedCompanionsBoogaloo.bsa`：72,365,533 bytes，SHA-256
  `5216db18b82a06362713b398ff8c2d97136a875db7d452bb3d77a1b9ff00416c`
- BSA 內 `scripts/lydiaconfigscriptnew.pex`：6,517 bytes，SHA-256
  `24e78d9d931fe03f34237deea9d578cb59321c827786ff52b63bcc91823e0ef0`。

## 同版簡中語意種子

- archive：`IFD Lydia 4.2.2 CHS and Patches-108986-4-2-2-1722969513.zip`
- SHA-256：`2d2903171f7daec23645c298ac80d13555a9038ddf79b7bd868c002ce7979385`
- 主 ESP：1,469,967 bytes，SHA-256
  `413e3a68f95473f21071f54e8677ad9dd391d7d11f87ccf217917db1f23b4152`
- loose PEX：6,399 bytes，SHA-256
  `eccd5e03af7163eda1bd06ac7918f4da3a193e2c97c2f1cbf7b09e8e403aa09a`。

archive 另有 Bruma、Wyrmstooth、LOTD 三個 patch ESP；本產物沒有採用或重發它們。

## 正中術語來源

Skyrim 原文來自官方 `Skyrim - Interface.bsa`（SHA-256
`5c8d5275eeaaa87eec84c893da8dc3bf977e0197eba86560bb0d1dc651432957`）。正中對照採現役
Skyrim Traditional Chinese 8.20 的三份 `_English` table：

| table | SHA-256 |
|---|---|
| `Skyrim_English.STRINGS` | `ae1cd52056ab4b06e44a30a6e0509feeea4f0ddfd186cc5027b6c5af53a14ef4` |
| `Skyrim_English.DLSTRINGS` | `fd3814b1f2a16b96c6b8adbb18017ad905284435e8a38aaebdbbab904acd0fd5` |
| `Skyrim_English.ILSTRINGS` | `e71d4a1f07c0fae9c4d07ab5ff8ecc15346ba19a4c4f02f75f81b0d77e2c94d9` |

79 個 IFD source English 字串在上述表中有唯一的完全相同原文，因此直接復用該譯文。其餘
1,715 個使用 OpenCC `1.3.2` 的 `s2tw` 設定轉換同版 CHS 種子，再做專案術語正規化。

## 權利與發布邊界

本目錄是私人 load-order 使用的衍生翻譯產物。官方 mod、簡中翻譯與原文字句的權利屬各自作者；
沒有核對 Nexus permissions 與翻譯作者授權前，不應把本包公開再發布。工具與 ledger 用於重建與
審計，不代表取得第三方資產的再散布權。
