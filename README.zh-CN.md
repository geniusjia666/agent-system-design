# Agent 系统设计

**先判断需不需要多 Agent，再设计它们如何协作。**

[English](README.md)

这个仓库用中文和英文发布同一套 Agent 设计方法。它要解决的是设计问题：先判断这件事是否真的需要 Agent，再选择够用的最简架构，把角色、契约、交接、防护和评测写下来，然后才谈框架。

本仓库的 GitHub 所有者是 [geniusjia666](https://github.com/geniusjia666)。许可证沿用仓库里已有的 MIT 许可证。导入过程见 [来源说明](PROVENANCE.md)。

## 用它可以产出什么

把它作为 Agent Skill 使用时，助手应交付设计文档，而不是交付一个正在运行的系统。一份完成的设计包括：

- 选定的架构档位，以及更简单的档位为什么不够。
- 每个 Agent 或工作流步骤的任务契约：输入、输出结构、完成标准、停止条件。
- 只保留该步需要的工具、上下文和记忆。
- 宿主能够校验的交接：七要素派发（dispatch）、结构化结果（handoff）、门禁（gate）。
- 该档位需要的人类介入、失败处理、预算和安全边界。
- 至少覆盖主路径、边界和失败的评测方案。
- 对适用维度的自检。文档分数不是成功率，也不是发布许可。

配套示例是一条固定的**代码生成、审查、修复**流程。它说明为什么这是「带隔离审查的工作流」，而不是增加 Agent 的理由。示例是说明性的，没有运行，也没有性能分数。见 [中文示例](examples/zh-CN/code-generation-review-fix.md)。

## 内容要点

两个语言版本描述的是同一套方法：

| 内容 | 位置 |
|---|---|
| 7 步：需求、架构、单体设计、编排、加固、评测、交付 | `SKILL.md` |
| 4 个档位：提示词、工作流、单 Agent、多 Agent | `SKILL.md` 与架构选型一章 |
| 21 种模式，并注明设计落点和自检维度 | `references/10-*` |
| 21 维设计自检；只有真正评审时才打 0–5 分 | `assets/` 中的自检清单 |
| 交接契约：`dispatch`、`handoff`、`gate` | `assets/` 中的 JSON 模板 |

模式编号和自检维度编号不是同一套顺序。索引里写明了这一点。评审报告的维度列使用自检编号。

## 边界

这是设计方法和设计评审辅助。Skill 原文写明：它不负责运行时编排、业务代码重构、仓库 Harness 化、部署或发布。

Google ADK、LangGraph、CrewAI、AutoGen 的说明是把同一份契约映射到这些 API 的文档骨架，不是已测试的集成。日期和限制见 [框架映射](#框架映射)。

## 目录

```text
skills/agent-system-design/        英文 Skill。目录名与 frontmatter 的 name 一致。
skills/agent-system-design-cn/     中文 Skill。目录名与 frontmatter 的 name 一致。
examples/en/                       英文示例提示词和一份完整的说明性设计
examples/zh-CN/                    中文示例提示词和同一份说明性设计
scripts/validate_repo.py           本地检查。只用 Python 标准库。
scripts/source-manifest.json       每个导入的 Skill 文件的 SHA-256
PROVENANCE.md                      压缩包如何导入
CONTRIBUTING.zh-CN.md              如何提议修改
LICENSE                            MIT，保持仓库初始提交中的文本
```

每个 Skill 目录都是一份自包含的 Agent Skill：

```text
skill-name/
├── SKILL.md
├── references/     # 按需阅读；01 到 10 共十章
└── assets/         # 设计模板、交接 JSON、自检清单
```

中文版的章节和素材文件名保持原始中文名，并以 UTF-8 存放。该 Skill 内部链接指向这些文件名。

## 安装

这里的安装，是把 Skill 目录放到你的 Agent 宿主已经在扫描的位置。本仓库不会向任何产品注册自己，克隆仓库也不会自动启用 Skill。

下列步骤依据 [Agent Skills 规范](https://agentskills.io/specification)。该页在 2026-11-10 为本次发布阅读过：

1. 选择一种语言。每种 Skill 都是完整的。不必同时加载两种。
2. 目录名必须与 `SKILL.md` 里的 `name` 相同。
   - 英文：[skills/agent-system-design](skills/agent-system-design/SKILL.md)（`name: agent-system-design`）
   - 中文：[skills/agent-system-design-cn](skills/agent-system-design-cn/SKILL.md)（`name: agent-system-design-cn`）
3. 把该目录复制或符号链接到宿主文档指定的技能目录。规范定义的是目录和 frontmatter，没有为所有产品规定同一个安装路径。
4. 直接要求一份设计、一次架构选择，或对已有设计的评审。[示例提示词](examples/zh-CN/sample-prompts.md) 只是起点，不是规定说法。

```bash
# 把 DESTINATION 换成宿主实际扫描的目录。
# 最后一级目录名必须保持 Skill 名称不变。
mkdir -p DESTINATION
cp -R skills/agent-system-design DESTINATION/agent-system-design
# 中文版：
cp -R skills/agent-system-design-cn DESTINATION/agent-system-design-cn
```

### Cursor：文档中有记载，本仓库未实测

Cursor 的 Agent Skills 页面 <https://cursor.com/docs/skills> 于 2026-11-10 阅读。该页列出的发现目录是：

| 位置 | 该页所写的范围 |
|---|---|
| `.agents/skills/` | 项目 |
| `.cursor/skills/` | 项目 |
| `~/.agents/skills/` | 用户本机 |
| `~/.cursor/skills/` | 用户本机 |

同一页还写到，Cursor 为兼容会加载 `.claude/skills/`、`.codex/skills/`、`~/.claude/skills/` 和 `~/.codex/skills/`，并且 GitHub 仓库不会自行变成已安装的 Skill，除非打包成插件。直接做法仍是复制 Skill 目录。

这次发布没有启动 Cursor、Claude Code 或 Codex，也没有把 Skill 装进上述任何目录。这里没有这些产品的认证或兼容性结论。上表只是对该文档页面的引用；使用前请对照最新页面自行确认。

## 使用

1. 按上面的步骤安装一个 Skill 目录。
2. 新系统：要求助手按 Skill 从需求走到设计文档。如果普通代码就够，Skill 会在架构选型处停止，不填写完整模板。
3. 已有设计：只要求评估报告。完整模板留给新设计和改造。
4. 某一步需要时，再让助手打开 `references/` 和 `assets/`。Skill 故意把这些文件留到那时再读。
5. 契约确定之后，框架章节才作为可选的映射说明。

支持该规范的宿主会先加载 `name` 和 `description`，请求匹配时再加载 `SKILL.md`，指令指向某个参考文件时再读取该文件。超出这一描述的产品行为，本仓库没有测量。

## 框架映射

[中文章节](skills/agent-system-design-cn/references/09-框架落地映射.md) 与 [英文章节](skills/agent-system-design/references/09-framework-implementation-mapping.md) 把同一条「生成、审查、修复」契约映射到四个库。两章都写明：这是 Python 构建骨架，生产运行器不在范围内，写这一章时没有安装这些库。

章节记录的是阅读日期，不是本仓库的实测结果。这次发布没有重新安装这些包，也没有重新审计上游仓库。下面是那两章自己的说法，不是新的兼容性测试：

- 补读日期为 2026-11-01；该章称官方材料归档于 2026-10-30。
- 当日包索引上的候选锁定版本：`google-adk==2.13.0`、`langgraph==1.2.19`、`crewai==1.15.33`、`autogen-core==0.7.5`。该章写明这些版本尚待兼容性验证。
- ADK：该章称官方文档以 2.0 图工作流替代传统模板工作流，且 2.13.0 源码把 `SequentialAgent` 标为弃用。骨架仍保留 `SequentialAgent`，以便对照既有系统。新项目应核对当前官方图文档。
- LangGraph 与 CrewAI：该章称类型化状态、任务输出和框架回调只是载体。业务校验、权限和接纳仍在宿主。它也指出归档中部分旧的 CrewAI 结果属性已经过时。
- AutoGen：该章称当前官方仓库已归档、不再维护、不提供安全修复。保留 Core 映射是为了理解既有系统和研究；新的生产选型应另选。旧 0.2、Core 与 AgentChat 的 API 不要混用。后继框架明确不在该章范围内。

不要把这些版本号说成是本仓库测试过的版本。

## 检查

在克隆下来的仓库中运行：

```bash
python3 scripts/validate_repo.py
```

脚本只使用 Python 标准库。它检查 UTF-8、JSON 解析、`SKILL.md` frontmatter、本地 Markdown 链接和标题锚点、7 步 / 4 档 / 21 模式 / 21 维 / 交接契约这些标记，以及导入的 Skill 文件是否与 SHA-256 清单一致。它不会执行 Skill 里的代码示例。

## 贡献

勘误、链接修复和有出处的更新请用 Pull Request。[贡献说明（中文）](CONTRIBUTING.zh-CN.md)。同时影响两种语言的方法修改，请让中英文保持对齐。

## 星标

如果这份清单帮你判断出不必再增加 Agent，可以为仓库点一颗星，让别人更容易找到它。星标不能证明某份设计是对的。本项目也不用星标交换支持、评审或兼容性承诺。

## 许可证

[MIT 许可证](LICENSE)。文件中的版权声明是 Copyright (c) 2026 Skyler。这次发布没有改动该文件。
