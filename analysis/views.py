from django.shortcuts import render

from . import queries, taglines


def home(request):
    return render(request, "home.html")


def single_profile(request, username):
    ctx = {"username": username}
    summary = queries.profile_summary(username)
    if summary:
        ctx.update(summary)
        ctx["tagline"] = taglines.get_tagline("high_rating")
    return render(request, "single_profile.html", ctx)


def compare(request):
    user_a = request.GET.get("user_a", "")
    user_b = request.GET.get("user_b", "")
    ctx = {"user_a": user_a, "user_b": user_b}
    if user_a and user_b:
        ctx["tagline"] = taglines.get_tagline("overlap")
    return render(request, "comparison.html", ctx)
