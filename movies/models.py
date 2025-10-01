from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')

    def __str__(self):
        return str(self.id) + ' - ' + self.name


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name


class HiddenMovie(models.Model):
    """
    S–Z user story:
    A per-user toggle that hides a movie from the main listings.
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'movie'),)

    def __str__(self):
        return f"{self.user.username} hides {self.movie.name}"


class Petition(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    reason = models.TextField(blank=True)
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='petitions')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} (by {self.requested_by.username})"


class PetitionVote(models.Model):
    id = models.AutoField(primary_key=True)
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='petition_votes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('petition', 'user'),)

    def __str__(self):
        return f"YES by {self.user.username} on {self.petition.title}"