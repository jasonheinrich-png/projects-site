#!/usr/bin/env python3
"""Privacy scan for the public projects site. Standard library only.

Scans every file that GitHub Pages would publish as content (index.html,
style.css, projects.json) and fails on anything that looks private.

Usage: python3 check_privacy.py        exit 0 = pass, 1 = findings

Deny-list: the names, hostnames and machine names found in the source repos
are stored ONLY as salted SHA-256 hashes of their normalized word sequence,
so this public repository does not itself publish them. The scan hashes
every 1-6 word sequence of the site text and compares. To add a term, run
    python3 check_privacy.py --hash "term to block"
and add the printed hash to deny_hashes.txt (git-ignored; a private copy lives in the
owner's private repository). Keep the plaintext list off
the site and out of Git.
"""
import hashlib
import pathlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGETS = ["index.html", "style.css", "projects.json"]
SALT = "projects-site-denylist:"
TOKEN = re.compile(r"[a-z0-9]+")
MAX_NGRAM = 6

# Regex rules: (name, pattern). Case-insensitive.
RULES = [
    ("IPv4 address", r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    ("private LAN prefix", r"192\.168"),
    ("tailnet/CGNAT prefix", r"\b100\.\d"),
    ("host:port", r"\b[a-z0-9.-]+:\d{2,5}\b"),
    ("bare :port", r"(?<![\w&])[:]\d{2,5}\b"),
    ("tailnet name", r"tailb"),
    ("tailnet domain", r"\.ts\.net"),
    ("Windows machine name", r"DESKTOP-"),
    ("at sign / email", r"@"),
    ("token", r"token"),
    ("key=", r"key\s*="),
    ("password", r"passw(?:or)?d"),
    ("secret", r"secret"),
    ("API key word", r"api[_-]?key"),
    ("AWS key", r"AKIA[0-9A-Z]{16}"),
    ("GitHub token", r"gh[pousr]_[A-Za-z0-9]{20,}"),
    ("OpenAI/Anthropic-style key", r"\bsk-[A-Za-z0-9_-]{16,}"),
    ("Slack token", r"xox[abprs]-"),
    ("Google API key", r"AIza[0-9A-Za-z_-]{30,}"),
    ("ntfy token", r"\btk_[A-Za-z0-9]{10,}"),
    ("private key block", r"BEGIN [A-Z ]*PRIVATE KEY"),
    ("JWT", r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),
    ("long hex string", r"\b[0-9a-f]{32,}\b"),
    ("MAC address", r"\b[0-9a-f]{2}(?::[0-9a-f]{2}){5}\b"),
    ("USB vendor:product ID", r"\b[0-9a-f]{4}:[0-9a-f]{4}\b"),
    ("phone number", r"\(?\b\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}\b"),
    ("Windows user path", r"[A-Z]:\\Users\\"),
    ("home directory path", r"/(?:home|Users)/[A-Za-z0-9._-]+"),
    ("private repo link", r"github\.com/"),
    ("serial port", r"\bCOM\d+\b"),
    ("home layout word", r"\b(?:garage|basement|bedroom|kid'?s room|nursery)\b"),
    ("family relation", r"\b(?:son|daughter|wife|husband|dad|mom|grandma|grandpa|grandson|granddaughter)\b"),
    ("employer/work", r"\b(?:employer|presales|my job)\b"),
    ("external resource", r"(?:src|href)\s*=\s*[\"']?(?:https?:)?//"),
    ("excluded project", r"heinrichprotocol|game_01"),
]

# Allowed exceptions per file (exact substrings removed before scanning).
ALLOW = {
    "style.css": ["@media"],
}

# The deny-list (salted hashes of private names, hostnames and places) is kept OUT of this
# public repo: one hash per line in deny_hashes.txt (git-ignored) or the file named by
# PRIVACY_DENYLIST. Its private copy lives in the owner's private repository.
def load_deny_hashes():
    import os
    path = pathlib.Path(os.environ.get("PRIVACY_DENYLIST") or pathlib.Path(__file__).with_name("deny_hashes.txt"))
    try:
        return {line.strip() for line in path.read_text().splitlines() if re.fullmatch(r"[0-9a-f]{64}", line.strip())}
    except OSError:
        return set()


DENY_HASHES = load_deny_hashes()


def norm_hash(text):
    return hashlib.sha256((SALT + " ".join(TOKEN.findall(text.lower()))).encode()).hexdigest()


def scan_text(name, text):
    findings = []
    for allowed in ALLOW.get(name, []):
        text = text.replace(allowed, " ")
    for lineno, line in enumerate(text.splitlines(), 1):
        for label, pattern in RULES:
            for m in re.finditer(pattern, line, re.IGNORECASE):
                findings.append(f"{name}:{lineno}: {label}: {m.group(0)!r}")
        tokens = TOKEN.findall(line.lower())
        for n in range(1, MAX_NGRAM + 1):
            for i in range(len(tokens) - n + 1):
                gram = " ".join(tokens[i:i + n])
                if norm_hash(gram) in DENY_HASHES:
                    findings.append(f"{name}:{lineno}: deny-list term: {gram!r}")
    return findings


def main(argv):
    if len(argv) >= 2 and argv[0] == "--hash":
        print(norm_hash(" ".join(argv[1:])))
        return 0
    findings = []
    if not DENY_HASHES:
        findings.append("deny-list missing: put deny_hashes.txt next to this script or set PRIVACY_DENYLIST")
    for name in TARGETS:
        path = ROOT / name
        if not path.exists():
            findings.append(f"{name}: missing (run build.py first)")
            continue
        findings += scan_text(name, path.read_text(encoding="utf-8"))
    if findings:
        print("PRIVACY CHECK FAILED")
        print("\n".join(findings))
        return 1
    print(f"Privacy check passed: {len(TARGETS)} files, {len(RULES)} patterns, {len(DENY_HASHES)} deny-list hashes.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
