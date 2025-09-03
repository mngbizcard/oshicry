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
    
    # Create sample users
    user1 = create_user("anime_fan_2024", "fan@example.com", "password123", "AnimeOtaku", "Big fan of shounen anime! Gojo is my oshi 💜", "en")
    user2 = create_user("manga_reader", "reader@example.com", "password123", "MangaLover", "Reading manga since 2010. Attack on Titan changed my life!", "en")
    user3 = create_user("otaku_senpai", "senpai@example.com", "password123", "OtakuSenpai", "先輩です！アニメが大好きです。", "ja")
    user4 = create_user("cry_for_oshi", "cry@example.com", "password123", "CryForOshi", "Emotional about every character death 😭", "en")
    user5 = create_user("tanjiro_stan", "tanjiro@example.com", "password123", "TanjiroStan", "Demon Slayer is the best anime ever created!", "en")
    
    # Make users follow some works and characters
    user1.follow_work(jjk.id)
    user1.follow_character(gojo.id)
    user1.follow_character(yuji.id)
    
    user2.follow_work(aot.id)
    user2.follow_character(eren.id)
    user2.follow_character(levi.id)
    
    user3.follow_work(ds.id)
    user3.follow_character(tanjiro.id)
    user3.follow_character(nezuko.id)
    
    user4.follow_character(mikasa.id)
    user4.follow_character(nezuko.id)
    user4.follow_character(nobara.id)
    
    user5.follow_work(ds.id)
    user5.follow_character(tanjiro.id)
    user5.follow_character(giyu.id)
    
    # Create sample posts
    sample_posts = [
        # Jujutsu Kaisen posts
        (user1.id, "Gojo's domain expansion is literally the most beautiful thing in anime! The visual effects are insane! 🔥", jjk.id, gojo.id),
        (user1.id, "Yuji's character development this season has me crying every episode... he deserves the world 😭", jjk.id, yuji.id),
        (user4.id, "Nobara is such an underrated character! Her confidence and strength inspire me every day 💪", jjk.id, nobara.id),
        
        # Attack on Titan posts
        (user2.id, "That final scene with Eren... I'm still not over it. What a masterpiece of storytelling!", aot.id, eren.id),
        (user2.id, "Levi vs Beast Titan is still the best fight scene in all of anime. PERIODT.", aot.id, levi.id),
        (user4.id, "Mikasa deserved so much better. My heart breaks for her every time I rewatch the ending 💔", aot.id, mikasa.id),
        (user3.id, "進撃の巨人の最終回を見た後、まだ泣いています。。。", aot.id, None),
        
        # Demon Slayer posts
        (user5.id, "Tanjiro's kindness towards demons makes him the best protagonist in shounen anime!", ds.id, tanjiro.id),
        (user5.id, "The animation quality in the Entertainment District arc was absolutely phenomenal!", ds.id, None),
        (user3.id, "禰豆子ちゃんが可愛すぎる！保護したい！", ds.id, nezuko.id),
        (user4.id, "Every time Zenitsu powers up I get literal chills. Thunder breathing is so cool!", ds.id, zenitsu.id),
        (user5.id, "Giyu's backstory episode had me sobbing for hours. He's been through so much pain...", ds.id, giyu.id),
        
        # General anime posts
        (user1.id, "Why do all my favorite characters have to suffer so much? 😭 Anime really knows how to break hearts", None, None),
        (user2.id, "Currently rewatching all three series and the emotional damage is real... worth it though!", None, None),
        (user3.id, "新しいアニメシーズンが楽しみです！皆さんのおすすめはありますか？", None, None),
    ]
    
    # Create the posts and add some reactions
    for user_id, content, work_id, character_id in sample_posts:
        post = create_post(user_id, content, work_id, character_id)
        
        # Add some random reactions to posts
        import random
        reaction_types = ['heart', 'fire', 'cry']
        for _ in range(random.randint(1, 4)):  # 1-4 reactions per post
            reactor_id = random.choice([user1.id, user2.id, user3.id, user4.id, user5.id])
            reaction_type = random.choice(reaction_types)
            if not post.user_reacted(reactor_id, reaction_type):
                post.add_reaction(reactor_id, reaction_type)
    
    # Create some replies
    first_post = list(posts.values())[0] if posts else None
    if first_post:
        reply1 = create_post(user2.id, "I totally agree! Gojo is literally perfection ✨", first_post.work_id, first_post.character_id, first_post.id)
        reply2 = create_post(user3.id, "五条先生最高です！", first_post.work_id, first_post.character_id, first_post.id)
        
        # Add reactions to replies
        reply1.add_reaction(user1.id, 'heart')
        reply1.add_reaction(user4.id, 'heart')
        reply2.add_reaction(user1.id, 'fire')

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
