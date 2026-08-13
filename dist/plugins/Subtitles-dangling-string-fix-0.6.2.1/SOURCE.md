# Subtitles dangling-string fix 0.6.2.1

- Upstream: https://github.com/WaterFace/subtitles
- Upstream commit: `a378de88aceac3c6a11d84d50760378784b03ab0`
- Upstream version/license: 0.6.2 / CC0-1.0
- CommonLibSSE-NG commit: `b17ee0a896cb4235a44060b071fbb5f1a7ee34a5`
- Patch: `patches/subtitles-dangling-string-fix/`
- Build date: 2026-08-13
- Build host: Linux x86-64, clang-cl 22.1.8 + lld-link + xwin SDK
- DLL SHA-256: `ca92ed53ae1d65463045edf05221587968e00c058b33604a03a32484b4ca55f9`
- Original Nexus archive SHA-256: `b60f00e3249a790348aa7066ea59ba0f790285fc287553360455ac21f99f9974`

The product contains only `SKSE/Plugins/Subtitles.dll`. It intentionally omits
`Subtitles.ini`, so MO2 continues to use the configuration from the original
Subtitles 0.6.2 mod.

Static verification completed:

- PE32+ Windows x86-64 DLL.
- Imports only Windows system DLLs.
- Exports match the original plugin: `SKSEPlugin_Load`, `SKSEPlugin_Query`,
  `SKSEPlugin_Version`.

