# Contributing to oh-my-lazybones

## 开发环境

```bash
git clone git@github.com:Samuel-lzyb/oh-my-lazybones.git
cd oh-my-lazybones
cp .env.example .env
pip install -r server/requirements.txt
pip install -e cli/
```

## Commit 规范

```
feat: 新功能
fix: Bug 修复
docs: 文档更新
refactor: 代码重构
test: 测试相关
chore: 构建/工具
```

## PR 流程

1. Fork 仓库
2. 创建 feature 分支
3. 提交代码（遵循 commit 规范）
4. 确保 CI 通过（lint + test）
5. 提交 PR，使用 PR 模板

## 代码风格

Python 代码使用 ruff 格式化。