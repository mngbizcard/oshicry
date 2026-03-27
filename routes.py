from flask import render_template, request, redirect, url_for, session, flash, jsonify
from urllib.parse import urlparse
from app import app
import data
from models import User
import logging

def safe_redirect_url(referrer_url, fallback_url):
    """Validate referrer URL to prevent open redirect attacks."""
    if not referrer_url:
        return fallback_url
    
    try:
        parsed_referrer = urlparse(referrer_url)
        parsed_request = urlparse(request.url)
        
        # Only allow redirects to the same domain (netloc)
        if parsed_referrer.netloc == parsed_request.netloc:
            return referrer_url
    except (ValueError, AttributeError):
        pass
    
    return fallback_url

# Language translations
TRANSLATIONS = {
    'en': {
        'app_name': 'OshiCRY',
        'home': 'Home',
        'works': 'Works',
        'profile': 'Profile',
        'login': 'Login',
        'register': 'Register',
        'logout': 'Logout',
        'post_cry': 'Post a Cry',
        'whats_happening': "思いの丈を叫んで(`・ω・´)b",
        'popular_works': 'Popular Works',
        'popular_characters': 'Popular Characters',
        'latest_cries': 'Latest Cries',
        'follow': 'Follow',
        'unfollow': 'Unfollow',
        'reply': 'Reply',
        'characters': 'Characters',
        'posts': 'Posts',
        'followers': 'Followers',
        'following': 'Following',
        'official_partnership_projects': 'Official Partnership Projects',
        'kadokawa_partnership': 'Kadokawa Partnership Project',
        'kadokawa_description': 'Exclusive content collaboration with major anime publishers',
        'premium_content': 'Premium Content',
        'shueisha_collaboration': 'Shueisha Collaboration Campaign',
        'shueisha_description': 'Special events and character spotlights from top manga series',
        'live_events': 'Live Events',
        'kodansha_creator_support': 'Kodansha Creator Support Program',
        'kodansha_description': 'Community-driven content creation and fan appreciation',
        'creator_hub': 'Creator Hub'
    },
    'ja': {
        'app_name': '推しCRY',
        'home': 'ホーム',
        'works': '作品',
        'profile': 'プロフィール',
        'login': 'ログイン',
        'register': '登録',
        'logout': 'ログアウト',
        'post_cry': 'クライを投稿',
        'whats_happening': '思いの丈を叫んで(`・ω・´)b',
        'popular_works': '人気作品',
        'popular_characters': '人気キャラクター',
        'latest_cries': '最新のクライ',
        'follow': 'フォロー',
        'unfollow': 'フォロー解除',
        'reply': '返信',
        'characters': 'キャラクター',
        'posts': '投稿',
        'followers': 'フォロワー',
        'following': 'フォロー中',
        'official_partnership_projects': '公式パートナープロジェクト',
        'kadokawa_partnership': 'KADOKAWAパートナーシッププロジェクト',
        'kadokawa_description': '主要アニメ出版社との独占コンテンツコラボレーション',
        'premium_content': 'プレミアムコンテンツ',
        'shueisha_collaboration': '集英社コラボレーションキャンペーン',
        'shueisha_description': 'トップ漫画シリーズの特別イベントとキャラクタースポットライト',
        'live_events': 'ライブイベント',
        'kodansha_creator_support': '講談社クリエイターサポートプログラム',
        'kodansha_description': 'コミュニティ主導のコンテンツ制作とファン感謝',
        'creator_hub': 'クリエイターハブ'
    }
}

def get_translation(key, lang='en'):
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)

def get_current_user():
    if 'user_id' in session:
        return data.users.get(session['user_id'])
    return None

@app.context_processor
def inject_user():
    user = get_current_user()
    lang = session.get('language', 'en')
    return {
        'current_user': user,
        'lang': lang,
        't': lambda key: get_translation(key, lang),
        'works': data.works,
        'characters': data.characters,
        'users': data.users
    }

@app.route('/')
def index():
    user = get_current_user()
    
    if user:
        # Show personalized timeline
        timeline_posts = data.get_posts_for_user_timeline(user.id)
    else:
        # Show general latest posts
        timeline_posts = data.get_latest_posts()
    
    popular_works = data.get_popular_works()
    popular_characters = data.get_popular_characters()
    
    return render_template('index.html', 
                         posts=timeline_posts,
                         popular_works=popular_works,
                         popular_characters=popular_characters,
                         works=data.works,
                         characters=data.characters,
                         users=data.users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = data.get_user_by_email(email)
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['language'] = user.language
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        nickname = request.form.get('nickname', '')
        bio = request.form.get('bio', '')
        language = request.form.get('language', 'en')
        
        # Check if user already exists
        if data.get_user_by_email(email):
            flash('Email already registered.', 'error')
            return render_template('register.html')
        
        if data.get_user_by_username(username):
            flash('Username already taken.', 'error')
            return render_template('register.html')
        
        # Create new user
        user = data.create_user(username, email, password, nickname, bio, language)
        session['user_id'] = user.id
        session['language'] = user.language
        flash('Registration successful!', 'success')
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/profile')
@app.route('/profile/<int:user_id>')
def profile(user_id=None):
    current_user = get_current_user()
    
    if user_id is None:
        if not current_user:
            return redirect(url_for('login'))
        profile_user = current_user
    else:
        profile_user = data.users.get(user_id)
        if not profile_user:
            flash('User not found.', 'error')
            return redirect(url_for('index'))
    
    # Get user's posts
    user_posts = [post for post in data.posts.values() if post.user_id == profile_user.id]
    user_posts.sort(key=lambda x: x.created_at, reverse=True)
    
    return render_template('profile.html', 
                         profile_user=profile_user,
                         posts=user_posts,
                         works=data.works,
                         characters=data.characters,
                         users=data.users)

@app.route('/work/<int:work_id>')
def work(work_id):
    work = data.works.get(work_id)
    if not work:
        flash('Work not found.', 'error')
        return redirect(url_for('index'))
    
    work_posts = data.get_posts_for_work(work_id)
    
    return render_template('work.html',
                         work=work,
                         posts=work_posts,
                         characters=data.characters,
                         users=data.users)

@app.route('/character/<int:character_id>')
def character(character_id):
    character = data.characters.get(character_id)
    if not character:
        flash('Character not found.', 'error')
        return redirect(url_for('index'))
    
    work = data.works.get(character.work_id)
    character_posts = data.get_posts_for_character(character_id)
    
    return render_template('character.html',
                         character=character,
                         work=work,
                         posts=character_posts,
                         users=data.users)

@app.route('/post', methods=['POST'])
def create_post():
    current_user = get_current_user()
    if not current_user:
        flash('Please log in to post.', 'error')
        return redirect(url_for('login'))
    
    content = request.form['content'].strip()
    work_id = request.form.get('work_id')
    character_id = request.form.get('character_id')
    parent_id = request.form.get('parent_id')
    scene = request.form.get('scene')
    custom_work = request.form.get('custom_work', '').strip()
    custom_character = request.form.get('custom_character', '').strip()
    custom_scene = request.form.get('custom_scene', '').strip()
    
    if not content:
        flash('Post content cannot be empty.', 'error')
        return redirect(safe_redirect_url(request.referrer, url_for('index')))
    
    if len(content) > 280:
        flash('Post content cannot exceed 280 characters.', 'error')
        return redirect(safe_redirect_url(request.referrer, url_for('index')))
    
    # Check if work is required (not empty and not "custom" without custom_work)
    if not work_id or (work_id == 'custom' and not custom_work):
        flash('Please select a work or enter a custom work name.', 'error')
        return redirect(safe_redirect_url(request.referrer, url_for('index')))
    
    # Handle custom inputs
    if work_id == 'custom':
        work_id = None  # Use custom_work instead
    
    if character_id == 'custom':
        character_id = None  # Use custom_character instead
    
    if scene == 'custom':
        scene = custom_scene if custom_scene else None
    
    # Convert string IDs to integers
    work_id = int(work_id) if work_id and work_id != 'None' and work_id != 'custom' else None
    character_id = int(character_id) if character_id and character_id != 'None' and character_id != 'custom' else None
    parent_id = int(parent_id) if parent_id and parent_id != 'None' else None
    
    post = data.create_post(current_user.id, content, work_id, character_id, parent_id, scene, custom_work, custom_character, custom_scene)
    flash('Cry posted successfully!', 'success')
    
    return redirect(safe_redirect_url(request.referrer, url_for('index')))

@app.route('/react/<int:post_id>/<reaction_type>')
def react_to_post(post_id, reaction_type):
    current_user = get_current_user()
    if not current_user:
        flash('Please log in to react.', 'error')
        return redirect(url_for('login'))
    
    post = data.posts.get(post_id)
    if not post:
        flash('Post not found.', 'error')
        return redirect(safe_redirect_url(request.referrer, url_for('index')))
    
    # Toggle reaction
    if post.user_reacted(current_user.id, reaction_type):
        post.remove_reaction(current_user.id, reaction_type)
    else:
        post.add_reaction(current_user.id, reaction_type)
    
    return redirect(safe_redirect_url(request.referrer, url_for('index')))

@app.route('/follow/<follow_type>/<int:target_id>')
def follow(follow_type, target_id):
    current_user = get_current_user()
    if not current_user:
        flash('Please log in to follow.', 'error')
        return redirect(url_for('login'))
    
    if follow_type == 'user':
        if target_id in current_user.following_users:
            current_user.unfollow_user(target_id)
            flash('Unfollowed user.', 'info')
        else:
            current_user.follow_user(target_id)
            flash('Following user.', 'success')
    elif follow_type == 'work':
        if target_id in current_user.following_works:
            current_user.unfollow_work(target_id)
            flash('Unfollowed work.', 'info')
        else:
            current_user.follow_work(target_id)
            flash('Following work.', 'success')
    elif follow_type == 'character':
        if target_id in current_user.following_characters:
            current_user.unfollow_character(target_id)
            flash('Unfollowed character.', 'info')
        else:
            current_user.follow_character(target_id)
            flash('Following character.', 'success')
    
    return redirect(safe_redirect_url(request.referrer, url_for('index')))

@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = data.posts.get(post_id)
    if not post:
        flash('Post not found.', 'error')
        return redirect(url_for('index'))
    
    # Get replies
    replies = [data.posts[reply_id] for reply_id in post.replies if reply_id in data.posts]
    
    return render_template('post.html',
                         post=post,
                         replies=replies,
                         works=data.works,
                         characters=data.characters,
                         users=data.users)

@app.route('/set_language/<lang>')
def set_language(lang):
    if lang in ['en', 'ja']:
        session['language'] = lang
        user = get_current_user()
        if user:
            user.language = lang
    return redirect(safe_redirect_url(request.referrer, url_for('index')))
