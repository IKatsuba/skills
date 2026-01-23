# 🧰 Utility Skills

General-purpose utility skills for development workflow.

## ✨ Available Skills

| Skill | Description |
|-------|-------------|
| `utils:changelog` | 📰 Generate beautiful, human-readable changelogs for product, marketing, and support teams |

## 📰 Changelog Generation

Transform your git history into human-readable changelogs for non-technical stakeholders.

### Usage

```bash
/utils:changelog last week           # Changes from the past 7 days
/utils:changelog since 2024-01-01    # All changes since a date
/utils:changelog v1.0.0..v1.1.0      # Changes between releases
```

### Features

- Analyzes git commit history
- Groups changes by category (features, fixes, improvements)
- Transforms technical commits into user-facing descriptions
- Perfect for product, marketing, and support teams

## 📦 Installation

```bash
# All utility skills
npx add-skill ikatsuba/skills/utils

# Individual skills
npx add-skill ikatsuba/skills --skill utils:changelog
```
