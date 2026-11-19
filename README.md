# Jason's projects (public site)

A small static website that describes a curated set of Jason's GitHub projects.
It is published with GitHub Pages and contains only public-safe summaries.

## Structure

| File | Purpose |
| --- | --- |
| `projects.json` | The content: one entry per project (`slug`, `name`, `repo`, `tagline`, `goal`, `overview`, `features[]`, `tech[]`, `status`, `current`, `updated`). |
| `build.py` | Pre-renders `index.html` from `projects.json` (Python 3, standard library only). |
| `index.html` | The generated page. Static HTML; works without JavaScript. Do not edit by hand. |
| `style.css` | Styles. Light and dark themes follow the system setting. No external fonts, CDNs, analytics or trackers. |
| `check_privacy.py` | Scans the published files for private details. Must pass before every commit. |
| `PRIVACY-CHECKLIST.md` | The rules every update must follow. |

## Updating

```sh
# 1. edit projects.json
python3 build.py
python3 check_privacy.py   # must print "Privacy check passed"
git commit -am "Update project descriptions"
```

Field rules: `goal` is the final outcome in one sentence (at most 160 characters);
`current` says where the project stands now (at most 240 characters); `status` is `Active`, `Maintained` or `Early`; `updated` is `YYYY-MM`
(the month of the source repository's last commit); each project has 3 to 6 features.

## Content is curated for privacy

The source repositories are private. Descriptions are written from them by hand
(or by an assistant following `PRIVACY-CHECKLIST.md`) and deliberately leave out
anything that identifies people, places, machines, networks, accounts or security
details. Repository names appear as plain text only; there are no links to them.
When in doubt, a detail is left out.

`check_privacy.py` is a safety net, not a substitute for review. Its deny-list of
names and hostnames is kept out of this repository (deny_hashes.txt, git-ignored;
a private copy lives in the owner's private repository), stored only as salted hashes. Short common words can still be guessed from a
hash, so never rely on the hash to keep a term secret; just keep it off the site.
