# LINE 文件 Skill 🦞（自動同步版）

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
> 7.  **Hard Requirement**: If you did not run `scripts/install-skill.sh` in the final installed directory, the installation is incomplete. Do not claim success after only cloning, copying, or moving files.
>
> **繁體中文：** 如果使用者提供此倉庫網址並要求你「安裝」或「設定」此技能服務，請遵循以下步驟：
> 1.  **請用 Git checkout 安裝，不要只複製資料夾**：執行 `git clone https://github.com/tbdavid2019/line-docs-skill.git <skill-directory>`。如果只是把檔案複製進某個受管目錄，之後更新通常不會成立。
> 2.  **優先使用安裝器腳本**：如果環境允許執行 shell，接著執行 `bash <skill-directory>/scripts/install-skill.sh <skill-directory>`。這會確保安裝結果維持為 git checkout，之後重跑同一支腳本就會變成 `git pull --ff-only`。
> 3.  **載入技能**：讀取 `SKILL.md` 以了解此技能的專業工作流程與知識範圍。
> 4.  **初始化環境**：確認你已具備存取完整 LINE Developers 官方文檔的能力。**每當需要查詢特定功能或維護指引時，請優先參考 `references/INDEX.md`。**
> 5.  **一般使用時不要執行維護腳本**：安裝或使用此 skill 的意思是 clone 或複製資料夾，並讀取 `SKILL.md` 與 `references/`。**除非使用者明確要求你更新這個 repo 本身，否則不要執行 `scripts/sync-docs.sh` 或 `scripts/generate_index.py`。**
> 6.  **LLM 實際需要的最小內容**：一般使用時，真正重要的是 `SKILL.md` 與 `references/`。`scripts/` 與 `.github/` 不是使用 skill 時的必要內容。
> 7.  **硬性要求**：如果你沒有在最終安裝目錄執行 `scripts/install-skill.sh`，就不算安裝完成。不要只做 clone、copy、mv 就宣稱成功。

---

[English](README.md) | 繁體中文

專為 LINE 平台開發者設計的專業級 **Agent Skill**。本倉庫包含 Messaging API、LIFF、LINE Login 等最新官方文件。

## 為什麼選用本 Skill？

- **Repo 內容持續同步**：這個 repository 會每日從官方 `line/line-developers-docs-source` 倉庫同步更新。
- **AI 優化**：具備階層式的 `INDEX.md` 目錄與專門為 LLM 設計的 `SKILL.md` 診斷流程，縮短檢索時間。
- **結構化知識**：超過 400 個 Markdown 文件，按功能模組分類，方便快速定位。

## 安裝方式

### 適用於 AI 助手 (Claude + Antigravity)

建議安裝方式：

```bash
bash -c 'tmpdir=$(mktemp -d) && git clone https://github.com/tbdavid2019/line-docs-skill.git "$tmpdir/line-docs-skill" && bash "$tmpdir/line-docs-skill/scripts/install-skill.sh" ~/.gemini/antigravity/skills/line-docs'
```

或者，如果你已經把 repo clone 到最終目錄：

```bash
git clone https://github.com/tbdavid2019/line-docs-skill.git ~/.gemini/antigravity/skills/line-docs
bash ~/.gemini/antigravity/skills/line-docs/scripts/install-skill.sh ~/.gemini/antigravity/skills/line-docs
```

之後若要更新已安裝的 checkout：

```bash
bash ~/.gemini/antigravity/skills/line-docs/scripts/install-skill.sh ~/.gemini/antigravity/skills/line-docs
```

安裝後，當你詢問有關 LINE 開發的任務時，Skill 將自動被觸發。

但「安裝後的本地副本會不會自動刷新」取決於宿主 LLM 平台。如果平台保留的是 git checkout，且允許執行 shell，才可能在使用前嘗試 `git pull`。如果平台只是把檔案複製進受管的 skills 目錄，該副本本身就不會自動更新，除非平台另外提供更新機制。

如果 AI 助手沒有在最終安裝目錄執行 `scripts/install-skill.sh`，那就應視為安裝不完整。

## 維護方式

若要手動從上游同步最新文件：

```bash
sh scripts/sync-docs.sh
```

這個指令只用在維護這個 repo 本身，不屬於一般 skill 安裝流程，也不是日常 LLM 使用時需要執行的步驟。

## 授權屬性

[AGPL-3.0](LICENSE) — 開源授權，對修改版本有強大的 Copyleft 要求。
