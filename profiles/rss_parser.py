import re
from xml.etree import ElementTree

import requests

LETTERBOXD_RSS_URL = "https://letterboxd.com/{username}/rss/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
}

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "letterboxd": "https://letterboxd.com",
    "tmdb": "https://themoviedb.org",
    "dc": "http://purl.org/dc/elements/1.1/",
}


def fetch_diary_entries(username, max_pages=10):
    all_entries = []
    for page in range(1, max_pages + 1):
        url = f"{LETTERBOXD_RSS_URL.format(username=username)}?page={page}"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        entries = parse_rss(resp.text)
        if not entries:
            break
        all_entries.extend(entries)
    return all_entries


def parse_rss(xml_text):
    root = ElementTree.fromstring(xml_text)
    channel = root.find("channel") or root

    items = []
    for item in channel.findall("item"):
        title = _tag_text(item, "letterboxd:filmTitle")
        year = _tag_text(item, "letterboxd:filmYear")
        rating_raw = _tag_text(item, "letterboxd:memberRating")

        # Fallback: parse from <title> tag if namespaced tags missing
        if not title:
            parsed = _parse_title_fallback(item)
            if not parsed:
                continue
            title = parsed["title"]
            year = parsed.get("year")
            rating_raw = parsed.get("rating_raw")

        rating = float(rating_raw) if rating_raw else None

        watched_date = _tag_text(item, "letterboxd:watchedDate")

        items.append({
            "film_title": title.strip() if title else "",
            "year": int(year) if year else None,
            "rating": rating,
            "review": "",
            "watched_date": watched_date,
        })

    return items


def _tag_text(item, tag):
    el = item.find(tag, NS)
    if el is not None and el.text:
        return el.text.strip()
    return None


def _parse_title_fallback(item):
    title_el = item.find("title")
    if title_el is None or not title_el.text:
        return None
    raw = title_el.text.strip()

    # "Perfect Blue, 1997 - ★★★★"
    match = re.match(
        r"(?P<title>.+?),?\s*(?:\(?(?P<year>\d{4})\)?)?"
        r"\s*-\s*(?P<stars>[★½]+)\s*$",
        raw,
    )
    if match:
        stars = match.group("stars")
        rating = stars.count("★") + (0.5 if "½" in stars else 0)
        return {
            "title": match.group("title"),
            "year": match.group("year"),
            "rating_raw": str(rating),
        }

    return None
