# Privacy checklist for site updates

This site is public. Every update (by Jason, Hermes or any other assistant) must
follow these rules. When in doubt, leave it out.

## Never include

- [ ] IP addresses, hostnames, machine names (for example Windows computer names or VM names),
      VPN/tailnet names or URLs, ports, MAC addresses, serial numbers or hardware IDs.
- [ ] File paths that contain usernames, email addresses, phone numbers, account IDs,
      keys, tokens, passwords or anything that looks like one.
- [ ] Names of people other than "Jason" (the site owner). No family members' names, ages,
      schools, routines, schedules, health, vehicles, locations, addresses or home layout
      (rooms, "garage" and so on). Refer generically: "family members", "a relative".
- [ ] Employer or work details.
- [ ] Security architecture details that could help an attacker: what is exposed, firewall
      rules, authentication weaknesses, where credentials are stored. General statements
      such as "runs privately on a home network over a VPN" are fine.
- [ ] Links to the private repositories. Show the repository name as plain text only.
- [ ] Custom domains, cloud project IDs or hosting account names.
- [ ] Images of real people. External fonts, CDNs, analytics or trackers.
- [ ] Any project that is not on the approved list (the game studio repository is excluded).

## Each project entry contains only

- A one-line tagline.
- A one-sentence final goal (the outcome the project is working toward).
- A 2 to 4 sentence overview: what it does and why it exists.
- 3 to 6 feature bullets.
- Tech tags in general terms (languages, frameworks, platforms, hardware categories
  such as "a quadruped robot" or "Android TV").
- Status: `Active`, `Maintained` or `Early`, plus one or two sentences on where it stands now.
- Last updated month (`YYYY-MM`, from `git log -1 --format=%cs`).

## Before committing

1. `python3 build.py`
2. `python3 check_privacy.py` must pass. Add newly encountered names or hostnames to its
   deny-list with `python3 check_privacy.py --hash "term"` (add only the hash to the private deny_hashes.txt, never to this repo).
3. Read the rendered page once more as a stranger would.
