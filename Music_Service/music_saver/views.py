from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, AddComment, AddSong, AddPlayList
from .models import Song, Playlist, Comment, Like, DisLike, Favorite
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.urls import reverse
from django.http import JsonResponse
from django.utils.timezone import localtime

def sign_up(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect(reverse("home"))
	else:
		form = RegistrationForm()
	
	context = {'form': form}
	return render(request, 'registration/sign_up.html', context)


def view_profile(request, username: str):
	user = User.objects.filter(username=username).first()
	songs = user.uploaded_songs.all()
	playlists = user.playlists.all()
	comments = user.user_comments.all()
	liked = Like.objects.filter(user=user).select_related('song')
	liked_songs = [s.song for s in liked]
	fav = Favorite.objects.filter(user=user).select_related('song')
	fav_songs = [s.song for s in fav]

	context = {
		'songs': songs,
		'playlists': playlists,
		'comments': comments,
		'liked_songs': liked_songs,
		'fav_songs': fav_songs,
	}

	return render(request, 'music_saver/user/profile.html', context)


def view_favorites(request, username: str):
	user = User.objects.filter(username=username).first()
	favorite = Favorite.objects.filter(user=user).select_related('song')
	favorites = [f.song for f in favorite]
	context = {'favorites': favorites}
	return render(request, 'music_saver/music/favorites.html', context)


def view_liked(request, username: str):
	user = User.objects.filter(username=username).first()
	liked = Like.objects.filter(user=user).select_related('song')
	likedsongs = [s.song for s in liked]
	context = {'songs': likedsongs}
	return render(request, 'music_saver/music/liked_songs.html', context)

def delete_liked_table(request, id: int):
	like = Like.objects.filter(id=id, user=request.user).first()
	if like:
		like.delete()
		return JsonResponse({"success": True})
	return JsonResponse({'error': 'Not found'}, status=404)

def delete_disliked_table(request, id: int):
	dislike = DisLike.objects.filter(id=id, user=request.user).first()
	if dislike:
		dislike.delete()
		return JsonResponse({"success": True})
	return JsonResponse({'error': 'Not found'}, status=404)

def delete_fav_table(request, id: int):
	fav = Favorite.objects.filter(id=id, user=request.user).first()
	if fav:
		fav.delete()
		return JsonResponse({"success": True})
	return JsonResponse({'error': 'Not found'}, status=404)

def home(request):
	songs = Song.objects.all().order_by("created_at")
	paginator = Paginator(songs, 8)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context = {'songs': songs, 'page_obj': page_obj}
	return render(request, "music_saver/music/home.html", context)

def search(request):
	q = request.GET.get('q', '').strip()
	results = []
	for song in Song.objects.filter(Q(title__icontains=q) | Q(author__icontains=q)):
		results.append({"type": "Song", "item": song})
	for playlist in Playlist.objects.filter(title__icontains=q, is_public=True):
		results.append({"type": "Playlist", "item": playlist})
	context = {"q": q, "results": results}
	return render(request, "music_saver/search/search.html", context)

def search_ajax(request):
	q = request.GET.get('q', '').strip()
	results = []

	for song in Song.objects.filter(Q(title__icontains=q) | Q(author__icontains=q)):
		results.append({"type": "Song", "item": {"id": song.id, "title": song.title, "author": song.author}})
	for playlist in Playlist.objects.filter(title__icontains=q, is_public=True):
		results.append({"type": "Playlist", "item": {"id": playlist.id, "title": playlist.title}})

	return JsonResponse({
		'results': results,
		'success': True,
		"q": q,
		"username": request.user.username if request.user.is_authenticated else None
	}, status=200)

@login_required(login_url="/login")
def view_song(request, title: str):
	title = title.strip()
	song = Song.objects.filter(title__iexact=title).first()
	comments = song.comments.filter(parent__isnull=True).all()
	AddForm = AddComment()
	AddPlaylistForm = AddPlayList()
	user = request.user
	is_fav = song.favorites.filter(user=user).exists()
	has_like = song.likes.filter(user=user).exists()
	has_dislike = song.dislikes.filter(user=user).exists()

	context = {
		'song': song,
		'comments': comments,
		'comment_form': AddForm,
		'add_playlist_form': AddPlaylistForm,
		'is_fav': is_fav,
		'has_like': has_like,
		'has_dislike': has_dislike,
	}
	return render(request, "music_saver/music/detail.html", context)

@login_required(login_url="/login")
def add_song(request):
	if request.method == "POST":
		form = AddSong(request.POST, request.FILES) 
		if form.is_valid():
			song = form.save(commit=False) 
			song.user = request.user      
			song.save()                    
			return redirect(reverse("home"))
	else:
		form = AddSong()
	context = {"form": form}
	return render(request, "music_saver/music/add_song.html", context)

@login_required(login_url="/login")
def edit_song(request, id: int):
	song = Song.objects.get(id=id)
	if request.method == "POST":
		form = AddSong(request.POST, request.FILES, instance=song)
		if form.is_valid():
			form.save()
			return redirect(reverse('view_song', args=[song.title]))
	else:
		form = AddSong(instance=song)
	return render(request, 'music_saver/music/edit_song.html', {'form': form})

@login_required(login_url="/login")
def delete_song_table(request, id: int):
	song = Song.objects.get(id=id)
	if request.method == "POST":
		song.delete()
		return JsonResponse({"success": True})
	return JsonResponse({'error': 'Invalid method'}, status=400)

@login_required(login_url="/login")
def add_view(request, id: int):
	if request.method == "POST":
		song = Song.objects.get(id=id)
		song.views += 1
		song.save(update_fields=["views"])
		return JsonResponse({"success": True, "views": song.views})
	return JsonResponse({'error': 'Invalid method'}, status=400)

@login_required(login_url="/login")
def like(request, id: int):
	if request.method == "POST":
		song = Song.objects.get(id=id)
		ext_like = Like.objects.filter(song=song, user=request.user)
		if ext_like.exists():
			ext_like.delete()
			has_like = False
		else:
			Like.objects.create(song=song, user=request.user)
			DisLike.objects.filter(song=song, user=request.user).delete()
			has_like = True
		likes_count = Like.objects.filter(song=song).count()
		return JsonResponse({'success': True, 'has_like': has_like, 'likes_count': likes_count})
	return JsonResponse({'error': 'Invalid action'}, status=400)

@login_required(login_url="/login")
def dislike(request, id: int):
	if request.method == "POST":	
		song = Song.objects.get(id=id)
		ext_dislike = DisLike.objects.filter(song=song, user=request.user)
		if ext_dislike.exists():
			ext_dislike.delete()
			has_dislike = False
		else:
			DisLike.objects.create(song=song, user=request.user)
			Like.objects.filter(song=song, user=request.user).delete()
			has_dislike = True
		return JsonResponse({'success': True, 'has_dislike': has_dislike})
	return JsonResponse({'error': 'Invalid action'}, status=400)

@login_required(login_url="/login")
def fav(request, id: int):
	if request.method == "POST":
		song = Song.objects.get(id=id)
		ext_fav = Favorite.objects.filter(song=song, user=request.user)
		if ext_fav.exists():
			ext_fav.delete()
			is_fav = False
		else:
			Favorite.objects.create(song=song, user=request.user)
			is_fav = True
		return JsonResponse({'success': True, 'is_fav': is_fav})
	return JsonResponse({'error': 'Invalid action'}, status=400)

@login_required(login_url="/login")
def un_fav_ajax(request, id: int):
	if request.headers.get('x-requested-with') == 'XMLHttpRequest':
		fav = Favorite.objects.filter(song_id=id, user=request.user).first()
		if fav:
			fav.delete()
		return JsonResponse({"success": True}, status=200)
	return JsonResponse({'error': 'Invalid method'}, status=400)

@login_required(login_url="/login")
def un_like_ajax(request, id: int):
	if request.headers.get('x-requested-with') == 'XMLHttpRequest':
		like = Like.objects.filter(song_id=id, user=request.user).first()
		if like:
			like.delete()
		return JsonResponse({"success": True}, status=200)
	return JsonResponse({'error': 'Invalid method'}, status=400)

@login_required(login_url="/login")
def delete_song_in_playlist(request, playlist_id: int, song_id: int):
	if request.headers.get('x-requested-with') == 'XMLHttpRequest':
		song = Song.objects.get(id=song_id)
		playlist = Playlist.objects.get(id=playlist_id)
		playlist.songs.remove(song)
		return JsonResponse({"success": True}, status=200)
	return JsonResponse({'error': 'Invalid method'}, status=400)

@login_required(login_url="/login")
def add_comment(request, id: int):
	song = Song.objects.get(id=id)
	if request.method == "POST":
		comment_form = AddComment(request.POST)
		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)
			new_comment.user = request.user
			new_comment.song = song
			parent_id = request.POST.get('parent')
			if parent_id:
				try:
					parent_comment = Comment.objects.get(id=parent_id)
					new_comment.parent = parent_comment
				except Comment.DoesNotExist:
					pass
			new_comment.save()
			return JsonResponse({
				'status': 'success',
				'success': True,
				'id': new_comment.id,
				'user': new_comment.user.username,
				'label': new_comment.label,
				'text': new_comment.text,
				'created_at': localtime(new_comment.created_at).strftime("%Y-%m-%d %H:%M"),
				'is_author': request.user == new_comment.user
			})
	return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@login_required(login_url="/login")
def edit_comment(request, id: int):
	comment = Comment.objects.get(id=id)
	if request.headers.get('x-requested-with') == 'XMLHttpRequest':
		comment_form = AddComment(request.POST, instance=comment)
		if comment_form.is_valid():
			comment_form.save()
			return JsonResponse({'success': True, 'text': comment.text, 'label': comment.label})
		else:
			return JsonResponse({'success': False, 'errors': comment_form.errors}, status=400)
	return JsonResponse({'success': False, 'error': 'Invalid method'}, status=400)

@login_required(login_url="/login")
def delete_comment(request, id: int):
	comment = Comment.objects.get(id=id)
	if request.method == "POST":
		comment.delete()
		return JsonResponse({"success": True,"id": id})
	return JsonResponse({'error': 'Invalid method'}, status=400)

@login_required(login_url="/login")
def delete_comment_table(request, username: str, id: int):
	comment = Comment.objects.get(id=id)
	if request.method == "POST":
		comment.delete()
		return JsonResponse({"success": True})
	return JsonResponse({'error': 'Invalid method'}, status=400)


@login_required(login_url="/login")
def view_playlists(request, username: str):
	user = User.objects.filter(username=username).first()
	playlists = user.playlists.all()
	if request.POST:
		add_playlist_form = AddPlayList(request.POST)
		if add_playlist_form.is_valid():
			new_playlist = add_playlist_form.save(commit=False)
			new_playlist.user = user
			new_playlist.save()
			return redirect(reverse("view_playlists", args=[username]))
	else:
		add_playlist_form = AddPlayList()
	context = {'playlists': playlists, 'add_playlist_form': add_playlist_form}
	return render(request, 'music_saver/music/playlists.html', context)

@login_required(login_url="/login")
def view_playlist(request, username: str, title: str):
    title = title.strip()
    playlist = get_object_or_404(
        Playlist,
        user__username=username,
        title__iexact=title
    )
    songs = playlist.songs.all()
    playlist.views += 1
    playlist.save(update_fields=['views'])
    context = {
        'songs': songs,
        'title': playlist.title,
        'playlist': playlist
    }
    return render(request, 'music_saver/music/playlist.html', context)

@login_required(login_url="/login")
def add_to_playlist(request, id: int):
	if request.POST:
		song = Song.objects.get(id=id)
		playlist_id = request.POST.get('playlist')
		if playlist_id:
			playlist = Playlist.objects.get(id=playlist_id)
			playlist.songs.add(song)
		return JsonResponse({"success": True}, status=200)
	return JsonResponse({'error': 'Invalid action'}, status=400)

@login_required(login_url="/login")
def add_playlist(request, id: int):
	if request.POST:
		add_playlist_form = AddPlayList(request.POST)
		if add_playlist_form.is_valid():
			new_playlist = add_playlist_form.save(commit=False)
			new_playlist.user = request.user
			new_playlist.save()
			return JsonResponse({'success': True, "username": request.user.username}, status=200)
	return JsonResponse({'error': 'Invalid action'}, status=400)

@login_required(login_url="/login")
def add_playlist_(request):
	if request.POST:
		add_playlist_form = AddPlayList(request.POST)
		if add_playlist_form.is_valid():
			new_playlist = add_playlist_form.save(commit=False)
			new_playlist.user = request.user
			new_playlist.save()
			return JsonResponse({
				'success': True,
				'id': new_playlist.id,
				'title': new_playlist.title,
				'is_public': new_playlist.is_public,
				'created_at': new_playlist.created_at.strftime('%d %b %Y'),
				'username': request.user.username,
			})
	return JsonResponse({'error': 'Invalid action'}, status=400)

@login_required(login_url="/login")
def edit_playlist_data(request, id: int):
	playlist = Playlist.objects.get(id=id)
	if request.headers.get('x-requested-with') == 'XMLHttpRequest':
		playlist_form = AddPlayList(request.POST, instance=playlist)
		if playlist_form.is_valid():
			playlist_form.save()
			return JsonResponse({'success': True, 'title': playlist.title, 'is_public': playlist.is_public}, status=200)
		else:
			return JsonResponse({'success': False, 'errors': playlist_form.errors}, status=400)
	return JsonResponse({'success': False, 'error': 'Invalid method'}, status=400)

@login_required(login_url="/login")
def delete_playlist_table(request, id: int):
	playlist = Playlist.objects.get(id=id)
	if request.method == "POST":
		playlist.delete()
		return JsonResponse({"success": True})
	return JsonResponse({'error': 'Invalid method'}, status=400)

@login_required(login_url="/login")
def delete_playlist_ajax(request, id: int):
	if request.headers.get('x-requested-with') == 'XMLHttpRequest':
		playlist = Playlist.objects.get(id=id)
		playlist.delete()
		return JsonResponse({"success": True}, status=200)
	return JsonResponse({'error': 'Invalid method'}, status=400)
