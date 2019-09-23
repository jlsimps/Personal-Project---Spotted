import spotipy
import spotipy.util as util
import praw

# SPOTIFY CREDENTIALS AND TOKEN
SPOTIFY_ID = "a spotify client id"
SPOTIFY_SECRET = "a spotify client secret"
spotify_username = "a spotify username"
scope = 'playlist-modify-private, user-read-recently-played, playlist-modify-public'
token = util.prompt_for_user_token(username=spotify_username, scope=scope, client_id=SPOTIFY_ID,
                                   client_secret=SPOTIFY_SECRET, redirect_uri="http://localhost:8888/callback/")

# REDDIT CREDENTIALS AND TOKEN
REDDIT_ID = "a reddit client id"
REDDIT_SECRET = "a reddit client secret"
USER_AGENT = "a reddit user agent"
reddit = praw.Reddit(client_id=REDDIT_ID,
                     client_secret=REDDIT_SECRET,
                     user_agent=USER_AGENT)


def get_songs(subreddit_name):
    tracks = {}
    spotify_ids = []
    # ATTEMPTING TO FILTER OUT POSTS BASED ON KEYWORDS
    excluded_words = ['mix', 'rip', 'ama', 'live', 'album', 'ep', 'tour']
    subreddit = reddit.subreddit(subreddit_name)
    for submission in subreddit.top('week'):
        sub_lower = submission.title.lower()
        if not any(word in sub_lower for word in excluded_words):
            if "-" in sub_lower:
                tracks[sub_lower.split("-", 2)[0]] = sub_lower.split("-", 2)[1]
    for artist, song in tracks.items():
        if len(spotify_ids) < 10:
            try:
                spotify_ids.append(
                    sp.search(q='artist:{} track:{}'.format(artist, song), type="track", limit=1)['tracks']['items'][0][
                        'id'])
                print("successfully added {} - {}".format(artist, song))
            except:
                print("spotify couldn't find {} - {}".format(artist, song))
                continue

    return spotify_ids


if token:
    sp = spotipy.Spotify(auth=token)
    subreddits = ['enter', 'subreddit', 'names', 'here']
    final_ids = []
    
    # MAKING SURE THERE ARE NO DUPLICATE SONGS BEING ADDED
    for sub in subreddits:
        ids = get_songs(sub)
        for i in ids:
            if i not in final_ids:
                final_ids.append(i)

    sp.user_playlist_add_tracks(spotify_username, 'a spotify playlist id', final_ids)


else:
    print("Can't get token for", spotify_username)

