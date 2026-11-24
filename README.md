# Atx File Host Bot - Render Deploy Guide

## Files
- main.py            -> tumhara bot (patch already laga hua hai, token env se aata hai)
- keep_alive.py      -> web server + 5 sec auto ping
- requirements.txt
- render.yaml        -> Render auto config
- .python-version, .gitignore, .env.example

## Steps
1. @BotFather me /revoke karke NAYA token lo (purana token leak ho chuka hai).
2. GitHub par private repo banao, saari files push karo.
3. Render -> New -> Web Service -> repo select (ya Blueprint se render.yaml).
4. Environment me BOT_TOKEN (aur OWNER_ID) daalo.
5. Deploy. Logs me "Auto-ping started" dikhega.

## Note
- Render free me disk temporary hai: restart/redeploy par uploads aur database
  (inf/bot_data.db) reset ho jaate hain. Permanent chahiye to paid Persistent Disk lo.
- Node.js (.js scripts) ke liye Docker deploy chahiye; native Python env me node nahi hota.
