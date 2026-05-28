import random

TAGLINES = {
    "high_rating": [
        "Generous with those stars, aren't we?",
        "Did you enjoy every movie ever made?",
        "Someone's easy to please.",
    ],
    "low_rating": [
        "Touch grass. Or maybe don't, you clearly hate everything.",
        "Who hurt you?",
        "A critic is born.",
    ],
    "genre_repeat": [
        "You really, really like {genre}, huh?",
        "Are you okay? That's a lot of {genre} movies.",
        "At this point, {genre} is not a genre, it's a personality.",
    ],
    "director_obsession": [
        "We get it, you like {director}.",
        "{director} should put you on the payroll.",
        "Have you considered that {director} movies count as a personality trait?",
    ],
    "overlap": [
        "You both have taste. Or maybe just the same Letterboxd feed.",
        "Great minds think alike. Or you just watch the same trending page.",
        "Soulmates? Or just a shared love of mediocrity?",
    ],
    "rating_diff": [
        "One of you is wrong. (It's the one who rated it lower.)",
        "Did you watch the same movie?",
        "This is why movie night is complicated.",
    ],
}


def get_tagline(category, **kwargs):
    lines = TAGLINES.get(category, ["No comment."])
    line = random.choice(lines)
    return line.format(**kwargs)
