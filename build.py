#!/usr/bin/env python3
"""Pre-render index.html from projects.json. Standard library only.

Usage: python3 build.py
"""
import html
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIELDS = ("slug", "name", "repo", "tagline", "goal", "overview", "features", "tech", "status", "current", "updated")
LIMITS = {"goal": 160, "current": 240}
STATUSES = {"Active", "Maintained", "Early"}

TITLE = "Jason's projects"
INTRO = "Home-lab, AI and automation projects built in spare time."
FOOTER = "Descriptions generated from the project repositories; updated periodically."


def e(text):
    return html.escape(str(text), quote=True)


def month_label(updated):
    year, month = (int(p) for p in updated.split("-"))
    return date(year, month, 1).strftime("%B %Y")


def load():
    projects = json.loads((ROOT / "projects.json").read_text(encoding="utf-8"))
    for p in projects:
        missing = [f for f in FIELDS if f not in p]
        if missing:
            raise SystemExit(f"{p.get('slug', '?')}: missing {missing}")
        if p["status"] not in STATUSES:
            raise SystemExit(f"{p['slug']}: status must be one of {sorted(STATUSES)}")
        if not 3 <= len(p["features"]) <= 6:
            raise SystemExit(f"{p['slug']}: needs 3-6 features")
        for field, cap in LIMITS.items():
            if not 10 <= len(p[field].strip()) <= cap:
                raise SystemExit(f"{p['slug']}: {field} must be 10-{cap} characters")
        month_label(p["updated"])
    return projects


def tags(items):
    return "".join(f'<li>{e(t)}</li>' for t in items)


def row(p):
    s = p["status"].lower()
    return f"""
    <li class="row">
      <div class="row-head">
        <h2><a href="#{e(p['slug'])}">{e(p['name'])}</a></h2>
        <span class="status status-{s}">{e(p['status'])}</span>
      </div>
      <dl class="row-body">
        <div><dt>Goal</dt><dd>{e(p['goal'])}</dd></div>
        <div><dt>Where it stands</dt><dd>{e(p['current'])}</dd></div>
      </dl>
    </li>"""


def detail(p):
    s = p["status"].lower()
    feats = "".join(f"<li>{e(f)}</li>" for f in p["features"])
    return f"""
  <article class="project" id="{e(p['slug'])}">
    <header>
      <h2>{e(p['name'])}</h2>
      <p class="tagline">{e(p['tagline'])}</p>
      <dl class="meta">
        <div><dt>Status</dt><dd><span class="status status-{s}">{e(p['status'])}</span></dd></div>
        <div><dt>Updated</dt><dd>{e(month_label(p['updated']))}</dd></div>
        <div><dt>Repository</dt><dd><code>{e(p['repo'])}</code> (private)</dd></div>
      </dl>
    </header>
    <dl class="goal-now">
      <div><dt>Goal</dt><dd>{e(p['goal'])}</dd></div>
      <div><dt>Where it stands</dt><dd>{e(p['current'])}</dd></div>
    </dl>
    <p>{e(p['overview'])}</p>
    <h3>Key features</h3>
    <ul class="features">{feats}</ul>
    <h3>Tech</h3>
    <ul class="tags">{tags(p['tech'])}</ul>
    <p class="top"><a href="#top">Back to all projects</a></p>
  </article>"""


def render(projects):
    rows = "".join(row(p) for p in projects)
    details = "".join(detail(p) for p in projects)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{e(INTRO)}">
<meta name="color-scheme" content="light dark">
<meta name="referrer" content="no-referrer">
<title>{e(TITLE)}</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<a class="skip" href="#projects">Skip to projects</a>
<header class="site" id="top">
  <h1>{e(TITLE)}</h1>
  <p>{e(INTRO)}</p>
</header>
<main>
  <section aria-label="Project overview">
    <ol class="list" id="projects">{rows}
    </ol>
  </section>
  <section aria-label="Project details" class="details">{details}
  </section>
</main>
<footer class="site">
  <p>{e(FOOTER)}</p>
</footer>
</body>
</html>
"""


def main():
    projects = load()
    (ROOT / "index.html").write_text(render(projects), encoding="utf-8")
    print(f"Built index.html with {len(projects)} projects")


if __name__ == "__main__":
    main()
