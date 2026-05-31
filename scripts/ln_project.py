#!/usr/bin/env python3
"""Utilities for Japanese light novel -> zh-CN translation projects.

This script prepares project memory files, inventories source chapters, chunks text
without external dependencies, and scans translations for high-risk GPT/translationese.
It does not translate; it supports Codex/Antigravity/ChatGPT workflows.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence

TEXT_EXTS = {".txt", ".md", ".markdown"}
IGNORE_DIRS = {".git", "translations", "meta", "qa", "work", "chunks", "node_modules", "__pycache__"}

HIGH_RISK_PATTERNS = [
    ("社会人", "日式概念；按语境改为上班族/已经工作的人/成年人等"),
    ("元气", "默认改为精神/有精神/身体还好/活力等"),
    ("违和感", "默认改为不对劲/别扭/异样/不自然/哪里怪等"),
    ("重要的事物", "抽象僵硬；改为重要的东西/珍视的人或事/心里最要紧的东西"),
    ("心情复杂", "高频翻译腔；改为五味杂陈/一时说不清/心里乱等"),
    ("果然如此", "高频套话；按语气改为这样啊/难怪/我懂了等"),
    ("说不定", "高频套话；按语气改为也许/或许/可能/没准等"),
    ("全部都由我", "疑似 GPT 腔；检查是否应改为我会听着/我受得住/我陪你"),
    ("身体擅自", "日式结构；改为身体先一步反应/身体记起"),
    ("鲜明地重放", "僵硬搭配；改为清楚回响/重新涌上耳底等"),
    ("悲痛喊声", "抽象说明；改成具体声音/哭腔/尖叫"),
    ("距离感", "人物关系里高风险；改为疏远/相处分寸/那道线"),
    ("即便如此", "强让步连接词；检查是否可改为还是/仍然/却或直接删去"),
    ("尽管如此", "强让步连接词；检查是否确有庄重让步功能"),
    ("就在这时", "场景推进模板；普通接续优先直接写动作"),
    ("那一瞬间", "瞬间模板；检查是否可直接写反应动作"),
]

CONNECTIVE_DENSITY_RULES = [
    ("可是", 5, "强转折高频；优先删、弱化或改成动作承接"),
    ("不过", 5, "补充/转折高频；检查是否可省略"),
    ("但是", 5, "强转折高频；小说叙述中可用但不要模板化"),
    ("即便如此", 3, "强让步高频；多数场景改为还是/仍然/却"),
    ("尽管如此", 3, "强让步高频；检查是否过于书面"),
    ("就在这时", 3, "场景推进模板高频；普通动作接续不需要"),
    ("那一瞬间", 4, "瞬间模板高频；可直接写反应"),
    ("一瞬间", 5, "瞬间模板高频；检查是否重复"),
    ("这一次", 5, "承接词高频；上下文清楚时可省"),
    ("不知什么时候", 3, "日式叙述垫步；可改为回过神来/这才发现或删"),
]

CONNECTIVE_START_RE = re.compile(r"^\s*(可是|不过|但是|然而|即便如此|尽管如此|就在这时|就在这时候|那一瞬间|一瞬间|这一次|这时|不知什么时候|回过神来)")

# Not banned words. These are density alarms for the Chinese-only edit pass.
CONNECTIVE_TERMS = [
    "不过", "可是", "然而", "即便如此", "即使如此", "尽管如此", "但", "但是",
    "就在这时", "这时", "那一瞬间", "下一刻", "随后", "接着", "然后",
    "于是", "因此", "所以", "也正因为如此", "不知什么时候", "回过神来时",
]
PARAGRAPH_OPENERS = [
    "不过", "可是", "然而", "即便如此", "即使如此", "尽管如此",
    "就在这时", "这时", "那一瞬间", "下一刻", "随后", "接着", "然后", "于是", "因此", "所以",
]

ABSTRACT_CATCH_RE = re.compile(r"接住(?![了住到]?\s*(?:球|杯|刀|剑|身体|人|孩子|书|东西|包|雨|花|钥匙|手机|拳头|攻击|箭|石头))")

TEMPLATES = {
    "series_bible.md": """# Series Bible\n\n## Work\n- Title:\n- Volume:\n- Genre:\n- POV:\n- Target reader:\n\n## Characters\n| Name | JP name/reading | Role | First appearance | Voice | Address forms | Notes |\n|---|---|---|---|---|---|---|\n\n## Relationships\n| Pair | Relationship | Current state | Address pattern | Change history |\n|---|---|---|---|---|\n\n## Timeline\n| Chapter | Event | Continuity note |\n|---|---|---|\n\n## Motifs / Repeated Lines\n| Source | zh-CN handling | First use | Note |\n|---|---|---|---|\n""",
    "style_guide.zh-CN.md": """# 轻小说简体中文风格指南\n\n## 总体译风\n- 自然、清楚、有画面、无 GPT 腔。\n\n## 称呼与敬语\n\n## 连接词与节奏控制\n- 段首连接词：少用“可是/不过/然而/即便如此”，只在强转折时保留。\n- 时间推进词：少用“就在这时/那一瞬间/下一刻”，只给突发动作或情绪爆点。\n- 内心独白：优先用短句、空行和动作承接，不用逻辑词解释每一步。\n\n## 反 GPT 腔禁用/慎用\n- 社会人：\n- 抽象接住：\n- 元气：\n- 违和感：\n\n## 标点与排版\n- 对话使用中文引号“”。\n""",
    "continuity_notes.md": """# Continuity Notes\n\n## Current Arc State\n\n## Address-Form Changes\n\n## Open Foreshadowing\n\n## Emotional Motifs\n\n## Resolved Issues\n""",
    "open_issues.md": """# Open Issues\n\n| ID | Severity | Location | Issue | Current decision | Needs review |\n|---|---|---|---|---|---|\n""",
}

GLOSSARY_HEADER = [
    "source", "reading", "category", "approved_zh_cn", "allowed_variants",
    "banned_variants", "first_appearance", "character_or_entity",
    "register_or_voice_note", "cultural_note", "status",
]

GLOSSARY_ROWS = [
    ["社会人", "しゃかいじん", "common_noun", "上班族|已经工作的人|成年人", "职场人|社会人士", "社会人", "", "", "与学生相对/成熟责任按语境选词", "", "approved"],
    ["受け止める", "うけとめる", "verb", "接受|听进去|理解|承受|认真听|陪你一起扛|我受得住", "接住(仅物理义)", "接住(抽象义)", "", "", "情感/忠告/告白场景慎译", "", "approved"],
    ["大丈夫", "だいじょうぶ", "pragmatic_phrase", "没事|没事吧|我没事|不用了|可以|放心|撑得住", "没关系", "固定译成没关系", "", "", "按语用功能判断", "", "approved"],
    ["違和感", "いわかん", "noun", "不对劲|别扭|异样|不自然|哪里怪", "违和感", "违和感(默认)", "", "", "除非讨论概念本身", "", "approved"],
]

@dataclass
class SourceFile:
    path: Path
    rel: str
    size: int
    chars: int
    lines: int
    sha1: str
    title: str


def read_text(path: Path) -> str:
    for enc in ("utf-8-sig", "utf-8", "cp932", "shift_jis", "gb18030"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def display_path(path: str | Path, start: str | Path | None = None) -> str:
    """Return a readable path without failing across Windows drives."""
    raw = Path(path)
    base = Path(start) if start is not None else Path.cwd()
    try:
        return os.path.relpath(str(raw), start=str(base))
    except ValueError:
        return str(raw)

def natural_key(s: str) -> list[object]:
    # Handles Arabic numbers in file names such as 第01话 and 第10话.
    parts = re.split(r"(\d+)", s)
    key: list[object] = []
    for part in parts:
        if part.isdigit():
            key.append(int(part))
        else:
            key.append(part.lower())
    return key


def iter_text_files(source: Path) -> list[Path]:
    files: list[Path] = []
    for path in source.rglob("*"):
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in TEXT_EXTS:
            files.append(path)
    return sorted(files, key=lambda p: natural_key(str(p.relative_to(source))))


def file_sha1(path: Path) -> str:
    h = hashlib.sha1()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def first_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        stripped = line.strip().lstrip("#").strip()
        if stripped:
            return stripped[:120]
    return fallback


def inventory(source: Path) -> list[SourceFile]:
    result: list[SourceFile] = []
    for path in iter_text_files(source):
        text = read_text(path)
        result.append(SourceFile(
            path=path,
            rel=str(path.relative_to(source)),
            size=path.stat().st_size,
            chars=len(text),
            lines=text.count("\n") + 1 if text else 0,
            sha1=file_sha1(path),
            title=first_title(text, path.stem),
        ))
    return result


def cmd_init(args: argparse.Namespace) -> int:
    root = Path(args.root)
    for d in [args.source, "translations", "meta", "qa", "work"]:
        (root / d).mkdir(parents=True, exist_ok=True)
    meta = root / "meta"
    for name, content in TEMPLATES.items():
        fp = meta / name
        if not fp.exists():
            write_text(fp, content)
    glossary = meta / "glossary.csv"
    if not glossary.exists():
        glossary.parent.mkdir(parents=True, exist_ok=True)
        with glossary.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(GLOSSARY_HEADER)
            writer.writerows(GLOSSARY_ROWS)
    print(f"initialized project at {root}")
    return 0


def cmd_inventory(args: argparse.Namespace) -> int:
    source = Path(args.source)
    items = inventory(source)
    data = [item.__dict__ | {"path": str(item.path)} for item in items]
    out = Path(args.output)
    write_text(out, json.dumps(data, ensure_ascii=False, indent=2))
    print(f"wrote {len(items)} source entries to {out}")
    return 0


def split_blocks(text: str) -> list[str]:
    text = text.replace("\r\n", "\n").replace("\r", "\n").strip("\n")
    if not text:
        return []
    # Prefer blank-line paragraphing; preserve scene separators and headings.
    blocks = re.split(r"\n\s*\n", text)
    return [b.strip("\n") for b in blocks if b.strip()]


def split_long_block(block: str, max_chars: int) -> list[str]:
    if len(block) <= max_chars:
        return [block]
    # Split at Japanese/Chinese sentence boundaries, keeping punctuation.
    sentences = re.split(r"(?<=[。！？!?」』）)])\s*", block)
    chunks: list[str] = []
    buf = ""
    for sent in sentences:
        if not sent:
            continue
        if len(buf) + len(sent) > max_chars and buf:
            chunks.append(buf.strip())
            buf = sent
        else:
            buf += sent
    if buf.strip():
        chunks.append(buf.strip())
    return chunks or [block]


def chunk_text(text: str, max_chars: int) -> list[str]:
    blocks: list[str] = []
    for block in split_blocks(text):
        blocks.extend(split_long_block(block, max_chars))
    chunks: list[str] = []
    buf: list[str] = []
    size = 0
    for block in blocks:
        if size + len(block) > max_chars and buf:
            chunks.append("\n\n".join(buf).strip())
            buf = [block]
            size = len(block)
        else:
            buf.append(block)
            size += len(block)
    if buf:
        chunks.append("\n\n".join(buf).strip())
    return chunks


def cmd_chunk(args: argparse.Namespace) -> int:
    src = Path(args.file)
    text = read_text(src)
    chunks = chunk_text(text, args.max_chars)
    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    manifest = []
    for i, chunk in enumerate(chunks, 1):
        name = f"chunk-{i:03d}.md"
        write_text(outdir / name, chunk + "\n")
        manifest.append({"id": f"{src.stem}-{i:03d}", "file": name, "chars": len(chunk)})
    write_text(outdir / "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
    print(json.dumps({"source": str(src), "chunks": len(chunks), "output_dir": str(outdir)}, ensure_ascii=False))
    return 0


def line_snippet(line: str, term: str, width: int = 60) -> str:
    idx = line.find(term)
    if idx < 0:
        return line.strip()[: width * 2]
    start = max(0, idx - width)
    end = min(len(line), idx + len(term) + width)
    prefix = "…" if start else ""
    suffix = "…" if end < len(line) else ""
    return prefix + line[start:end].strip() + suffix


def count_cjk_chars(text: str) -> int:
    return len(re.findall(r"[\u3400-\u9fff]", text))


def paragraph_opener(paragraph: str) -> str | None:
    stripped = paragraph.strip().lstrip("　 ")
    for opener in sorted(PARAGRAPH_OPENERS, key=len, reverse=True):
        if stripped.startswith(opener):
            return opener
    return None


def scan_connective_density(path: Path, text: str) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    chars = max(count_cjk_chars(text), 1)
    # Density alarms are intentionally conservative. They should trigger review, not automatic rewriting.
    for term in CONNECTIVE_TERMS:
        count = text.count(term)
        if count >= 6 and count / chars * 1000 >= 1.2:
            findings.append({
                "file": str(path),
                "line": 0,
                "hit": f"连接词过密:{term}x{count}",
                "note": "不是禁用；请做中文-only 节奏审校，删除无必要转折/时间推进词",
                "snippet": f"全文约{chars}个中文字符，{term}出现{count}次",
            })
    paragraphs = re.split(r"\n\s*\n", text)
    opener_counts: dict[str, int] = {}
    for para in paragraphs:
        opener = paragraph_opener(para)
        if opener:
            opener_counts[opener] = opener_counts.get(opener, 0) + 1
    for opener, count in sorted(opener_counts.items(), key=lambda kv: (-kv[1], kv[0])):
        if count >= 3:
            findings.append({
                "file": str(path),
                "line": 0,
                "hit": f"段首连接词重复:{opener}x{count}",
                "note": "段首反复显得模板化；能用句号/动作/停顿承接时优先删改",
                "snippet": f"{opener} 作为段首出现 {count} 次",
            })
    return findings


def scan_file(path: Path) -> list[dict[str, object]]:
    text = read_text(path)
    findings: list[dict[str, object]] = []
    for line_no, line in enumerate(text.splitlines(), 1):
        for term, note in HIGH_RISK_PATTERNS:
            if term in line:
                findings.append({"file": str(path), "line": line_no, "hit": term, "note": note, "snippet": line_snippet(line, term)})
        if "接住" in line and ABSTRACT_CATCH_RE.search(line):
            findings.append({"file": str(path), "line": line_no, "hit": "接住(疑似抽象义)", "note": "检查是否应改为接受/听着/承受/陪你一起扛", "snippet": line_snippet(line, "接住")})
    findings.extend(scan_connective_density(path, text))
    return findings


def cmd_scan(args: argparse.Namespace) -> int:
    target = Path(args.path)
    files: list[Path]
    if target.is_file():
        files = [target]
    else:
        files = [p for p in target.rglob("*") if p.is_file() and p.suffix.lower() in TEXT_EXTS]
    findings: list[dict[str, object]] = []
    for fp in sorted(files, key=lambda p: natural_key(str(p))):
        findings.extend(scan_file(fp))
    lines = ["# High-Risk Translationese Scan", "", f"Scanned files: {len(files)}", f"Findings: {len(findings)}", ""]
    if findings:
        lines.append("| file | line | hit | note | snippet |")
        lines.append("|---|---:|---|---|---|")
        for f in findings:
            rel = display_path(str(f["file"]), start=os.getcwd())
            snippet = str(f["snippet"]).replace("|", "\\|")
            note = str(f["note"]).replace("|", "\\|")
            line_display = "summary" if f["line"] == 0 else str(f["line"])
            lines.append(f"| {rel} | {line_display} | {f['hit']} | {note} | {snippet} |")
    else:
        lines.append("No high-risk phrases found by deterministic scan. This is not a substitute for literary review.")
    out = Path(args.output)
    write_text(out, "\n".join(lines) + "\n")
    print(f"wrote scan report with {len(findings)} findings to {out}")
    return 0


def cmd_context_pack(args: argparse.Namespace) -> int:
    source = Path(args.source)
    meta = Path(args.meta)
    items = inventory(source)
    lines = ["# Context Pack", "", "This file is a deterministic scaffold. Fill summaries, character notes, and decisions during pre-reading.", "", "## Source Order", ""]
    lines.append("| # | file | chars | title |")
    lines.append("|---:|---|---:|---|")
    for i, item in enumerate(items, 1):
        lines.append(f"| {i} | {item.rel} | {item.chars} | {item.title.replace('|', '/')} |")
    lines += ["", "## Pre-Reading Notes", "", "### Work Overview", "", "### Main Characters", "", "### Relationships", "", "### Timeline", "", "### Address Forms", "", "### Repeated Lines / Motifs", "", "### High-Risk Terms", "", "### Open Issues", ""]
    for name in ["series_bible.md", "style_guide.zh-CN.md", "glossary.csv", "continuity_notes.md", "open_issues.md"]:
        fp = meta / name
        status = "exists" if fp.exists() else "missing"
        lines.append(f"- `{fp}`: {status}")
    write_text(Path(args.output), "\n".join(lines) + "\n")
    print(f"wrote context pack to {args.output}")
    return 0


def translation_candidates(src_rel: str) -> list[str]:
    stem = Path(src_rel).stem
    return [
        f"{stem}.zh-CN.md",
        f"{stem}.zh-CN.txt",
        f"{src_rel}.zh-CN.md",
        f"{src_rel}.zh-CN.txt",
    ]


def cmd_manifest(args: argparse.Namespace) -> int:
    src = Path(args.source)
    trans = Path(args.translations)
    items = inventory(src)
    lines = ["# Translation Manifest", "", "| # | source | chars | translation | status |", "|---:|---|---:|---|---|"]
    missing = 0
    for i, item in enumerate(items, 1):
        found = None
        for cand in translation_candidates(item.rel):
            p = trans / cand
            if p.exists():
                found = p
                break
        status = "ok" if found else "missing"
        if not found:
            missing += 1
        lines.append(f"| {i} | {item.rel} | {item.chars} | {found.relative_to(trans) if found else ''} | {status} |")
    lines += ["", f"Missing translations: {missing}"]
    write_text(Path(args.output), "\n".join(lines) + "\n")
    print(f"wrote manifest to {args.output}; missing={missing}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Japanese light novel zh-CN translation project utilities")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init", help="create project directories and meta templates")
    s.add_argument("--root", default=".")
    s.add_argument("--source", default="source")
    s.set_defaults(func=cmd_init)

    s = sub.add_parser("inventory", help="write source inventory json")
    s.add_argument("--source", default="source")
    s.add_argument("--output", default="meta/source_inventory.json")
    s.set_defaults(func=cmd_inventory)

    s = sub.add_parser("chunk", help="split a source file into chunks")
    s.add_argument("file")
    s.add_argument("--output-dir", required=True)
    s.add_argument("--max-chars", type=int, default=4500)
    s.set_defaults(func=cmd_chunk)

    s = sub.add_parser("scan", help="scan translation files for high-risk phrases")
    s.add_argument("path")
    s.add_argument("--output", default="qa/high_risk_scan.md")
    s.set_defaults(func=cmd_scan)

    s = sub.add_parser("context-pack", help="create deterministic context pack scaffold")
    s.add_argument("--source", default="source")
    s.add_argument("--meta", default="meta")
    s.add_argument("--output", default="meta/context_pack.md")
    s.set_defaults(func=cmd_context_pack)

    s = sub.add_parser("manifest", help="compare source files with translation outputs")
    s.add_argument("--source", default="source")
    s.add_argument("--translations", default="translations")
    s.add_argument("--output", default="qa/translation_manifest.md")
    s.set_defaults(func=cmd_manifest)
    return p


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
