"""Enhanced Akron ORM example with Django-like foreign keys and Pydantic models."""

from akron import Akron
from akron.models import ModelMixin
from pydantic import BaseModel
from typing import Optional

# Initialize database connection
db = Akron("sqlite:///enhanced_blog.db")

# Define Pydantic models with Django-like foreign key syntax
class User(BaseModel, ModelMixin):
    id: Optional[int] = None
    name: str
    email: str
    age: int
    active: bool = True

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
    
    # 🔥 Django-like foreign key definitions
    __foreign_keys__ = {
        'author_id': 'users.id',
        'category_id': 'categories.id'
    }

def run_enhanced_example():
    print("🚀 Enhanced Akron ORM Demo with Django-like Foreign Keys")
    print("=" * 60)
    
    # 1. Create tables with foreign key relationships
    print("\n1. 📋 Creating type-safe tables with relationships...")
    User.create_table(db)
    Category.create_table(db) 
    Post.create_table(db)  # Automatically handles foreign keys!
    print("✅ Tables created: users, categories, posts (with foreign keys)")
    
    # 2. Insert data using type-safe Pydantic models
    print("\n2. 👤 Creating users with type validation...")
    
    alice = User(
        name="Alice Johnson",
        email="alice@example.com", 
        age=28,
        active=True
    )
    
    bob = User(
        name="Bob Smith",
        email="bob@example.com",
        age=32, 
        active=True
    )
    
    alice_id = User.insert(db, alice)
    bob_id = User.insert(db, bob)
    print(f"   ✅ Created: Alice (ID: {alice_id}), Bob (ID: {bob_id})")
    
    # 3. Create categories
    print("\n3. 📁 Creating categories...")
    
    tech_category = Category(
        name="Technology",
        slug="technology",
        description="Posts about programming and tech"
    )
    
    tutorial_category = Category(
        name="Tutorials", 
        slug="tutorials",
        description="Step-by-step guides"
    )
    
    tech_id = Category.insert(db, tech_category)
    tutorial_id = Category.insert(db, tutorial_category)
    print(f"   ✅ Created: Technology (ID: {tech_id}), Tutorials (ID: {tutorial_id})")
    
    # 4. Create posts with foreign key relationships
    print("\n4. 📝 Creating posts with foreign key relationships...")
    
    post1 = Post(
        title="Getting Started with Akron ORM",
        content="Akron is a universal Python ORM that supports multiple databases...",
        author_id=alice_id,     # Foreign key to users table
        category_id=tech_id,    # Foreign key to categories table
        published=True,
        views=150
    )
    
    post2 = Post(
        title="Building APIs with Flask and Akron",
        content="Learn how to build REST APIs using Flask and Akron ORM...", 
        author_id=bob_id,       # Foreign key to users table
        category_id=tutorial_id, # Foreign key to categories table
        published=True,
        views=89
    )
    
    post3 = Post(
        title="Advanced Database Techniques", 
        content="Explore advanced features like transactions and indexing...",
        author_id=alice_id,     # Foreign key to users table
        category_id=tech_id,    # Foreign key to categories table
        published=False,        # Draft post
        views=5
    )
    
    Post.insert(db, post1)
    Post.insert(db, post2)
    Post.insert(db, post3)
    print("   ✅ Created 3 posts with author and category relationships")
    
    # 5. Query data with relationships
    print("\n5. 🔍 Querying related data...")
    
    # Find all active users
    active_users = User.find(db, {"active": True})
    print(f"   👥 Active users: {len(active_users)}")
    
    # Find Alice's posts
    alice_posts = Post.find(db, {"author_id": alice_id})
    print(f"   📚 Alice's posts: {len(alice_posts)}")
    for post in alice_posts:
        status = "Published" if post.published else "Draft"
        print(f"      • {post.title} ({status}, {post.views} views)")
    
    # Find posts in Technology category
    tech_posts = Post.find(db, {"category_id": tech_id})
    print(f"   🔧 Technology posts: {len(tech_posts)}")
    
    # Find published posts
    published_posts = Post.find(db, {"published": True})
    print(f"   📈 Published posts: {len(published_posts)}")
    
    # 6. Update operations
    print("\n6. ✏️  Update operations...")
    
    # Update Alice's age
    User.update(db, {"id": alice_id}, {"age": 29})
    print("   ✅ Updated Alice's age to 29")
    
    # Publish Alice's draft post
    Post.update(db, {"author_id": alice_id, "published": False}, {"published": True})
    print("   ✅ Published Alice's draft post")
    
    # 7. Aggregation and counting
    print("\n7. 📊 Statistics and aggregation...")
    
    total_users = User.count(db)
    total_posts = Post.count(db) 
    published_count = Post.count(db, {"published": True})
    tech_post_count = Post.count(db, {"category_id": tech_id})
    
    print(f"   📈 Total users: {total_users}")
    print(f"   📈 Total posts: {total_posts}")
    print(f"   📈 Published posts: {published_count}")
    print(f"   📈 Technology posts: {tech_post_count}")
    
    # 8. Advanced queries with raw SQL (for complex relationships)
    print("\n8. 🔗 Advanced relationship queries...")
    
    # Get user statistics with their post counts
    user_stats = db.raw("""
        SELECT 
            u.name,
            u.email,
            COUNT(p.id) as post_count,
            SUM(CASE WHEN p.published = 1 THEN 1 ELSE 0 END) as published_count,
            COALESCE(SUM(p.views), 0) as total_views
        FROM user u
        LEFT JOIN post p ON u.id = p.author_id
        GROUP BY u.id, u.name, u.email
        ORDER BY total_views DESC
    """)
    
    print("   👤 User Statistics:")
    for stat in user_stats:
        print(f"      • {stat['name']} ({stat['email']}): "
              f"{stat['post_count']} posts, "
              f"{stat['published_count']} published, "
              f"{stat['total_views']} total views")
    
    # 9. Demonstrate existence checking and get_or_create
    print("\n9. 🔍 Existence checking and convenience methods...")
    
    # Check if a user exists
    alice_exists = User.exists(db, {"email": "alice@example.com"})
    print(f"   ✅ Alice exists: {alice_exists}")
    
    # Try to find a specific post
    akron_post = Post.find(db, {"title": "Getting Started with Akron ORM"})
    if akron_post:
        print(f"   📝 Found post: '{akron_post[0].title}' by author ID {akron_post[0].author_id}")
    
    # 10. Final summary
    print("\n10. 📋 Final Summary:")
    print("    🎉 Successfully demonstrated:")
    print("       • Django-like foreign key syntax (__foreign_keys__)")
    print("       • Type-safe Pydantic models with ModelMixin")
    print("       • Automatic foreign key constraint creation")
    print("       • Cross-table relationships and queries")
    print("       • CRUD operations with type validation")
    print("       • Advanced SQL queries for complex relationships")
    
    print(f"\n✨ Database contains:")
    print(f"   👥 {User.count(db)} users")
    print(f"   📁 {Category.count(db)} categories") 
    print(f"   📝 {Post.count(db)} posts")
    print(f"   🔗 All with proper foreign key relationships!")

if __name__ == "__main__":
    run_enhanced_example()
    db.close()
    print(f"\n🎯 Django-like foreign key demo completed successfully!")

# 🔥 Key Features Demonstrated:
#
# ✅ __foreign_keys__ class attribute for clean FK definitions
# ✅ Type-safe Pydantic models with automatic validation  
# ✅ Automatic foreign key constraint creation
# ✅ Cross-table relationship queries
# ✅ Enhanced ModelMixin with find_all, get_by_id, exists methods
# ✅ Raw SQL for complex relationship queries
# ✅ Universal database support (SQLite, MySQL, PostgreSQL, MongoDB)