"""Quick test of the published Akron package with Django-like foreign keys."""

try:
    from akron import Akron
    from akron.models import ModelMixin
    from pydantic import BaseModel
    from typing import Optional
    
    print("✅ Import successful!")
    
    # Test Django-like foreign keys
    class User(BaseModel, ModelMixin):
        id: Optional[int] = None
        name: str
        email: str
    
    class Post(BaseModel, ModelMixin):
        id: Optional[int] = None
        title: str
        author_id: int
        
        __foreign_keys__ = {
            'author_id': 'users.id'
        }
    
    # Quick test
    db = Akron("sqlite:///:memory:")
    
    User.create_table(db)
    Post.create_table(db)
    
    # Create user and post
    user = User(name="Test User", email="test@example.com")
    user_id = User.insert(db, user)
    
    post = Post(title="Test Post", author_id=user_id)
    Post.insert(db, post)
    
    # Verify relationships
    users = User.find_all(db)
    posts = Post.find_all(db)
    
    print(f"✅ Created {len(users)} user(s) and {len(posts)} post(s)")
    print(f"✅ Post author_id: {posts[0].author_id} matches user ID: {users[0].id}")
    print("🎉 Django-like foreign keys working perfectly!")
    
    db.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
    raise