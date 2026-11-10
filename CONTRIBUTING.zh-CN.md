# 贡献说明

[English](CONTRIBUTING.md) · [中文说明](README.zh-CN.md)

欢迎用 Issue 和 Pull Request 提交事实勘误、失效链接、编码错误，以及含糊的安装说明。

## 保持方法本身完整

英文和中文两套 Skill 是方法原文。它们描述的是同一套 7 步、4 个架构档位、21 种模式、21 个评审维度和交接契约。

- 方法上的修改应同时体现在两种语言里，并且含义一致。
- 不要用增加 Agent、框架或分数来「简化」设计。Skill 要求这些选择要么写清理由，要么省略。
- 文档里不要写示例分数。配套示例保持「说明性、未评分」。
- 框架的维护状态或 API 事实发生变化时可以更新说明。请写明出处和阅读日期。除非某次修改记录了真实测试及其限度，否则 ADK、LangGraph、CrewAI 和 AutoGen 仍应写成映射骨架。

## 保持 Skill 能被发现

`SKILL.md` frontmatter 的 `name` 必须与 Skill 目录名一致：`agent-system-design` 或 `agent-system-design-cn`。`description` 必须不超过 1024 个字符。英文描述已经接近这个上限。

中文文件名保持 UTF-8。新增链接时，目标必须是真实文件名，包括中文字符。不要把 `__MACOSX`、`.DS_Store` 或 AppleDouble 文件加回来。

## 这个仓库不需要的内容

运行时编排、网站、发版自动化、托管部署、徽章、下载计数和星标活动都不在范围内。框架章节里的代码块是 Skill 文档的一部分。仓库检查不会执行它们，贡献也不应为了运行它们而增加依赖。

## 打开 Pull Request 之前

```bash
python3 scripts/validate_repo.py
```

脚本只使用 Python 标准库。如果你有意修改导入的 Skill 文件，请按检查器读取的 SHA-256 字段重新生成 `scripts/source-manifest.json`，并说明字节为什么改变。无意的改动应让检查失败。

不要改写 [LICENSE](LICENSE)。其中的版权是 Skyler，2026。geniusjia666 对仓库的所有权是另一件事，写在 README 里。
