from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name="home"),
	path('home/', views.home, name="home"),
	path('search/', views.search, name="search"),
	path('search-ajax/', views.search_ajax, name="search_ajax"),
	path('song/add/', views.add_song, name="add_song"),
	path('song/<str:title>/', views.view_song, name="view_song"),
	path('song/<int:id>/edit/', views.edit_song, name="edit_song"),
	path('user/song/<int:id>/delete/', views.delete_song_table, name="delete_song_table"),
	path('song/<int:id>/like/', views.like, name="like"),
	path('song/<int:id>/dislike/', views.dislike, name="dislike"),
	path('song/<int:id>/fav/', views.fav, name="fav"),
	path("song/<int:id>/add_view/", views.add_view, name="add_view"),
	path('song/<int:id>/add-to-playlist/', views.add_to_playlist, name="add_to_playlist"),
	path('playlist/<int:playlist_id>/remove/<int:song_id>/', views.delete_song_in_playlist, name='remove_song_in_playlist'),

	path('song/<int:id>/comment/add/', views.add_comment, name="add_comment"),
	path('comment/<int:id>/edit/', views.edit_comment, name="edit_comment"),
	path('comment/<int:id>/delete/', views.delete_comment, name="delete_comment"),
	path('user/<str:username>/comment/<int:id>/delete/', views.delete_comment_table, name="delete_comment_table"),

	path('playlists/<str:username>/', views.view_playlists, name="view_playlists"),
	path('playlist/<str:username>/<str:title>/', views.view_playlist, name="view_playlist"),
	path('playlist/<int:id>/add/', views.add_playlist, name="add_playlist"),
	path('user/playlist/<int:id>/delete/', views.delete_playlist_table, name="delete_playlist_table"),
	path('ajax_add_playlist/', views.add_playlist_, name="ajax_add_playlist"),
	path('ajax_delete_playlist/<int:id>/', views.delete_playlist_ajax, name="delete_playlist_ajax"),
	path('ajax_edit_playlist/<int:id>/', views.edit_playlist_data, name="ajax_edit_playlist"),

	path('sign-up/', views.sign_up, name="sign_up"),
	path('user/<str:username>/', views.view_profile, name="view_profile"),
	path('user/<str:username>/favorites/', views.view_favorites, name="view_favorites"),
	path('user/<str:username>/liked/', views.view_liked, name="view_liked"),
	path('user/liked/<int:id>/delete/', views.delete_liked_table, name="delete_liked_table"),
	path('user/disliked/<int:id>/delete/', views.delete_disliked_table, name="delete_disliked_table"),
	path('user/fav/<int:id>/delete/', views.delete_fav_table, name="delete_fav_table"),
	path("favorites/remove/<int:id>/", views.un_fav_ajax, name="un_fav_ajax"),
	path("liked/remove/<int:id>/", views.un_like_ajax, name="un_like_ajax"),
]
