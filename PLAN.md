# FilmFight — Learning Plan

## Phase 0: Foundation ✅ (Complete)

| Task | Status |
|------|--------|
| Interview / requirement gathering | ✅ |
| PRD written | ✅ |
| Django project scaffolded | ✅ |
| Two apps created (`profiles` + `analysis`) | ✅ |
| Tailwind CSS (CDN) wired in | ✅ |
| Chart.js (CDN) wired in | ✅ |
| Dark theme base template | ✅ |
| Git repo initialised | ✅ |

## Phase 1: Data Layer ✅ (Complete — Read Only)

| Task | Status |
|------|--------|
| `Profile` model | ✅ |
| `Film` model | ✅ |
| `DiaryEntry` model | ✅ |
| Models registered in admin | ✅ |
| RSS parser for Letterboxd feeds | ✅ |
| TMDB client (search, genres, director, poster) | ✅ |
| Management command: `fetch_profile` | ✅ |
| Migrations created + applied | ✅ |

### How to fetch data:
```bash
export TMDB_API_KEY="your_key_here"
python3 manage.py fetch_profile roo
python3 manage.py fetch_profile cline
```

Data is now in SQLite and ready to query.

---

## Phase 2: Views + Templates ✅ (Complete — Read Only)

| Task | Status |
|------|--------|
| Home page with 1- and 2-username forms | ✅ |
| Single profile page with chart canvases | ✅ |
| Comparison page with chart canvases | ✅ |
| URL routing (`/`, `/profile/<u>/`, `/compare/`) | ✅ |
| Tagline/commentary system | ✅ |

### What the templates render right now:
- Placeholder text ("Waiting for your query")
- Empty chart canvases

They fill with real data once **you** write the queries.

---

## Phase 3: Your Learning — Basic Queries 🔧 (Next)

| Task | Status |
|------|--------|
| **Exercise 1:** Count total diary entries for a profile | ☐ |
| **Exercise 2:** Calculate average rating per profile | ☐ |
| **Exercise 3:** Rating distribution (count per star value) | ☐ |
| **Exercise 4:** Genre breakdown — most-watched genres | ☐ |
| **Exercise 5:** Top directors by film count | ☐ |
| Wire results into `single_profile.html` template | ☐ |
| Wire Chart.js to render real data | ☐ |

**File you'll edit:** `analysis/queries.py`

---

## Phase 4: Comparison Queries 🔧 (Next)

| Task | Status |
|------|--------|
| **Exercise 6:** Side-by-side total films and avg rating | ☐ |
| **Exercise 7:** Genre overlap (genres both users watch) | ☐ |
| **Exercise 8:** Rating correlation on shared films | ☐ |
| **Exercise 9:** Films user A watched but user B hasn't | ☐ |
| Wire results into `comparison.html` template | ☐ |
| Wire Chart.js (genre chart + scatter plot) | ☐ |

**File you'll edit:** `analysis/queries.py`

---

## Phase 5: Polish & Fun (Later)

| Task | Status |
|------|--------|
| Play with taglines — make them funnier | ☐ |
| Add loading spinners while data fetches | ☐ |
| Responsive mobile layout polish | ☐ |
| Error handling (invalid usernames, no RSS, etc.) | ☐ |
| Custom 404 / error pages | ☐ |
| TMDB poster grid in comparison | ☐ |

---

## Phase 6: Stretch Goals (If You Want)

| Task | Status |
|------|--------|
| Director / actor comparison | ☐ |
| "Same day" detection (watched same film same day) | ☐ |
| Year-by-year stats | ☐ |
| "Roast me" mode with savage taglines | ☐ |
| Deploy to Render / Railway / Fly.io | ☐ |
| Swap SQLite → Postgres | ☐ |

---

## Learning Path Summary

```
Phase 0-2: I built everything. You read. ──▶ Understand the structure
Phase 3:    You write basic queries    ──▶ Learn Django ORM (filter, annotate, count)
Phase 4:    You write comparison queries ──▶ Learn joins, subqueries, aggregation
Phase 5:    You polish & customize      ──▶ Own the app
```

Ready to start Phase 3? Say "give me a query" and I'll walk you through Exercise 1.
