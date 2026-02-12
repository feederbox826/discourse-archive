# discourse-archive
discourse archiver & archive browser

- no apikey required
- /browse has json post browser
- Caddy handles rewrites for SPA page loading
- configure `.env` to reflect your site (see src/env.py)
- sqlite is used for topic update detection, git is used for VC of topics
