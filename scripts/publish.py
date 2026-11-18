"""Check the newest entries and rebuild README.md and archive/README.md.

Each archive entry lives in archive/YYYY-MM-DD-slug/ with a post.md that starts
with a front-matter block (key: value lines between --- fences). The newest
entry becomes the repo README; relative links in it are rewritten so they
resolve from the repo root.

Entries from SERIES_START on must pass the checks in CLAUDE.md: evidence notes,
a short third-person post, no banned words, no em dashes. The script refuses to
publish if any fail, so nothing reaches the README without them.

    python scripts/publish.py           # check, then rebuild
    python scripts/publish.py --check   # check only
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "archive"
TAGLINE = "one settled finding, drawn clearly, every day"

SERIES_START = "2026-11-18"          # first entry of the settled-findings series
FINDING_TYPES = {"effect", "dose-response", "moderator", "association", "comparison", "mechanism"}
REQUIRED_META = ("date", "title", "slug", "topic", "finding", "source", "doi", "chart", "summary")
EVIDENCE_FIELDS = ("Finding:", "Source:", "Design:", "Key numbers:", "Corroboration:", "Wording check:",
                   "Limits:", "Fact-check:")
REQUIRED_FILES = ("post.md", "evidence.md", "analysis.py", "chart.png", "chart.svg", "data/SOURCES.md")
MAX_WORDS = 100                      # prose between the image and the Source line
MAX_TITLE_WORDS = 9
MAX_SUMMARY_CHARS = 180

FIRST_PERSON = re.compile(r"\b(I|I'm|I've|I'd|I'll|me|my|mine|myself|we|We|we're|we've|our|Our|ours|us|ourselves)\b")
BANNED = [
    "striking", "stark", "notably", "crucially", "underscore", "highlights", "delve", "landscape", "tapestry",
    "game-changer", "game changer", "the story here", "in a world where", "it's not just", "fascinating",
    "remarkable", "remarkably", "surprisingly", "shocking", "mind-blowing", "groundbreaking", "revolutionary",
    "key takeaway", "why it matters", "let's", "here's", "turns out", "dive into", "a reminder that",
]
LEGACY_NOTE = ("The first ten entries looked for new patterns in public data rather than charting settled "
               "findings. They are kept for the record.")


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


def prose_of(body: str) -> str:
    """The post's own sentences: everything that isn't the headline, image, source block or links."""
    keep = []
    for line in body.splitlines():
        s = line.strip()
        if not s or s.startswith(("#", "![", "**Source", "**Evidence", "[Data]", "<sub>", "---")):
            continue
        keep.append(s)
    return " ".join(keep)


def check_entry(d: Path, meta: dict, body: str, prev: dict | None) -> list[str]:
    p = []
    say = lambda msg: p.append(f"{d.name}: {msg}")  # noqa: E731

    for key in REQUIRED_META:
        if not meta.get(key):
            say(f"front matter missing '{key}'")
    if meta.get("finding") and meta["finding"] not in FINDING_TYPES:
        say(f"'finding' must be one of {sorted(FINDING_TYPES)}")
    for f in REQUIRED_FILES:
        if not (d / f).exists():
            say(f"missing {f}")

    ev = d / "evidence.md"
    if ev.exists():
        text = ev.read_text()
        missing = [f for f in EVIDENCE_FIELDS if f not in text]
        if missing:
            say(f"evidence.md lacks {', '.join(missing)}")
        corro = text.split("Corroboration:", 1)[-1].split("Wording check:", 1)[0]
        if corro.lower().count("doi") + corro.count("http") < 2:
            say("evidence.md needs at least two corroborating sources with a DOI or link")

    title, summary = meta.get("title", ""), meta.get("summary", "")
    if len(title.split()) > MAX_TITLE_WORDS:
        say(f"title has {len(title.split())} words (max {MAX_TITLE_WORDS})")
    if len(summary) > MAX_SUMMARY_CHARS:
        say(f"summary has {len(summary)} characters (max {MAX_SUMMARY_CHARS})")
    if not re.search(rf"^# {re.escape(title)}\s*$", body, re.M):
        say("first heading must match the title")

    prose = prose_of(body)
    n = len(re.findall(r"[A-Za-z0-9][\w'.,%–-]*", prose))
    if n > MAX_WORDS:
        say(f"post prose is {n} words (max {MAX_WORDS})")
    for name, text in (("title", title), ("summary", summary), ("post", prose)):
        if m := FIRST_PERSON.search(text):
            say(f"first person in {name}: '{m.group(0)}'")
        low = text.lower()
        for w in BANNED:
            if w in low:
                say(f"banned phrase in {name}: '{w}'")
        if "!" in text:
            say(f"exclamation mark in {name}")
    if not re.search(r"^\*\*Source:\*\*.*(doi\.org|https?://)", body, re.M):
        say("needs a '**Source:**' line with a DOI or link")
    if not re.search(r"^\*\*Evidence:\*\*", body, re.M):
        say("needs an '**Evidence:**' line")
    for target in ("(data/)", "(analysis.py)", "(evidence.md)"):
        if target not in body:
            say(f"links line must link {target}")

    for f in ("post.md", "evidence.md", "chart.svg", "data/SOURCES.md"):
        fp = d / f
        if fp.exists() and "—" in fp.read_text(errors="ignore"):
            say(f"em dash in {f}")

    if prev:
        if prev.get("finding") == meta.get("finding"):
            say(f"finding type '{meta.get('finding')}' repeats the previous entry")
        if prev.get("topic", "").lower() == meta.get("topic", "").lower():
            say(f"topic '{meta.get('topic')}' repeats the previous entry")
    return p


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
    series = [e for e in entries if e[1]["date"] >= SERIES_START]
    legacy = [e for e in entries if e[1]["date"] < SERIES_START]

    problems = []
    for i, (d, meta, body) in enumerate(series):
        problems += check_entry(d, meta, body, series[i - 1][1] if i else None)
    if problems:
        raise SystemExit("checks failed:\n  " + "\n  ".join(problems))
    print(f"checks passed for {len(series)} entr{'y' if len(series) == 1 else 'ies'}")
    if "--check" in sys.argv:
        return

    d, meta, body = entries[-1]
    rel = d.relative_to(ROOT).as_posix()
    n = len(entries)
    earlier = [e for e in series[:-1]][-3:]
    prev = (" · ".join(f"[{m['title']}]({e.relative_to(ROOT).as_posix()}/post.md)" for e, m, _ in reversed(earlier))
            + " · ") if earlier else ""
    readme = (
        f"<sub>**pix** · {TAGLINE} · No. {n} · {meta['date']} · {meta['topic']} · [archive →](archive/)</sub>\n\n"
        + rewrite_links(body, rel).rstrip()
        + "\n\n---\n\n"
        + f"<sub>{'Previously: ' if earlier else ''}{prev}[full archive](archive/) · [how this works](CLAUDE.md)</sub>\n"
    )
    (ROOT / "README.md").write_text(readme)

    def row(e: Path, m: dict) -> str:
        p = e.relative_to(ARCHIVE).as_posix()
        meta_line = m["topic"] + (f" · {m['source']}" if m.get("source") else "")
        return (f"| {m['date']} | <a href=\"{p}/post.md\"><img src=\"{p}/{m['chart']}\" width=\"180\"></a> "
                f"| **[{m['title']}]({p}/post.md)**<br><sub>{meta_line}</sub><br>{m['summary']} |")

    head = "| Date | | Finding |\n|---|---|---|\n"
    index = (
        "# pix archive\n\n"
        f"{len(series)} settled finding{'' if len(series) == 1 else 's'}, newest first. Each folder holds the post, "
        "the chart, the evidence notes, the code and the data.\n\n"
        + head + "\n".join(row(e, m) for e, m, _ in reversed(series)) + "\n"
    )
    if legacy:
        index += (f"\n## Earlier series\n\n{LEGACY_NOTE}\n\n| Date | | Analysis |\n|---|---|---|\n"
                  + "\n".join(row(e, m) for e, m, _ in reversed(legacy)) + "\n")
    (ARCHIVE / "README.md").write_text(index)
    print(f"published {d.name} (No. {n})")


if __name__ == "__main__":
    main()
