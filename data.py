from models import User, Work, Character, Post
from werkzeug.security import generate_password_hash

# In-memory storage
users = {}
works = {}
characters = {}
posts = {}

# Counters for IDs
user_counter = 1
work_counter = 1
character_counter = 1
post_counter = 1

def get_next_user_id():
    global user_counter
    user_counter += 1
    return user_counter - 1

def get_next_work_id():
    global work_counter
    work_counter += 1
    return work_counter - 1

def get_next_character_id():
    global character_counter
    character_counter += 1
    return character_counter - 1

def get_next_post_id():
    global post_counter
    post_counter += 1
    return post_counter - 1

def init_data():
    """Initialize the app with test data"""
    # Create works
    aot = Work(get_next_work_id(), "Attack on Titan", "進撃の巨人", "A dark fantasy anime about humanity's fight against titans")
    ds = Work(get_next_work_id(), "Demon Slayer", "鬼滅の刃", "A supernatural action anime about demon hunters")
    jjk = Work(get_next_work_id(), "Jujutsu Kaisen", "呪術廻戦", "A supernatural action anime about jujutsu sorcerers")
    
    works[aot.id] = aot
    works[ds.id] = ds
    works[jjk.id] = jjk
    
    # Create characters for Attack on Titan
    eren = Character(get_next_character_id(), "Eren Yeager", "エレン・イェーガー", aot.id, "Main protagonist")
    mikasa = Character(get_next_character_id(), "Mikasa Ackerman", "ミカサ・アッカーマン", aot.id, "Eren's childhood friend")
    levi = Character(get_next_character_id(), "Levi Ackerman", "リヴァイ・アッカーマン", aot.id, "Captain of Special Operations Squad")
    hange = Character(get_next_character_id(), "Hange Zoe", "ハンジ・ゾエ", aot.id, "14th Commander of Survey Corps")
    
    # Create characters for Demon Slayer
    tanjiro = Character(get_next_character_id(), "Tanjiro Kamado", "竈門炭治郎", ds.id, "Main protagonist")
    nezuko = Character(get_next_character_id(), "Nezuko Kamado", "竈門禰豆子", ds.id, "Tanjiro's sister")
    zenitsu = Character(get_next_character_id(), "Zenitsu Agatsuma", "我妻善逸", ds.id, "Thunder Breathing user")
    giyu = Character(get_next_character_id(), "Giyu Tomioka", "冨岡義勇", ds.id, "Water Hashira")
    
    # Create characters for Jujutsu Kaisen
    yuji = Character(get_next_character_id(), "Yuji Itadori", "虎杖悠仁", jjk.id, "Main protagonist")
    gojo = Character(get_next_character_id(), "Satoru Gojo", "五条悟", jjk.id, "Special Grade Jujutsu Sorcerer")
    nobara = Character(get_next_character_id(), "Nobara Kugisaki", "釘崎野薔薇", jjk.id, "First-year student")
    megumi = Character(get_next_character_id(), "Megumi Fushiguro", "伏黒恵", jjk.id, "First-year student")
    
    # Add characters to storage
    for char in [eren, mikasa, levi, hange, tanjiro, nezuko, zenitsu, giyu, yuji, gojo, nobara, megumi]:
        characters[char.id] = char
        works[char.work_id].add_character(char)

def create_user(username, email, password, nickname="", bio="", language="en"):
    """Create a new user"""
    user_id = get_next_user_id()
    password_hash = generate_password_hash(password)
    user = User(user_id, username, email, password_hash, nickname, bio, language)
    users[user_id] = user
    return user

def get_user_by_email(email):
    """Get user by email"""
    for user in users.values():
        if user.email == email:
            return user
    return None

def get_user_by_username(username):
    """Get user by username"""
    for user in users.values():
        if user.username == username:
            return user
    return None

def create_post(user_id, content, work_id=None, character_id=None, parent_id=None):
    """Create a new post"""
    post_id = get_next_post_id()
    post = Post(post_id, user_id, content, work_id, character_id, parent_id)
    posts[post_id] = post
    
    # If it's a reply, add to parent's replies
    if parent_id and parent_id in posts:
        posts[parent_id].replies.append(post_id)
    
    return post

def get_posts_for_user_timeline(user_id):
    """Get posts for user's home timeline"""
    if user_id not in users:
        return []
    
    user = users[user_id]
    timeline_posts = []
    
    for post in posts.values():
        # Include posts from followed users
        if post.user_id in user.following_users:
            timeline_posts.append(post)
        # Include posts from followed works
        elif post.work_id in user.following_works:
            timeline_posts.append(post)
        # Include posts from followed characters
        elif post.character_id in user.following_characters:
            timeline_posts.append(post)
        # Include user's own posts
        elif post.user_id == user_id:
            timeline_posts.append(post)
    
    # Sort by creation time (newest first)
    timeline_posts.sort(key=lambda x: x.created_at, reverse=True)
    return timeline_posts

def get_posts_for_work(work_id):
    """Get all posts for a specific work"""
    work_posts = [post for post in posts.values() if post.work_id == work_id]
    work_posts.sort(key=lambda x: x.created_at, reverse=True)
    return work_posts

def get_posts_for_character(character_id):
    """Get all posts for a specific character"""
    character_posts = [post for post in posts.values() if post.character_id == character_id]
    character_posts.sort(key=lambda x: x.created_at, reverse=True)
    return character_posts

def get_popular_works():
    """Get popular works based on post count"""
    work_post_counts = {}
    for post in posts.values():
        if post.work_id:
            work_post_counts[post.work_id] = work_post_counts.get(post.work_id, 0) + 1
    
    popular_works = sorted(work_post_counts.items(), key=lambda x: x[1], reverse=True)
    return [works[work_id] for work_id, _ in popular_works[:5]]

def get_popular_characters():
    """Get popular characters based on post count"""
    character_post_counts = {}
    for post in posts.values():
        if post.character_id:
            character_post_counts[post.character_id] = character_post_counts.get(post.character_id, 0) + 1
    
    popular_characters = sorted(character_post_counts.items(), key=lambda x: x[1], reverse=True)
    return [characters[char_id] for char_id, _ in popular_characters[:8]]

def get_latest_posts(limit=10):
    """Get latest posts across all works and characters"""
    latest_posts = sorted(posts.values(), key=lambda x: x.created_at, reverse=True)
    return latest_posts[:limit]
