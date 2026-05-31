# 整卷翻译工作流

## 输入
- `source/`：日文原文文件，按章节命名。
- 可选：已有 `meta/`、前卷译文、术语表。

## 输出
- `translations/<chapter>.zh-CN.md`
- `qa/<chapter>.qa.md`
- `qa/high_risk_scan.md`
- `qa/translation_manifest.md`
- `qa/volume_consistency_report.md`
- updated `meta/`

## 执行
```bash
python scripts/ln_project.py init --root . --source source
python scripts/ln_project.py inventory --source source --output meta/source_inventory.json
python scripts/ln_project.py context-pack --source source --meta meta --output meta/context_pack.md
```

1. 读取 `meta/context_pack.md`、`meta/style_guide.zh-CN.md`、`meta/glossary.csv`。
2. 建立第一章或首段 style lock。
3. 每章按场景切分，翻译、编辑、中文-only 通读、双语完整性检查。
4. 写入译文和 QA。
5. 更新 `meta/`。
6. 全卷完成后运行：

```bash
python scripts/ln_project.py scan translations --output qa/high_risk_scan.md
python scripts/ln_project.py manifest --source source --translations translations --output qa/translation_manifest.md
```

7. 人工/模型复核跨章一致性，写 `qa/volume_consistency_report.md`。
