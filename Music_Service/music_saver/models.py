from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timezone as tz

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Song(models.Model):
	GENRES = [
		("pop", "Pop"),
		("rock", "Rock"),
		("hiphop", "Hip-Hop"),
		("electronic", "Electronic"),
		("jazz", "Jazz"),
		("classical", "Classical"),
		("other", "Other"),
	]

	KEYS = [
		("C", "C Major"),
		("Cm", "C Minor"),
		("D", "D Major"),
		("Dm", "D Minor"),
		("E", "E Major"),
		("Em", "E Minor"),
		("F", "F Major"),
		("Fm", "F Minor"),
		("G", "G Major"),
		("Gm", "G Minor"),
		("A", "A Major"),
		("Am", "A Minor"),
		("B", "B Major"),
		("Bm", "B Minor"),
	]

	author = models.CharField(max_length=20)
	title = models.CharField(max_length=20)
	text = models.TextField()
	audio = models.FileField(upload_to="songs/")
	cover_image = models.ImageField(upload_to="images/")
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uploaded_songs")
	created_at = models.DateTimeField(auto_now_add=True)
	views = models.IntegerField(default=0)
	genre = models.CharField(max_length=20, choices=GENRES, default="other")
	release_year = models.CharField(max_length=4, null=True, blank=True)
	key = models.CharField(max_length=5, choices=KEYS, null=True, blank=True)
	bpm = models.IntegerField(null=True, blank=True)

	@property
	def is_release(self):
		delta = 1
		now = timezone.now()
		limit = self.created_at + timezone.timedelta(days=delta)
		return self.created_at <= now <= limit 

	@property
	def delta(self):
		now = timezone.now()
		timediff = now - self.created_at
		return timediff
	
	class Meta:
		db_table = "songs"

class Comment(models.Model):
	label = models.CharField(max_length=30)
	text = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
	song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="comments")
	parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name="replies")

	class Meta:
		db_table = 'comments'

class Favorite(models.Model):
	song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="favorites")
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")

	class Meta:
		db_table = "favorites"
		unique_together = ('song', 'user')

class Like(models.Model):
	song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="likes")
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_songs")

	class Meta:
		db_table = "likes"
		unique_together = ('song', 'user')

class DisLike(models.Model):
	song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="dislikes")
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="disliked_songs")

	class Meta:
		db_table = "dislikes"
		unique_together = ('song', 'user')

class Playlist(models.Model):
	title = models.CharField(max_length=20)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="playlists")
	songs = models.ManyToManyField(Song, related_name="songs", blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	is_public = models.BooleanField(default=False)
	views = models.IntegerField(default=0)

	class Meta:
		db_table = "playlists"