# FilmFight — PRD

> **Status:** Draft  
> **Last updated:** May 2026  
> **Goal:** Build a playful Letterboxd profile comparison webapp to learn data analysis with Django, SQL/ORM, and data visualisation.

---

## 1. Overview

FilmFight lets users enter one or two Letterboxd usernames and see fun, insightful analysis of their movie-watching habits. Single profiles get a personal "wrap" style breakdown; two profiles get a head-to-head comparison.

The focus is **learning by doing** — the app is deliberately split so the user writes the analysis queries while the boilerplate (fetching, parsing, models, UI) is pre-built.

## 2. Data Sources

| Source | Purpose | Auth Required |
|--------|---------|--------------|
| **Letterboxd RSS feed** (`letterboxd.com/{username}/rss/`) | Diary entries, ratings, reviews, watched dates | No |
| **TMDB API** (`api.themoviedb.org/3`) | Film metadata: genres, director, poster, year | Free API key |

The official Letterboxd API is **not used** because its terms deny data-analysis/visualisation projects.

## 3. Architecture

```
Django 6.0 + SQLite (default)
├── profiles app     — models, RSS parser, TMDB client, management commands
├── analysis app     — query functions, taglines, views (user edits this)
├── templates/       — base.html, home, single_profile, comparison
└── static/          — custom CSS/JS (minimal)
```

- **No user accounts.** Anyone can enter usernames and see results.
- **No JS framework.** Django templates + Tailwind CSS (CDN) + Chart.js.
- **SQLite** for development. Easy swap to Postgres later.

## 4. Data Model

### Profile
- `username` (unique), `display_name`, `bio`, `avatar_url`, `last_fetched`

### Film
- `tmdb_id` (nullable), `title`, `year`, `genres` (JSON list), `director`, `poster_url`

### DiaryEntry
- `profile` (FK), `film` (FK), `rating` (0.5–5, half-star increments), `review`, `watched_date`
- Unique constraint: (profile, film, watched_date)

Data is fetched via `python3 manage.py fetch_profile <username>`.

## 5. Pages

### Home (`/`)
- Enter two usernames → Compare
- Enter one username → Single analysis
- Whimsical copy, dark theme

### Single Profile (`/profile/<username>/`)
- Total films watched, average rating, rating distribution chart
- Genre breakdown, top directors
- Tagline / commentary (e.g. "You rated The Room 5 stars — respect.")

### Comparison (`/compare/?user_a=X&user_b=Y`)
- Side-by-side stats (total films, avg rating)
- Genre overlap chart
- Rating correlation scatter plot
- "Films you both watched" table
- Mutual taglines

## 6. Your Learning Zone

All files marked with 🔧 are yours to write:

| File | What you'll do |
|------|---------------|
| `analysis/queries.py` 🔧 | Write Django ORM queries to aggregate, filter, and compute stats |
| `analysis/taglines.py` | Customise the playful commentary (already functional) |
| Templates / views | Optionally tweak UI — but the focus is queries |

Suggested first exercises:
1. Count total diary entries for a profile
2. Calculate average rating per profile
3. Find most-watched genre per profile
4. Find most-watched director per profile
5. Compute rating overlap/correlation between two profiles
6. List films one user watched but the other hasn't

## 7. Tech Stack

- **Backend:** Django 6.0 (Python 3.12)
- **Database:** SQLite (dev), easily swappable
- **Styling:** Tailwind CSS (CDN)
- **Charts:** Chart.js 4 (CDN)
- **Parsing:** BeautifulSoup4 + lxml
- **HTTP:** requests

## 8. Future Ideas (if wanted)

- Director / actor comparison
- Watched-on-the-same-day detection
- "Roast me" mode with savage taglines
- User accounts to save favourite comparisons
- Year-in-review style stats pages
- TMDB poster grid for visual comparison

## 9. Constraints

- No official Letterboxd API access (terms forbid data analysis use)
- RSS only exposes diary entries and reviews — no watchlist or list data
- TMDB rate limits apply (free tier: 40 requests per 10 seconds)
- No authentication — all data is public RSS
