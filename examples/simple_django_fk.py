"""Simple Django-like Foreign Key Example for Akron ORM."""

from pydantic import BaseModel
from akron import Akron
from akron.models import ModelMixin
from typing import Optional

# Initialize database
db = Akron("sqlite:///django_style_blog.db")

# Define models with Django-like foreign key syntax
class User(BaseModel, ModelMixin):
    id: Optional[int] = None
    name: str
    email: str

class Post(BaseModel, ModelMixin):
    id: Optional[int] = None
    title: str
    content: str
    author_id: int  # This will be a foreign key
    published: bool = False
    
    # 🔥 Django-like foreign key definition - Simple and clean!
    __foreign_keys__ = {
        'author_id': 'users.id'  # author_id references users.id
    }

class Comment(BaseModel, ModelMixin):
    id: Optional[int] = None
    post_id: int     # This will be a foreign key
    author_name: str
    content: str
    
    # 🔥 Single foreign key reference
    __foreign_keys__ = {
        'post_id': 'posts.id'  # post_id references posts.id
    }

def main():
    print("🚀 Django-style Foreign Keys with Akron ORM")
    print("=" * 45)
    
    # 1. Create tables (foreign keys handled automatically!)
    print("\n1. Creating tables with foreign key relationships...")
    User.create_table(db)
    Post.create_table(db)    # Automatically creates author_id -> users.id
    Comment.create_table(db) # Automatically creates post_id -> posts.id
    print("✅ All tables created with foreign key constraints")
    
    # 2. Insert data with relationships
    print("\n2. Creating related records...")
    
    # Create a user
    user = User(name="Alice Johnson", email="alice@example.com")
    user_id = User.insert(db, user)
    print(f"👤 Created user: Alice (ID: {user_id})")
    
    # Create posts for the user
    post1 = Post(
        title="Getting Started with Akron",
        content="Akron makes database operations simple and intuitive...",
        author_id=user_id,  # Foreign key reference
        published=True
    )
    
    post2 = Post(
        title="Advanced Akron Features", 
        content="Let's explore transactions and advanced querying...",
        author_id=user_id,  # Foreign key reference
        published=False
    )
    
    post1_id = Post.insert(db, post1)
    post2_id = Post.insert(db, post2)
    print(f"📝 Created posts: {post1_id}, {post2_id}")
    
    # Create comments for the posts
    comment1 = Comment(
        post_id=post1_id,  # Foreign key reference
        author_name="Bob Reader",
        content="Great tutorial! Very helpful."
    )
    
    comment2 = Comment(
        post_id=post1_id,  # Foreign key reference  
        author_name="Carol Coder",
        content="Looking forward to more Akron content!"
    )
    
    Comment.insert(db, comment1)
    Comment.insert(db, comment2)
    print("💬 Created comments with post references")
    
    # 3. Query related data
    print("\n3. Querying related data...")
    
    # Find Alice's posts
    alice_posts = Post.find(db, {"author_id": user_id})
    print(f"📚 Alice has {len(alice_posts)} posts:")
    for post in alice_posts:
        status = "✅ Published" if post.published else "📝 Draft"
        print(f"   • {post.title} ({status})")
    
    # Find comments on first post
    post_comments = Comment.find(db, {"post_id": post1_id})
    print(f"\n💭 Post '{post1.title}' has {len(post_comments)} comments:")
    for comment in post_comments:
        print(f"   • {comment.author_name}: {comment.content}")
    
    # 4. Show foreign key relationships in action
    print(f"\n4. Relationship Summary:")
    print(f"   👤 Users: {User.count(db)}")
    print(f"   📝 Posts: {Post.count(db)}")  
    print(f"   💬 Comments: {Comment.count(db)}")
    print(f"   📈 Published Posts: {Post.count(db, {'published': True})}")
    
    print(f"\n🎉 Success! Foreign keys work seamlessly with Django-like syntax!")

if __name__ == "__main__":
    main()
    db.close()

# 🔥 Key Benefits of Django-like Foreign Keys in Akron:
#
# ✅ Simple Syntax: Just add __foreign_keys__ = {'field': 'table.column'}
# ✅ Familiar: Django developers feel at home
# ✅ Clean: No complex decorators or field definitions needed
# ✅ Type-Safe: Full Pydantic validation and type hints
# ✅ Universal: Works with SQLite, MySQL, PostgreSQL, MongoDB
# ✅ Intuitive: Relationships are clearly visible in model definition