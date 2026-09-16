---
name: previewing-site
description: Use when someone wants to see the dominigames.ru site locally before publishing — "покажи сайт", "запусти превью", "лайвпревью", "как это будет выглядеть", "открой локально", "посмотреть изменения", "останови превью" — often a non-technical person (lawyer, accountant, manager).
---

# Previewing the site locally

## Overview
The site is plain HTML, so a static server from the repo root is the whole preview. The person asking may not be technical: you do every step yourself and reply in plain Russian, with no commands in the reply.

## Start
1. Check whether a preview is already running:
   ```bash
   curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/
   ```
   `200` → already running, skip to step 3. Anything else → step 2.
2. Start the server **in the background** (Bash `run_in_background: true`), from the repo root:
   ```bash
   python -m http.server 8000 --bind 127.0.0.1
   ```
   - Port busy with something else → use 8001 (and that port in every URL below).
   - No `python` → `npx --yes http-server -p 8000 -a 127.0.0.1 -c-1`.
3. Check the pages answer `200`: `/`, `/accreditation/`, `/privacy-policy/`, `/terms/`.
4. Open the page the person cares about (the one just edited, else the main page):
   - Windows: `start "" http://localhost:8000/accreditation/`
   - macOS: `open …`, Linux: `xdg-open …`

Never open files via `file://` — links between pages break there.

## Reply to the person (template, Russian)
> Сайт открыт в браузере: http://localhost:8000/…
> Другие страницы: главная — http://localhost:8000/, аккредитация — …/accreditation/, политика — …/privacy-policy/, условия — …/terms/
> Это видно только на вашем компьютере, на настоящем сайте пока ничего не изменилось.
> После новых правок просто нажмите F5 (обновить страницу).
> Как выглядит на телефоне: нажмите F12, затем Ctrl+Shift+M и выберите телефон сверху.
> Когда закончите, напишите «останови превью».

## Stop
Stop the background task you started (TaskStop with its ID). If you don't have the ID (new session), on Windows find the process listening on the port and stop it:
```powershell
Get-NetTCPConnection -LocalPort 8000 -State Listen | ForEach-Object { Stop-Process -Id $_.OwningProcess -Confirm:$false }
```
Confirm with the `curl` check (no longer `200`) and tell the person the preview is off.

## Common mistakes
- Running the server in the foreground → the session hangs. Always background.
- Starting a second server when one already answers on 8000.
- Giving the person commands to type. Do it yourself; give them only links and the F5 / F12 tips.
