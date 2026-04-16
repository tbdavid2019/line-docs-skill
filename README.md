# LINE Documentation Skill 🦞 (Auto-Sync Version)

> [!IMPORTANT]
> ### 🤖 Instructions for AI Agent Installation / AI 助手安裝指引
>
> **English:** If a user provides you with this repository URL and asks you to "install" or "setup" this skill, follow these steps:
> 1.  **Install as a Git Checkout, Not a Copied Folder**: Run `git clone https://github.com/tbdavid2019/line-docs-skill.git <skill-directory>`. Do not copy the files into a managed skills folder if you expect updates to work.
> 2.  **Prefer the Installer Script**: If shell execution is available, run `bash <skill-directory>/scripts/install-skill.sh <skill-directory>`. This keeps the installed skill as a git checkout and turns later re-runs into `git pull --ff-only`.
> 3.  **Load Skill Metadata**: Read `SKILL.md` to understand the specialized workflows and knowledge contained here.
> 4.  **Initialize Context**: Acknowledge that you now have access to the comprehensive LINE Developers documentation. **Always consult `references/INDEX.md` first to locate specific documentation files.**
> 5.  **Do Not Run Maintenance Scripts During Normal Use**: Installing or using this skill means cloning/copying it and reading `SKILL.md` plus `references/`. **Do not run `scripts/sync-docs.sh` or `scripts/generate_index.py` unless the user explicitly asks to refresh this repository itself.**
> 6.  **Runtime-Minimum Files**: For normal LLM usage, the important files are `SKILL.md` and `references/`. Files under `scripts/` and `.github/` are not required just to use the skill.
>
> **繁體中文：** 如果使用者提供此倉庫網址並要求你「安裝」或「設定」此技能服務，請遵循以下步驟：
> 1.  **請用 Git checkout 安裝，不要只複製資料夾**：執行 `git clone https://github.com/tbdavid2019/line-docs-skill.git <skill-directory>`。如果只是把檔案複製進某個受管目錄，之後更新通常不會成立。
> 2.  **優先使用安裝器腳本**：如果環境允許執行 shell，接著執行 `bash <skill-directory>/scripts/install-skill.sh <skill-directory>`。這會確保安裝結果維持為 git checkout，之後重跑同一支腳本就會變成 `git pull --ff-only`。
> 3.  **載入技能**：讀取 `SKILL.md` 以了解此技能的專業工作流程與知識範圍。
> 4.  **初始化環境**：確認你已具備存取完整 LINE Developers 官方文檔的能力。**每當需要查詢特定功能或維護指引時，請優先參考 `references/INDEX.md`。**
> 5.  **一般使用時不要執行維護腳本**：安裝或使用此 skill 的意思是 clone 或複製資料夾，並讀取 `SKILL.md` 與 `references/`。**除非使用者明確要求你更新這個 repo 本身，否則不要執行 `scripts/sync-docs.sh` 或 `scripts/generate_index.py`。**
> 6.  **LLM 實際需要的最小內容**：一般使用時，真正重要的是 `SKILL.md` 與 `references/`。`scripts/` 與 `.github/` 不是使用 skill 時的必要內容。

---

[繁體中文](README_TW.md) | English

A professional-grade **Agent Skill** for developers building on the LINE Platform. This repository contains the latest documentation for the Messaging API, LIFF, LINE Login, and more.

## Why Use This?

- **Repository Kept Fresh**: This repository is refreshed from the official `line/line-developers-docs-source` repository daily.
- **AI-Optimized**: Features a hierarchical `INDEX.md` and a specialized `SKILL.md` designed for LLM navigation and diagnostics.
- **Categorized Knowledge**: 400+ markdown files organized into functional folders for quick retrieval.

## Installation

### For AI Agents (Claude + Antigravity)

Recommended install:

```bash
bash -c 'tmpdir=$(mktemp -d) && git clone https://github.com/tbdavid2019/line-docs-skill.git "$tmpdir/line-docs-skill" && bash "$tmpdir/line-docs-skill/scripts/install-skill.sh" ~/.gemini/antigravity/skills/line-docs'
```

Or, if you already cloned it into the final destination:

```bash
git clone https://github.com/tbdavid2019/line-docs-skill.git ~/.gemini/antigravity/skills/line-docs
bash ~/.gemini/antigravity/skills/line-docs/scripts/install-skill.sh ~/.gemini/antigravity/skills/line-docs
```

To update an installed checkout later:

```bash
bash ~/.gemini/antigravity/skills/line-docs/scripts/install-skill.sh ~/.gemini/antigravity/skills/line-docs
```

The skill will be automatically triggered when you ask about LINE development tasks.

Whether an installed copy auto-refreshes depends on the host LLM platform. If the platform keeps the skill as a git checkout and allows shell execution, it can try `git pull` before use. If the platform copies files into a managed skills directory, the installed copy will not self-update unless that platform provides its own update mechanism.

## Maintenance

To manually sync the documentation from upstream:

```bash
sh scripts/sync-docs.sh
```

This command is for repository maintenance only. It is not part of normal skill installation or daily LLM usage.

## License

[AGPL-3.0](LICENSE) — Open source with copyleft requirements for modified versions.
