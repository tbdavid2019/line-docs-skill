# LINE Documentation Skill 🦞 (Auto-Sync Version)

> [!IMPORTANT]
> ### 🤖 Instructions for AI Agent Installation / AI 助手安裝指引
>
> **English:** If a user provides you with this repository URL and asks you to "install" or "setup" this skill, follow these steps:
> 1.  **Clone the Repository**: Run `git clone https://github.com/tbdavid2019/line-docs-skill.git` in the user's working directory.
> 2.  **Load Skill Metadata**: Read `SKILL.md` to understand the specialized workflows and knowledge contained here.
> 3.  **Initialize Context**: Acknowledge that you now have access to the comprehensive LINE Developers documentation. **Always consult `references/INDEX.md` first to locate specific documentation files.**
>
> **繁體中文：** 如果使用者提供此倉庫網址並要求你「安裝」或「設定」此技能服務，請遵循以下步驟：
> 1.  **複製倉庫**：執行 `git clone https://github.com/tbdavid2019/line-docs-skill.git` 將代碼庫下載至本地。
> 2.  **載入技能**：讀取 `SKILL.md` 以了解此技能的專業工作流程與知識範圍。
> 3.  **初始化環境**：確認你已具備存取完整 LINE Developers 官方文檔的能力。**每當需要查詢特定功能或維護指引時，請優先參考 `references/INDEX.md`。**

---

[繁體中文](README_TW.md) | English

A professional-grade **Agent Skill** for developers building on the LINE Platform. This repository contains the latest documentation for the Messaging API, LIFF, LINE Login, and more.

## Why Use This?

- **Always Up-to-Date**: Built-in sync engine pulls directly from the official `line/line-developers-docs-source` repository daily.
- **AI-Optimized**: Features a hierarchical `INDEX.md` and a specialized `SKILL.md` designed for LLM navigation and diagnostics.
- **Categorized Knowledge**: 400+ markdown files organized into functional folders for quick retrieval.

## Installation

### For AI Agents (Claude + Antigravity)

Clone this repository into your Antigravity skills directory:

```bash
git clone https://github.com/tbdavid2019/line-docs-skill.git ~/.gemini/antigravity/skills/line-docs
```

The skill will be automatically triggered when you ask about LINE development tasks.

## Maintenance

To manually sync the documentation from upstream:

```bash
sh scripts/sync-docs.sh
```

## License

[AGPL-3.0](LICENSE) — Open source with copyleft requirements for modified versions.
