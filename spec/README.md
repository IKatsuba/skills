# 📐 Specification Skills

Skills for specification-driven development workflow.

## 📝 Specification Creation

| Skill | Description |
|-------|-------------|
| `spec:requirements` | 📋 Generate structured requirements documents with user stories and acceptance criteria |
| `spec:design` | 🏗️ Create technical design documents with architecture diagrams and interfaces |
| `spec:tasks` | ✅ Build implementation plans with tracked tasks and checkboxes |

## ⚡ Task Execution

| Skill | Description |
|-------|-------------|
| `spec:do-all` | 🔄 Execute all pending tasks sequentially |
| `spec:do-next` | ▶️ Run the next pending task |
| `spec:do-task` | 🎯 Run a specific task by number (e.g., `spec:do-task 1.2`) |

## 🎯 Workflow

### Phase 1: Specification

1. **`/spec:requirements <name>`** → Creates `.specs/<name>/requirements.md`
2. **`/spec:design <name>`** → Creates `.specs/<name>/design.md`
3. **`/spec:tasks <name>`** → Creates `.specs/<name>/tasks.md`

### Phase 2: Implementation

4. **`/spec:do-all <name>`** — Execute all tasks automatically
5. **`/spec:do-next <name>`** — Execute tasks one at a time with review
6. **`/spec:do-task <name> <number>`** — Execute a specific task

## 📁 Output Structure

```
.specs/
└── <spec-name>/
    ├── requirements.md   # 📋 User stories and acceptance criteria
    ├── design.md         # 🏗️ Architecture, components, interfaces
    └── tasks.md          # ✅ Implementation plan with checkboxes
```

## 📦 Installation

```bash
# All spec skills
npx add-skill ikatsuba/skills/spec

# Individual skills
npx add-skill ikatsuba/skills --skill spec:requirements
npx add-skill ikatsuba/skills --skill spec:design
npx add-skill ikatsuba/skills --skill spec:tasks
npx add-skill ikatsuba/skills --skill spec:do-all
npx add-skill ikatsuba/skills --skill spec:do-next
npx add-skill ikatsuba/skills --skill spec:do-task
```
