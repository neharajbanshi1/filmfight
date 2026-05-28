from django.core.management.base import BaseCommand
from letterboxdpy.user import User as LbUser

from profiles.models import Profile, Film, DiaryEntry
from profiles.tmdb import search_movie


class Command(BaseCommand):
    help = "Fetch full diary for a Letterboxd profile"

    def add_arguments(self, parser):
        parser.add_argument("username")

    def handle(self, username, **options):
        profile, _ = Profile.objects.get_or_create(username=username)

        self.stdout.write(f"Fetching diary for @{username}...")
        lb_user = LbUser(username)
        diary = lb_user.get_diary()
        entries = list(diary["entries"].values())

        if not entries:
            self.stdout.write(self.style.WARNING("No diary entries found."))
            return

        created_count = 0
        for entry in entries:
            title = entry["name"]
            year = entry.get("release")

            film, _ = Film.objects.get_or_create(
                title=title,
                defaults={"year": year},
            )

            if not film.tmdb_id:
                tmdb_data = search_movie(title, year)
                if tmdb_data:
                    for key, val in tmdb_data.items():
                        setattr(film, key, val)
                    film.save()

            watched_date = None
            if entry.get("date"):
                watched_date = entry["date"][:10]

            rating = entry["actions"]["rating"]

            _, was_created = DiaryEntry.objects.get_or_create(
                profile=profile,
                film=film,
                watched_date=watched_date,
                defaults={"rating": rating},
            )
            if was_created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. {created_count} new entries saved "
                f"({len(entries) - created_count} already existed). "
                f"Total films logged: {lb_user.stats['films']}"
            )
        )
