from django.contrib import admin
from .models import Song, Comment, Favorite, Like, DisLike, Playlist

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
	list_display = ("title", "user", "created_at", "likes_count", "dislikes_count", "favorites_count")
	list_filter = ("user", "created_at")
	search_fields = ("title", "description", "user__username")

	def likes_count(self, obj):
		return obj.likes.count()
	likes_count.short_description = "Likes"

	def dislikes_count(self, obj):
		return obj.dislikes.count()
	dislikes_count.short_description = "Dislikes"

	def favorites_count(self, obj):
		return obj.favorites.count()
	favorites_count.short_description = "Favorites"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ("label", "user", "song", "created_at")
	list_filter = ("user", "created_at")
	search_fields = ("label", "text", "user__username", "song__title")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
	list_display = ("song", "user")
	search_fields = ("song__title", "user__username")


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
	list_display = ("song", "user")
	search_fields = ("song__title", "user__username")


@admin.register(DisLike)
class DisLikeAdmin(admin.ModelAdmin):
	list_display = ("song", "user")
	search_fields = ("song__title", "user__username")


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
	list_display = ("title", "user", "songs_count")
	search_fields = ("title", "user__username")

	def songs_count(self, obj):
		return obj.songs.count()
	songs_count.short_description = "Songs in Playlist"
