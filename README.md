# 🛠️ Skills

> A collection of skills for Claude Code, Codex, Cursor and OpenCode to supercharge your specification-driven development workflow!

## 🚀 Quick Start

```bash
npx add-skill ikatsuba/skills
```

That's it! You're ready to go.

---

## 📦 Installation Options

### Install specific skills

Pick only what you need:

```bash
npx add-skill ikatsuba/skills --skill spec:requirements
npx add-skill ikatsuba/skills --skill spec:design
npx add-skill ikatsuba/skills --skill spec:tasks
npx add-skill ikatsuba/skills --skill spec:do-all
npx add-skill ikatsuba/skills --skill spec:do-next
npx add-skill ikatsuba/skills --skill spec:do-task
npx add-skill ikatsuba/skills --skill utils:changelog
```

### Global installation

Want skills everywhere? Go global:

```bash
npx add-skill ikatsuba/skills -g
```

### Browse available skills

```bash
npx add-skill ikatsuba/skills --list
```

---

## ✨ Available Skills

### 📝 Specification Creation

| Skill | Description |
|-------|-------------|
| `spec:requirements` | 📋 Generate structured requirements documents with user stories and acceptance criteria |
| `spec:design` | 🏗️ Create technical design documents with architecture diagrams and interfaces |
| `spec:tasks` | ✅ Build implementation plans with tracked tasks and checkboxes |

### ⚡ Task Execution

| Skill | Description |
|-------|-------------|
| `spec:do-all` | 🔄 Execute all pending tasks sequentially — sit back and relax! |
| `spec:do-next` | ▶️ Run the next pending task — perfect for incremental progress |
| `spec:do-task` | 🎯 Run a specific task by number (e.g., `spec:do-task 1.2`) |

### 🧰 Utility

| Skill | Description |
|-------|-------------|
| `utils:changelog` | 📰 Generate beautiful, human-readable changelogs for product, marketing, and support teams |

---

## 🎯 Workflow

These skills support a complete specification-driven development workflow:

### Phase 1: Specification 📐

Build your blueprint:

1. **`/spec:requirements <name>`** → Creates `.specs/<name>/requirements.md`
2. **`/spec:design <name>`** → Creates `.specs/<name>/design.md`
3. **`/spec:tasks <name>`** → Creates `.specs/<name>/tasks.md`

### Phase 2: Implementation 🔨

Let the magic happen:

4. **`/spec:do-all <name>`** — Execute all tasks automatically
5. **`/spec:do-next <name>`** — Execute tasks one at a time with review
6. **`/spec:do-task <name> <number>`** — Execute a specific task

### Changelog Generation 📰

Keep your stakeholders in the loop:

```bash
/utils:changelog last week           # Changes from the past 7 days
/utils:changelog since 2024-01-01    # All changes since a date
/utils:changelog v1.0.0..v1.1.0      # Changes between releases
```

---

## 📁 Documents Structure

```
.specs/
└── <spec-name>/
    ├── requirements.md   # 📋 User stories and acceptance criteria
    ├── design.md         # 🏗️ Architecture, components, interfaces
    └── tasks.md          # ✅ Implementation plan with checkboxes
```

---

## 📄 License

MIT — Use it, share it, love it! ❤️
