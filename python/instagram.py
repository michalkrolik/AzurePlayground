import instaloader, datetime, hashlib, time, json, uuid, os, requests
from instaloader import Instaloader, Profile

#After 200 spooled files:
#Too many queries in the last time. Need to wait 228 seconds, until 07:00 (5 minutes)

now = datetime.datetime.now()
current_date = datetime.datetime.strftime(now, "%Y%m%d")

L = instaloader.Instaloader()

account = 'xxx'
password = 'xxx'
L.login(account, password)

username = 'candf_com'

Output_profile = f'/home/mike/Desktop/Instagram/python/myenv/{username}/profile'
Output_posts = f'/home/mike/Desktop/Instagram/python/myenv/{username}/posts'
Output_media = f'/home/mike/Desktop/Instagram/python/myenv/{username}/media'

for dir in [Output_profile, Output_posts, Output_media]:
    if not os.path.exists(f'{dir}'):
        os.makedirs(f'{dir}')

profile = instaloader.Profile.from_username(L.context, username)

profile_data = {
    'username': profile.username,
    'full_name': profile.full_name,
    'biography': profile.biography,
    'followers': profile.followers,
    'following': profile.followees,
    'posts': profile.mediacount,
    'ingestion_date': str(now)
}

with open(f'{Output_profile}/{username}_{current_date}.json', 'w') as json_file:
    json.dump(profile_data, json_file, indent=4)

for post in profile.get_posts():
    data = {}
    unique_id = str(uuid.uuid4())

    post_date = post.date
    post_pic_url = post.url
    post_vid_url = post.video_url
    post_vid_view_count = post.video_view_count
    post_caption = post.caption
    post_likes = post.likes
    post_comments = post.comments
    post_hashtags = post.caption_hashtags
    post_mentions = post.caption_mentions

    post_date_format = datetime.datetime.strptime(str(post_date), "%Y-%m-%d %H:%M:%S")
    post_unix_date = int(post_date_format.timestamp())
    post_date_new_format = post_date_format.strftime("%Y%m%d")

    comments = {}
    for comment in post.get_comments():
        comm_id = comment.id
        comm_text = comment.text
        comm_date = comment.created_at_utc
        comm_owner = comment.owner
        comm_likes = comment.likes_count
        comments[comm_id] = {
            'author': str(comm_owner),
            'date': str(comm_date),
            'text': str(comm_text),
            'likes': comm_likes}
    
    if post_pic_url:
        media = 'photo'
        response = requests.get(post_pic_url)
        with open(f'{Output_media}/{unique_id}.jpg', 'wb') as file:
            file.write(response.content)

    if post_vid_url:
        media = 'video'
        response = requests.get(post_vid_url)
        with open(f'{Output_media}/{unique_id}.mp4', 'wb') as file:
            file.write(response.content)

    data["data"] = {
        'uuid': unique_id,
        'date': post_unix_date,
        'media': media,
        'picture':post_pic_url,
        'video': post_vid_url,
        'video_viewers_count': post_vid_view_count,
        'caption':post_caption,
        'likes': post_likes,
        'hashtags': post_hashtags,
        'mentions': post_mentions,
        'post_comments': post_comments,
        'comments': comments,
        'ingestion_date': str(now)}

    with open(f'{Output_posts}/{str(unique_id)}_{str(post_date_new_format)}_{current_date}.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
