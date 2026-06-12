# bookshelf 个人书架

一个简单的命令行工具，用于管理自己读过 / 想读的书。

本项目同时是一个 **多人协作 Git 工作流的练习场**，覆盖：
Issue 驱动、Draft PR、CI、Tag 发版、Revert、Hotfix、Cherry-pick、Stash、Reflog 等场景。

## 安装（开发环境）

```bash
pip install -e .
```

## 使用

```bash
bookshelf --help
```

## 可用命令

<!-- COMMANDS:BEGIN -->
- `bookshelf add <书名> [--author 作者] [--tag 标签]` —— 添加一本书（小张）
- `bookshelf list` —— 列出所有书（小李）
- `bookshelf aearch` ——— 搜索 （小王）
<!-- COMMANDS:END -->

## 贡献流程

1. **先建 Issue** 描述要做的事
2. **拉分支**：`feat/<issue编号>-<简短描述>`，例如 `feat/3-add-search`
3. 在 `bookshelf/commands/<name>.py` 里实现命令
4. 在 `bookshelf/cli.py` 注册命令
5. 在本文件的"可用命令"区追加一行说明
6. 开 PR，在 PR 描述里写 `Closes #<issue编号>`，合并后会自动关闭 Issue

## 项目结构

```
bookshelf/
├── bookshelf/
│   ├── cli.py          # 命令行入口
│   ├── storage.py      # 数据存储层（共享）
│   └── commands/       # 各命令模块
├── tests/              # 单元测试
└── .github/workflows/  # GitHub Actions CI
```
