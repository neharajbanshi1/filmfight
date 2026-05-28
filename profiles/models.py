from django.db import models


class Profile(models.Model):
    username = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    avatar_url = models.URLField(blank=True)
    last_fetched = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Film(models.Model):
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True)
    title = models.CharField(max_length=300)
    year = models.IntegerField(null=True, blank=True)
    genres = models.JSONField(default=list, blank=True)
    director = models.CharField(max_length=300, blank=True)
    poster_url = models.URLField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.year})"


class DiaryEntry(models.Model):
    HALF = 0.5

    RATING_CHOICES = [
        (HALF, HALF), (1, 1), (1.5, 1.5), (2, 2), (2.5, 2.5),
        (3, 3), (3.5, 3.5), (4, 4), (4.5, 4.5), (5, 5),
    ]

    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='diary_entries'
    )
    film = models.ForeignKey(
        Film, on_delete=models.CASCADE, related_name='diary_entries'
    )
    rating = models.FloatField(null=True, blank=True, choices=RATING_CHOICES)
    review = models.TextField(blank=True)
    watched_date = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'diary entries'
        unique_together = ('profile', 'film', 'watched_date')

    def __str__(self):
        return f"{self.profile.username} - {self.film.title}"
