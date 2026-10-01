# CLAUDE.md

Static website of ООО «ДОМИНИГЕЙМС» (dominigames.ru). Plain HTML, no build, no JS framework, no package manager. Each push to `main` triggers the GitHub Pages build/deploy (`CNAME` → dominigames.ru); status: https://github.com/dominigamesru/website/actions. Content and commits are in Russian.

## Structure
- `index.html` — landing: logo, subtitle, infinite CSS carousel of game icons (`images/games/`, list is duplicated for the seamless loop), footer with requisites and links to legal pages.
- `accreditation/index.html` — data for Минцифры IT accreditation: requisites, bank account, contacts, ОКВЭД, IT-activity codes (12.01, 22.01), tech stack, services and pricing.
- `privacy-policy/index.html`, `terms/index.html` — legal documents with `Редакция от …` date.
- Each page is self-contained: its own `<style>`, BEM classes (`header__…`, `main__…`, `footer__…`), Ubuntu font from Google Fonts, dark theme (`#000` background, white text with opacity). Subpages link back with `../`.

## Rules
- **All page text is legal text: keep it verbatim.** Only markup/CSS may be improved. Never fix typos, punctuation or wording on your own — report them and ask.
- For any content or layout change, use the `updating-site-content` skill (`.claude/skills/updating-site-content/`). It includes `text_diff.py`, which diffs the visible text against git — run it before reporting done.
- Requisites are duplicated (accreditation, privacy policy, `index.html` footer) — keep them in sync, ask before changing others.
- Keep pages dependency-free: no external JS, no shared CSS unless asked.
- Commit/push only when asked. Commit messages in Russian.

## Commands
- Preview: use the `previewing-site` skill (background `python -m http.server 8000` → http://localhost:8000/)
- Text check: `python .claude/skills/updating-site-content/text_diff.py [REV]`

## Known issues
- `og:image` points to `images/ogimage.png`, which does not exist.
- Privacy policy section 6 mentions Яндекс.Метрика, but no counter is installed on the pages.
