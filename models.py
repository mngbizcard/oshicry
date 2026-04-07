from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, user_id, username, email, password_hash, nickname="", bio="", language="en"):
        self.id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.nickname = nickname or username
        self.bio = bio
        self.language = language
        self.following_users = set()
        self.following_works = set()
        self.following_characters = set()
        self.following_creators = set()
        self.created_at = datetime.now()
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def follow_user(self, user_id):
        self.following_users.add(user_id)
    
    def unfollow_user(self, user_id):
        self.following_users.discard(user_id)
    
    def follow_work(self, work_id):
        self.following_works.add(work_id)
    
    def unfollow_work(self, work_id):
        self.following_works.discard(work_id)
    
    def follow_character(self, character_id):
        self.following_characters.add(character_id)
    
    def unfollow_character(self, character_id):
        self.following_characters.discard(character_id)

    def follow_creator(self, creator_id):
        self.following_creators.add(creator_id)

    def unfollow_creator(self, creator_id):
        self.following_creators.discard(creator_id)

class Creator:
    def __init__(self, creator_id, name, name_jp="", creator_type="voice_actor", description="", description_jp="", works=None):
        self.id = creator_id
        self.name = name
        self.name_jp = name_jp
        self.creator_type = creator_type  # 'author', 'voice_actor', 'animator'
        self.description = description
        self.description_jp = description_jp
        self.works = works or []  # list of work_ids
        self.characters = []  # list of character_ids (for voice actors)
        self.created_at = datetime.now()

class Work:
    def __init__(self, work_id, name, name_jp="", description=""):
        self.id = work_id
        self.name = name
        self.name_jp = name_jp
        self.description = description
        self.characters = {}
        self.created_at = datetime.now()
    
    def add_character(self, character):
        self.characters[character.id] = character

class Character:
    def __init__(self, character_id, name, name_jp="", work_id=None, description=""):
        self.id = character_id
        self.name = name
        self.name_jp = name_jp
        self.work_id = work_id
        self.description = description
        self.created_at = datetime.now()

class Post:
    def __init__(self, post_id, user_id, content, work_id=None, character_id=None, parent_id=None, scene=None, custom_work=None, custom_character=None, custom_scene=None):
        self.id = post_id
        self.user_id = user_id
        self.content = content
        self.work_id = work_id
        self.character_id = character_id
        self.parent_id = parent_id  # For replies
        self.scene = scene
        self.custom_work = custom_work
        self.custom_character = custom_character
        self.custom_scene = custom_scene
        self.reactions = {}  # reaction_type -> set of user_ids
        self.created_at = datetime.now()
        self.replies = []
    
    def add_reaction(self, user_id, reaction_type):
        if reaction_type not in self.reactions:
            self.reactions[reaction_type] = set()
        self.reactions[reaction_type].add(user_id)
    
    def remove_reaction(self, user_id, reaction_type):
        if reaction_type in self.reactions:
            self.reactions[reaction_type].discard(user_id)
    
    def get_reaction_count(self, reaction_type):
        return len(self.reactions.get(reaction_type, set()))
    
    def user_reacted(self, user_id, reaction_type):
        return user_id in self.reactions.get(reaction_type, set())
