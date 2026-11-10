# Provenance / 来源说明

[English README](README.md) · [中文说明](README.zh-CN.md)

## English

The skill files in this repository were imported from two zip archives supplied for publication in [geniusjia666/agent-system-design](https://github.com/geniusjia666/agent-system-design). The archives contained Markdown and JSON only. Nothing in them was executed. `__MACOSX/` entries and AppleDouble `._*` sidecar files were discarded. The content entries did not include `.DS_Store`.

| Archive role | Published directory | Files | What changed |
|---|---|---|---|
| English skill | [skills/agent-system-design](skills/agent-system-design/SKILL.md) | 14 | Placement only. Bytes unchanged. |
| Chinese skill | [skills/agent-system-design-cn](skills/agent-system-design-cn/SKILL.md) | 14 | Bytes unchanged. Root directory renamed. Filenames decoded as UTF-8. |

Chinese names inside the zip were UTF-8 bytes stored without the ZIP UTF-8 flag (general-purpose bit 11). A reader that assumes CP437 shows those names as mojibake. Import decoded the stored name bytes as UTF-8. The resulting names were already Unicode NFC, so no further renaming of chapter files was required. Relative links inside the Chinese skill already used those UTF-8 names; no link text was rewritten.

The Chinese archive's top folder was `agent-system-design_cn`, while `SKILL.md` says `name: agent-system-design-cn`. The [Agent Skills specification](https://agentskills.io/specification) requires `name` to match the parent directory, and allows only lowercase letters, digits, and single hyphens. The published folder is therefore `agent-system-design-cn`. The frontmatter line was not edited.

[scripts/source-manifest.json](scripts/source-manifest.json) stores the SHA-256 and byte size of all 28 skill files (669,481 bytes in total). [scripts/validate_repo.py](scripts/validate_repo.py) fails if a skill file drifts from that record.

[LICENSE](LICENSE) is the MIT license from the repository's initial commit: Copyright (c) 2026 Skyler. It was not rewritten. The skill files do not add a separate author line. The GitHub owner of this repository is geniusjia666. Do not replace the copyright line in `LICENSE` unless the copyright holder does.

Repository README, examples, contribution notes, and the validator were written for this publication. They are not part of the imported skill byte count.

## 中文

本仓库中的 Skill 文件来自为公开发布而提供的两份压缩包，发布位置是 [geniusjia666/agent-system-design](https://github.com/geniusjia666/agent-system-design)。压缩包里只有 Markdown 和 JSON。其中的内容没有被当作脚本执行。`__MACOSX/` 和 AppleDouble `._*` 附属文件已丢弃。内容条目中没有 `.DS_Store`。

| 压缩包 | 发布目录 | 文件数 | 变化 |
|---|---|---|---|
| 英文 Skill | [skills/agent-system-design](skills/agent-system-design/SKILL.md) | 14 | 只改变了存放位置。字节未改。 |
| 中文 Skill | [skills/agent-system-design-cn](skills/agent-system-design-cn/SKILL.md) | 14 | 字节未改。根目录改名。文件名按 UTF-8 解码。 |

中文文件名在 ZIP 中是 UTF-8 字节，但没有设置 ZIP 的 UTF-8 标志（通用位 11）。按 CP437 解读时，这些名字会变成乱码。导入时把存储的文件名字节按 UTF-8 解码。解码后的名字已经是 Unicode NFC，章节文件不需要再改名。中文 Skill 内部的相对链接本来就使用这些 UTF-8 名字，链接文字没有改写。

中文压缩包的顶层目录原名是 `agent-system-design_cn`，而 `SKILL.md` 中的 `name` 是 `agent-system-design-cn`。[Agent Skills 规范](https://agentskills.io/specification) 要求 `name` 与父目录相同，并且只允许小写字母、数字和单个连字符。因此发布目录使用 `agent-system-design-cn`。frontmatter 那一行没有改。

[scripts/source-manifest.json](scripts/source-manifest.json) 记录全部 28 个 Skill 文件的 SHA-256 和字节数（合计 669,481 字节）。[scripts/validate_repo.py](scripts/validate_repo.py) 会在 Skill 文件与该记录不一致时失败。

[LICENSE](LICENSE) 是仓库初始提交中的 MIT 许可证，版权行为 Copyright (c) 2026 Skyler。该文件没有改写。Skill 文件里没有另外的作者行。本仓库的 GitHub 所有者是 geniusjia666。除非版权持有人提出，不要替换 `LICENSE` 里的版权行。

仓库的 README、示例、贡献说明和校验脚本是这次发布时编写的，不计入导入的 Skill 字节数。
