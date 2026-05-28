from django.core.management.base import BaseCommand
from profiles.models import Profile, Film, DiaryEntry
from profiles.rss_parser import fetch_diary_entries
from profiles.tmdb import search_movie


class Command(BaseCommand):
    help = "Fetch diary entries for a Letterboxd profile"

    def add_arguments(self, parser):
        parser.add_argument("username")

    def handle(self, username, **options):
        profile, _ = Profile.objects.get_or_create(username=username)

        self.stdout.write(f"Fetching RSS for @{username}...")
        entries = fetch_diary_entries(username)

        if not entries:
            self.stdout.write(self.style.WARNING("No diary entries found."))
            return

        created_count = 0
        for entry in entries:
            film, _ = Film.objects.get_or_create(
                title=entry["film_title"],
                defaults={"year": entry["year"]},
            )

            if not film.tmdb_id:
                tmdb_data = search_movie(entry["film_title"], entry["year"])
                if tmdb_data:
                    for key, val in tmdb_data.items():
                        setattr(film, key, val)
                    film.save()

            _, was_created = DiaryEntry.objects.get_or_create(
                profile=profile,
                film=film,
                watched_date=None,
                defaults={
                    "rating": entry["rating"],
                    "review": entry["review"],
                },
            )
            if was_created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. {created_count} new entries saved "
                f"({len(entries) - created_count} already existed)."
            )
        )
