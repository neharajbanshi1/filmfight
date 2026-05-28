"""
YOUR LEARNING ZONE — write your ORM / analysis queries here.

Each function receives a username (or two) and should return
a dict with the data needed for the template.

Examples:

def genre_breakdown(username):
    # Your query here
    return {"categories": [...], "counts": [...]}

def average_rating(username):
    return {"avg": 3.5}

def rating_correlation(user_a, user_b):
    return {"correlation": 0.72}
"""


from profiles.models import Profile


def profile_summary(username):
    profile = Profile.objects.get(username=username)
    total = profile.diary_entries.count()
    return {"total_films": total}
