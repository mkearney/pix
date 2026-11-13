"""Rebuild README.md (today's post) and archive/README.md (the full index).

Each archive entry lives in archive/YYYY-MM-DD-slug/ and must contain a post.md
with a simple front-matter block (key: value lines between --- fences).
The newest entry becomes the repo README; relative links in it are rewritten
so they resolve from the repo root.

    python scripts/publish.py
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "archive"

# Originality checks (see CLAUDE.md) apply to entries dated on or after this.
CHECKS_FROM = "2026-11-13"
CLAIM_TYPES = {
    "share", "concentration", "equivalence", "gap", "reversal",
    "turning-point", "mechanism", "outlier", "crossover",
}
# Claim types for entries published before the field existed. Published entries
# are never edited, so their types live here.
LEGACY_CLAIMS = {
    "2026-11-08": "concentration",
    "2026-11-09": "equivalence",
    "2026-11-10": "share",
    "2026-11-11": "gap",
    "2026-11-12": "share",
}
PRIOR_ART_FIELDS = ("Naive prediction:", "Searches:", "Closest takes:", "What this adds:")


def parse(post: Path) -> tuple[dict, str]:
    text = post.read_text()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise SystemExit(f"{post}: missing front matter")
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    for key in ("date", "title", "topic", "chart", "summary"):
        if key not in meta:
            raise SystemExit(f"{post}: front matter missing '{key}'")
    return meta, m.group(2).lstrip()


def claim_of(meta: dict) -> str | None:
    return meta.get("claim") or LEGACY_CLAIMS.get(meta["date"])


def check_originality(entries: list) -> None:
    """Refuse new entries that skip the originality checks in CLAUDE.md."""
    problems = []
    for i, (d, meta, _) in enumerate(entries):
        if meta["date"] < CHECKS_FROM:
            continue
        claim = meta.get("claim")
        if claim not in CLAIM_TYPES:
            problems.append(f"{d.name}: 'claim' must be one of {sorted(CLAIM_TYPES)}")
            continue
        prior = d / "prior_art.md"
        if not prior.exists():
            problems.append(f"{d.name}: missing prior_art.md")
        else:
            text = prior.read_text()
            missing = [f for f in PRIOR_ART_FIELDS if f not in text]
            if missing:
                problems.append(f"{d.name}: prior_art.md lacks {', '.join(missing)}")
        earlier = [claim_of(m) for _, m, _ in entries[max(0, i - 6):i]]
        if claim in earlier[-2:]:
            problems.append(f"{d.name}: claim '{claim}' repeats one of the previous two entries")
        if earlier.count(claim) >= 2:
            problems.append(f"{d.name}: claim '{claim}' used twice already in the last seven entries")
    if problems:
        raise SystemExit("originality checks failed:\n  " + "\n  ".join(problems))


def rewrite_links(body: str, prefix: str) -> str:
    """Prefix relative markdown link/image targets with the entry's path."""
    def fix(m: re.Match) -> str:
        target = m.group(2)
        if re.match(r"^(https?:|#|/|mailto:)", target):
            return m.group(0)
        return f"{m.group(1)}({prefix}/{target})"
    return re.sub(r"(!?\[[^\]]*\])\(([^)\s]+)\)", fix, body)


def main() -> None:
    entries = []
    for d in sorted(p for p in ARCHIVE.iterdir() if p.is_dir() and (p / "post.md").exists()):
        meta, body = parse(d / "post.md")
        entries.append((d, meta, body))
    if not entries:
        raise SystemExit("no archive entries found")
    entries.sort(key=lambda e: (e[1]["date"], e[0].name))
    check_originality(entries)

    d, meta, body = entries[-1]
    rel = d.relative_to(ROOT).as_posix()
    n = len(entries)
    readme = (
        f"<sub>**pix** · one visual analysis of the world, every day · "
        f"No. {n} · {meta['date']} · {meta['topic']} · [archive →](archive/)</sub>\n\n"
        + rewrite_links(body, rel).rstrip()
        + "\n\n---\n\n"
        f"<sub>Previously: "
        + " · ".join(f"[{m['title']}]({e.relative_to(ROOT).as_posix()}/post.md)"
                     for e, m, _ in reversed(entries[-4:-1]))
        + ("" if n > 1 else "this is the first one.")
        + " · [full archive](archive/) · [how this works](CLAUDE.md)</sub>\n"
    )
    (ROOT / "README.md").write_text(readme)

    rows = []
    for e, m, _ in reversed(entries):
        p = e.relative_to(ARCHIVE).as_posix()
        rows.append(
            f"| {m['date']} | <a href=\"{p}/post.md\"><img src=\"{p}/{m['chart']}\" width=\"180\"></a> "
            f"| **[{m['title']}]({p}/post.md)**<br><sub>{m['topic']}</sub><br>{m['summary']} |"
        )
    index = (
        "# pix archive\n\n"
        f"{n} visual analyses, newest first. Each folder holds the post, the chart, the code and the data.\n\n"
        "| Date | | Analysis |\n|---|---|---|\n" + "\n".join(rows) + "\n"
    )
    (ARCHIVE / "README.md").write_text(index)
    print(f"published {d.name} ({n} entries)")


if __name__ == "__main__":
    main()
