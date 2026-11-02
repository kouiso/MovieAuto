#!/usr/bin/env python3
"""公開内容チェック — issue/PR/コメント本文を規則で照合する。

規則ファイル: .github/content-guard-rules.txt
  一行一則 `規則名<TAB>正規表現`（# 始まりはコメント）。
  依頼元指定の禁止語はこのファイルに追加する。

出力は規則名・行番号・件数だけ。命中した文字そのものは出さない。
usage: content_guard.py <rules-file> <text-file>
exit: 0=clean / 1=hit / 2=usage error
"""
import re
import sys


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: content_guard.py <rules-file> <text-file>", file=sys.stderr)
        return 2
    rules_path, text_path = sys.argv[1], sys.argv[2]

    rules = []
    for raw in open(rules_path, encoding="utf-8"):
        line = raw.rstrip("\n")
        if not line or line.startswith("#"):
            continue
        name, _, pattern = line.partition("\t")
        if not pattern:
            continue
        try:
            rules.append((name.strip(), re.compile(pattern)))
        except re.error as exc:
            print(f"rules: bad regex '{name}': {exc}", file=sys.stderr)
            return 2

    hits = []
    with open(text_path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            for name, pat in rules:
                count = len(pat.findall(line))
                if count:
                    hits.append((name, lineno, count))

    for name, lineno, count in hits:
        print(f"rule:{name} line:{lineno} count:{count}")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
