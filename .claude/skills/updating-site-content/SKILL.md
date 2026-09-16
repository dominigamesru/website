---
name: updating-site-content
description: Use when adding, changing or restyling text on the dominigames.ru website — accreditation (аккредитация, реквизиты, ОКВЭД, коды ИТ-деятельности Минцифры), privacy policy (политика конфиденциальности), terms (пользовательское соглашение) or the main page — especially when a lawyer or accountant sends a package of content changes.
---

# Updating site content (dominigames.ru)

## Overview
Static site, no build step. Every page is one self-contained HTML file with its own `<style>`. GitHub Pages serves `main` (see `CNAME`).

**Core rule: page text is legal text. It goes on the site exactly as supplied — only markup and styling may be improved.** Violating the letter of this rule is violating its spirit.

| Page | File |
|---|---|
| Главная | `index.html` |
| Аккредитация (реквизиты, ОКВЭД, коды ИТ-деятельности, услуги) | `accreditation/index.html` |
| Политика конфиденциальности | `privacy-policy/index.html` |
| Пользовательское соглашение | `terms/index.html` |

## Text contract
Added text = the requester's text, character for character:
- Typos, odd spacing, dashes, quote styles, capitalisation — keep them (e.g. `реализациии (или)`, `22.01 -Деятельность`). Report suspected typos to the user; fix only after they confirm.
- Existing text is never reworded, re-punctuated, reordered or "unified" — including when restyling a page.
- Outer quotes/marks that only delimit the quote in the request («…», "…", trailing ` .`) are not part of the text. When unsure, ask.
- New text goes where the requester said. If they only named the topic ("код 12.01 — рекламная платформа"), put it next to the matching existing item. "В начале" of privacy/terms = after `Редакция от …`, before section 1.
- "Метка: значение" in a request becomes a `.main__table` row: label cell = text before the colon, value cell = text after it.
- Phones, emails and site addresses are rendered as links (`tel:`, `mailto:`, `https:`), new or existing; the visible text stays the same.
- Headings/labels the requester did not provide are not invented. If structure needs a label, use their own words or ask.
- Requisites (ИНН, ОГРН, КПП, адрес, телефон, email) repeat across pages (accreditation, privacy, footer of `index.html`). If one changes, `grep` the old value and ask whether to change every occurrence.

## Markup conventions
- BEM classes in the page's own `<style>`: `.main__section`, `.main__table` (label | value rows), `.main__highlight`, `.main__code` (long official wording of a code under a list item, in accreditation).
- No inline `style=""` for new elements; add a class. When restyling a page, moving its inline styles into classes is fine; otherwise leave them.
- Check width 320px: long text must wrap; tables must not overflow.
- Footer year `© Доминигеймс, 2020 – YYYY` — update only if asked.
- The edition date (`Редакция от …`) in privacy/terms — do not change on your own; ask whether the edit needs a new date.

## Verify (required before reporting done)
```bash
python .claude/skills/updating-site-content/text_diff.py        # vs HEAD; or pass a REV
```
Run from the site's repo root (for another checkout: `cd` there and call the script by absolute path). Prints the diff of **visible text** only (markup/CSS ignored).
- Layout-only change → must print `no text changes`.
- Content change → only `+` lines with the requested text. Any `-` line means existing text was altered: undo it.
- Compare each `+` line with the request word for word.

If the layout changed: `python -m http.server 8000` from the repo root, open `http://localhost:8000/<page>/` (relative `../` links need a server, not `file://`). Check desktop and 320–375px width via browser DevTools device mode; headless screenshots can't go that narrow — then ask the user to check on a phone and say so in the report.

## Report to the user
1. Added text, verbatim, and where it went.
2. The `text_diff.py` result (removals: none).
3. Layout changes.
4. Suspected typos, contradictions with other clauses (e.g. privacy scope in п. 1.1), edition date — as questions, not as fixes.

Commit only when asked; message in Russian, describing the content change (e.g. `аккредитация: добавлены коды ИТ-деятельности 12.01 и 22.01`).

## Red flags — stop
- "Fixing an obvious typo in the legal text"
- "Unifying the company name / quotes / dashes"
- "Shortening the long official wording so it fits"
- "Restyling, so I rewrote the intro a bit"
- Skipping `text_diff.py` because "I only added a row"
