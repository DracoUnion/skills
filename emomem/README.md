# EmoMem

基于 Reverie `src/memory` 模块的跨会话长期记忆命令行工具 + Claude Code skill。

- 数据默认存在 `~/.emomem/`（SQLite 事实库 `metadata.db`），可以用 `--data-dir` 覆盖。
- 语义召回依赖本机缓存的 `sentence-transformers` 模型；缺失时自动降级为词法召回，离线可用。
- skill 定义在 `SKILL.md`。

## 快速开始

```bash
# 在仓库根目录运行
python .skill/emomem/bin/emomem.py add "用户喜欢手冲咖啡"
python .skill/emomem/bin/emomem.py search 咖啡
python .skill/emomem/bin/emomem.py remember "用户生日是3月2日"
python .skill/emomem/bin/emomem.py list
python .skill/emomem/bin/emomem.py export ~/memory-backup.json
python .skill/emomem/bin/emomem.py import ~/memory-backup.json --replace
```

所有命令支持 `--json` 输出，便于被脚本和 Claude Code 解析。
常用命令清单见 `SKILL.md`。

## 数据与隐私

- 数据明文存放在你指定的目录（默认 `~/.emomem`），与桌面端 `data/memory` 隔离。
- 身份锚点（`My name is EmoMem …`）是 CLI 自身的中性身份，不是用户记忆。
- 备份文件是标准 JSON 数组，用 `export` 生成、`import` 恢复。

## 测试

```bash
python -m pytest tests/test_emomem_cli.py -q
```

测试使用临时 `--data-dir`，不会触碰 `~/.emomem` 或 `data/memory`。