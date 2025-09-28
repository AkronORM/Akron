"""Django-like Foreign Key Example with Pydantic Models."""

from pydantic import BaseModel
from akron import Akron
from akron.models import ModelMixin
from typing import Optional
from datetime import datetime

# Database connection
db = Akron("sqlite:///blog_django_style.db")

# Define Models with Django-like Foreign Key Syntax
class User(BaseModel, ModelMixin):
    id: Optional[int] = None
    username: str
    email: str
    full_name: str
    bio: Optional[str] = None
    created_at: Optional[str] = None
    is_active: bool = True

class Category(BaseModel, ModelMixin):
    id: Optional[int] = None
    name: str
    slug: str
    description: Optional[str] = None

class Post(BaseModel, ModelMixin):
    id: Optional[int] = None
    title: str
    content: str
    author_id: int
    category_id: Optional[int] = None
    published: bool = False
    views: int = 0
    created_at: Optional[str] = None
    
    # Django-like foreign key definitions - Simple and clean!
    __foreign_keys__ = {
        'author_id': 'users.id',
        'category_id': 'categories.id'
    }

class Comment(BaseModel, ModelMixin):
    id: Optional[int] = None
    post_id: int
    author_name: str
    author_email: str
    content: str
    approved: bool = False
    created_at: Optional[str] = None
    
    # Single foreign key
    __foreign_keys__ = {
        'post_id': 'posts.id'
    }

def demonstrate_django_like_fks():
    print("🚀 Django-like Foreign Keys with Akron ORM")
    print("=" * 50)
    
    # Create tables in correct order (dependencies first)
    print("\n1. Creating tables with foreign key relationships...")
    
    User.create_table(db)
    print("✅ Created 'users' table")
    
    Category.create_table(db)
    print("✅ Created 'categories' table")
    
    Post.create_table(db)  # References users and categories
    print("✅ Created 'posts' table with foreign keys:")
    print("   - author_id -> users.id")
    print("   - category_id -> categories.id")
    
    Comment.create_table(db)  # References posts
    print("✅ Created 'comments' table with foreign key:")
    print("   - post_id -> posts.id")
    
    # Insert data with relationships
    print("\n2. Inserting related data...")
    
    # Create users
    user1 = User(
        username="alice_dev",
        email="alice@example.com",
        full_name="Alice Johnson",
        bio="Full-stack developer and tech blogger",
        created_at=datetime.now().isoformat(),
        is_active=True
    )
    
    user2 = User(
        username="bob_writer",
        email="bob@example.com", 
        full_name="Bob Smith",
        bio="Technical writer and Python enthusiast",
        created_at=datetime.now().isoformat(),
        is_active=True
    )
    
    user1_id = User.insert(db, user1)
    user2_id = User.insert(db, user2)
    print(f"✅ Created users: Alice (ID: {user1_id}), Bob (ID: {user2_id})")
    
    # Create categories
    tech_category = Category(
        name="Technology",
        slug="technology", 
        description="Posts about programming and tech trends"
    )
    
    tutorial_category = Category(
        name="Tutorials",
        slug="tutorials",
        description="Step-by-step guides and tutorials"
    )
    
    tech_cat_id = Category.insert(db, tech_category)
    tutorial_cat_id = Category.insert(db, tutorial_category)
    print(f"✅ Created categories: Technology (ID: {tech_cat_id}), Tutorials (ID: {tutorial_cat_id})")
    
    # Create posts with foreign key relationships
    post1 = Post(
        title="Getting Started with Akron ORM",
        content="Akron ORM makes database operations simple and intuitive...",
        author_id=user1_id,  # References Alice
        category_id=tech_cat_id,  # References Technology category
        published=True,
        views=150,
        created_at=datetime.now().isoformat()
    )
    
    post2 = Post(
        title="Building a Flask Blog with Akron",
        content="In this tutorial, we'll build a complete blog application...",
        author_id=user2_id,  # References Bob
        category_id=tutorial_cat_id,  # References Tutorials category  
        published=True,
        views=89,
        created_at=datetime.now().isoformat()
    )
    
    post3 = Post(
        title="Draft: Advanced Akron Features",
        content="This post covers advanced features like transactions...",
        author_id=user1_id,  # References Alice
        category_id=tech_cat_id,  # References Technology category
        published=False,
        views=5,
        created_at=datetime.now().isoformat()
    )
    
    post1_id = Post.insert(db, post1)
    post2_id = Post.insert(db, post2) 
    post3_id = Post.insert(db, post3)
    print(f"✅ Created posts: {post1_id}, {post2_id}, {post3_id}")
    
    # Create comments with foreign key to posts
    comment1 = Comment(
        post_id=post1_id,  # References first post
        author_name="Charlie Reader",
        author_email="charlie@example.com",
        content="Great introduction to Akron! Very helpful.",
        approved=True,
        created_at=datetime.now().isoformat()
    )
    
    comment2 = Comment(
        post_id=post2_id,  # References second post
        author_name="Diana Coder", 
        author_email="diana@example.com",
        content="Looking forward to trying this tutorial. Thanks!",
        approved=True,
        created_at=datetime.now().isoformat()
    )
    
    Comment.insert(db, comment1)
    Comment.insert(db, comment2)
    print("✅ Created comments with post references")
    
    # Query related data
    print("\n3. Querying related data...")
    
    # Find Alice's posts
    alice_posts = Post.find(db, {"author_id": user1_id})
    print(f"📝 Alice has {len(alice_posts)} posts:")
    for post in alice_posts:
        status = "Published" if post.published else "Draft"
        print(f"   - {post.title} ({status}, {post.views} views)")
    
    # Find posts in Technology category
    tech_posts = Post.find(db, {"category_id": tech_cat_id})
    print(f"🔧 Technology category has {len(tech_posts)} posts")
    
    # Find comments on first post
    post1_comments = Comment.find(db, {"post_id": post1_id})
    print(f"💬 Post '{post1.title}' has {len(post1_comments)} comments:")
    for comment in post1_comments:
        print(f"   - {comment.author_name}: {comment.content[:50]}...")
    
    # Demonstrate constraint checking
    print("\n4. Testing foreign key constraints...")
    
    try:
        # This should work - valid user_id
        valid_post = Post(
            title="Valid Post",
            content="This post has a valid author_id",
            author_id=user1_id,  # Valid reference
            category_id=tech_cat_id,  # Valid reference
            published=True
        )
        Post.insert(db, valid_post)
        print("✅ Post with valid foreign keys inserted successfully")
        
    except Exception as e:
        print(f"❌ Error inserting post: {e}")
    
    try:
        # This might fail with foreign key constraint (depends on DB settings)
        invalid_post = Post(
            title="Invalid Post", 
            content="This post has invalid author_id",
            author_id=99999,  # Non-existent user
            category_id=tech_cat_id,
            published=True
        )
        Post.insert(db, invalid_post)
        print("⚠️  Post with invalid foreign key inserted (constraint not enforced)")
        
    except Exception as e:
        print(f"✅ Foreign key constraint prevented invalid insert: {e}")
    
    # Show final statistics
    print("\n5. Final Statistics:")
    print(f"   👥 Users: {User.count(db)}")
    print(f"   📁 Categories: {Category.count(db)}")
    print(f"   📝 Posts: {Post.count(db)}")
    print(f"   💬 Comments: {Comment.count(db)}")
    print(f"   📈 Published Posts: {Post.count(db, {'published': True})}")
    
    # Demonstrate advanced querying with foreign keys
    print("\n6. Advanced Queries with Relationships:")
    
    # First, let's check what tables were created
    tables_check = db.raw("SELECT name FROM sqlite_master WHERE type='table'")
    print("📋 Available tables:", [t['name'] for t in tables_check])
    
    # Using raw SQL for joins (ModelMixin creates lowercase table names)
    user_post_stats = db.raw("""
        SELECT 
            u.full_name,
            u.username,
            COUNT(p.id) as post_count,
            COALESCE(SUM(p.views), 0) as total_views,
            COALESCE(AVG(p.views), 0) as avg_views
        FROM user u
        LEFT JOIN post p ON u.id = p.author_id AND p.published = 1
        GROUP BY u.id, u.full_name, u.username
        ORDER BY total_views DESC
    """)
    
    print("📊 User Statistics:")
    for stat in user_post_stats:
        total_views = stat.get('total_views') or 0
        avg_views = stat.get('avg_views') or 0
        print(f"   {stat['full_name']} (@{stat['username']}): "
              f"{stat['post_count']} posts, {total_views} total views, "
              f"{avg_views:.1f} avg views")
    
    # Category post counts
    category_stats = db.raw("""
        SELECT 
            c.name,
            c.description,
            COALESCE(COUNT(p.id), 0) as post_count
        FROM category c
        LEFT JOIN post p ON c.id = p.category_id AND p.published = 1
        GROUP BY c.id, c.name, c.description
        ORDER BY post_count DESC
    """)
    
    print("\n📂 Category Statistics:")
    for stat in category_stats:
        print(f"   {stat['name']}: {stat['post_count']} posts")
        print(f"     {stat['description']}")
    
    print(f"\n🎉 Django-like foreign key demonstration completed!")
    print("✨ Benefits of this approach:")
    print("   • Simple class-level foreign key definitions")
    print("   • Clean, readable model declarations")  
    print("   • Familiar Django-like syntax")
    print("   • Type-safe with Pydantic validation")
    print("   • Works across all Akron-supported databases")

if __name__ == "__main__":
    demonstrate_django_like_fks()
    db.close()