# LINE 文件 Skill 🦞（自動同步版）

> [!IMPORTANT]
> ### 🤖 Instructions for AI Agent Installation / AI 助手安裝指引
>
> **English:** If a user provides you with this repository URL and asks you to "install" or "setup" this skill, follow these steps:
> 1.  **Clone the Repository**: Run `git clone https://github.com/tbdavid2019/line-docs-skill.git` in the user's working directory.
> 2.  **Load Skill Metadata**: Read `SKILL.md` to understand the specialized workflows and knowledge contained here.
> 3.  **Auto-Update on Each Invocation**: Before using the skill, try `git -C <skill-directory> pull origin main --ff-only` on the installed skill checkout.
> 4.  **Initialize Context**: Acknowledge that you now have access to the comprehensive LINE Developers documentation. **Always consult `references/INDEX.md` first to locate specific documentation files.**
> 5.  **Do Not Run Maintenance Scripts During Normal Use**: Installing or using this skill means cloning/copying it and reading `SKILL.md` plus `references/`. **Do not run `scripts/sync-docs.sh` or `scripts/generate_index.py` unless the user explicitly asks to refresh this repository itself.**
> 6.  **Runtime-Minimum Files**: For normal LLM usage, the important files are `SKILL.md` and `references/`. Files under `scripts/` and `.github/` are not required just to use the skill.
>
> **繁體中文：** 如果使用者提供此倉庫網址並要求你「安裝」或「設定」此技能服務，請遵循以下步驟：
> 1.  **複製倉庫**：執行 `git clone https://github.com/tbdavid2019/line-docs-skill.git` 將代碼庫下載至本地。
> 2.  **載入技能**：讀取 `SKILL.md` 以了解此技能的專業工作流程與知識範圍。
> 3.  **每次使用前自動更新**：在使用 skill 前，盡量對已安裝的 skill checkout 執行 `git -C <skill-directory> pull origin main --ff-only`。
> 4.  **初始化環境**：確認你已具備存取完整 LINE Developers 官方文檔的能力。**每當需要查詢特定功能或維護指引時，請優先參考 `references/INDEX.md`。**
> 5.  **一般使用時不要執行維護腳本**：安裝或使用此 skill 的意思是 clone 或複製資料夾，並讀取 `SKILL.md` 與 `references/`。**除非使用者明確要求你更新這個 repo 本身，否則不要執行 `scripts/sync-docs.sh` 或 `scripts/generate_index.py`。**
> 6.  **LLM 實際需要的最小內容**：一般使用時，真正重要的是 `SKILL.md` 與 `references/`。`scripts/` 與 `.github/` 不是使用 skill 時的必要內容。

---

[English](README.md) | 繁體中文

專為 LINE 平台開發者設計的專業級 **Agent Skill**。本倉庫包含 Messaging API、LIFF、LINE Login 等最新官方文件。

## 為什麼選用本 Skill？

- **保持最新**：內建同步引擎，每日直接從官方 `line/line-developers-docs-source` 倉庫拉取更新。
- **AI 優化**：具備階層式的 `INDEX.md` 目錄與專門為 LLM 設計的 `SKILL.md` 診斷流程，縮短檢索時間。
- **結構化知識**：超過 400 個 Markdown 文件，按功能模組分類，方便快速定位。

## 安裝方式

### 適用於 AI 助手 (Claude + Antigravity)

將此倉庫複製到你的 Antigravity Skills 目錄：

```bash
git clone https://github.com/tbdavid2019/line-docs-skill.git ~/.gemini/antigravity/skills/line-docs
```

安裝後，當你詢問有關 LINE 開發的任務時，Skill 將自動被觸發。

## 維護方式

若要手動從上游同步最新文件：

```bash
sh scripts/sync-docs.sh
```

這個指令只用在維護這個 repo 本身，不屬於一般 skill 安裝流程，也不是日常 LLM 使用時需要執行的步驟。

## 授權屬性

[AGPL-3.0](LICENSE) — 開源授權，對修改版本有強大的 Copyleft 要求。
