#!/usr/bin/env python3
"""issue/PR 書き方チェック — 必須見出しの有無と記入を文字規則だけで判定する。

issue: 背景 / 今どこまで / 次にやること / 誰の判断待ち / 完了条件
PR:    概要 / 変更内容 / 関連Issue（Closes #N か Refs #N）

usage: check_format.py issue <body-file> | check_format.py pr <body-file>
stdout: 欠けている項目を一行ずつ `missing:<見出し>`。全有なら何も出ない。
exit: 0=ok / 1=missing / 2=usage error
"""
import re
import sys

ISSUE_HEADS = ["背景", "今どこまで", "次にやること", "誰の判断待ち", "完了条件"]
PR_HEADS = ["概要", "変更内容"]
PR_LINK = re.compile(r"(?i)\b(?:Closes|Refs)\s+#\d+")


def heading_filled(body: str, name: str) -> bool:
    m = re.search(
        rf"(?ms)^#+\s*{re.escape(name)}\s*$(.*?)(?=^#+\s|\Z)", body)
    if not m:
        return False
    for line in m.group(1).splitlines():
        s = line.strip()
        if not s or s == "-":
            continue
        if re.match(r"^<!--.*-->\s*$", s):
            continue
        return True
    return False


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[1] not in ("issue", "pr"):
        print("usage: check_format.py issue|pr <body-file>", file=sys.stderr)
        return 2
    kind, path = sys.argv[1], sys.argv[2]
    body = open(path, encoding="utf-8").read()

    missing = []
    if kind == "issue":
        for h in ISSUE_HEADS:
            if not heading_filled(body, h):
                missing.append(h)
    else:
        for h in PR_HEADS:
            if not heading_filled(body, h):
                missing.append(h)
        if not PR_LINK.search(body):
            missing.append("関連Issue")

    for h in missing:
        print(f"missing:{h}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
