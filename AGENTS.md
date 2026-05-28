# FilmFight — AGENTS.md

## Project nature

Learning project. The user writes Django ORM queries in `analysis/queries.py` to learn data analysis. The `profiles` app (models, RSS parsing, TMDB) is pre-built boilerplate — do not modify unless explicitly asked.

## Data sources

- **Letterboxd RSS** (`letterboxd.com/{username}/rss/`) — diary entries, ratings, reviews. No auth.
- **TMDB API** (free tier: 40 req/10s) — genres, director, poster. Requires `TMDB_API_KEY` env var.
- Official Letterboxd API is **not used** (terms forbid data-analysis projects).

## Commands

```bash
export TMDB_API_KEY="your_key"
python3 manage.py fetch_profile <username>
python3 manage.py runserver
```

No test/lint/typecheck commands exist.

## Architecture

- Django 6.0 + SQLite + Python 3.12
- Two apps: `profiles` (data layer) and `analysis` (query/views layer)
- URL root routes through `analysis.urls` (`/`, `/profile/<str:username>/`, `/compare/`)
- No user accounts, no auth, anonymous access only
- Templates: Tailwind CSS CDN + Chart.js 4 CDN, dark theme with `film-*` custom purple palette

## Key conventions

- `profiles/models.py`: Profile (username unique), Film (tmdb_id unique, genres=JSONField), DiaryEntry (unique_together: profile+film+watched_date)
- `analysis/queries.py` — user's file; query functions receive usernames, return dicts. Views call `queries.profile_summary()`. Keep this contract.
- `analysis/taglines.py` — dict of category→list of template strings with `{genre}`/`{director}` placeholders, chosen via `random.choice`.
- Comparison view reads `?user_a=X&user_b=Y` query params (GET, not POST).
- Homepage single-profile form uses JS redirect hack (`onsubmit` + `event.preventDefault()`), not a standard Django form POST.
- `settings.py` reads `TMDB_API_KEY` from `os.getenv`, falls back to empty string.

## What not to do

- Do not add user accounts, auth, or login pages.
- Do not replace the RSS/TMDB data pipeline unless asked.
- Do not add test infrastructure unless explicitly requested.
- Do not modify `profiles/` models, RSS parser, or TMDB client without instruction.
- Do not add migrations for the `analysis` app (it has no models).
