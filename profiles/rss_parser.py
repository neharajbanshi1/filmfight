import re
from datetime import datetime
from xml.etree import ElementTree

import requests

LETTERBOXD_RSS_URL = "https://letterboxd.com/{username}/rss/"


def fetch_diary_entries(username):
    url = LETTERBOXD_RSS_URL.format(username=username)
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    return parse_rss(resp.text)


def parse_rss(xml_text):
    root = ElementTree.fromstring(xml_text)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    channel = root.find("channel")
    if channel is None:
        channel = root

    items = []
    for item in channel.findall("item"):
        title_el = item.find("title")
        if title_el is None or not title_el.text:
            continue
        raw = title_el.text.strip()

        parsed = _parse_item_title(raw)
        if parsed is None:
            continue

        description = ""
        desc_el = item.find("description")
        if desc_el is not None and desc_el.text:
            description = desc_el.text.strip()

        rating = _extract_rating(description, parsed["rating_text"])

        items.append({
            "film_title": parsed["film_title"],
            "year": parsed["year"],
            "rating": rating,
            "review": parsed.get("review", ""),
        })

    return items


def _parse_item_title(raw):
    match = re.match(
        r'"(?P<film_title>.+?)"(?:\s*\((?P<year>\d{4})\))?'
        r'(?:\s*-\s*(?P<rating_text>.+?))?'
        r'(?:\s*(?P<review>.*?))?\s*$',
        raw,
    )
    if not match:
        return None

    data = match.groupdict()
    data["year"] = int(data["year"]) if data.get("year") else None
    return data


RATING_MAP = {
    "★": 1,
    "★★": 2,
    "★★★": 3,
    "★★★★": 4,
    "★★★★★": 5,
    "½": 0.5,
}


def _extract_rating(description, rating_text):
    if rating_text and "★" in rating_text:
        stars = rating_text.count("★")
        half = 0.5 if "½" in rating_text else 0
        return stars + half
    return None
