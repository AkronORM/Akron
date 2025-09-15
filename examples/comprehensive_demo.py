"""
Comprehensive example demonstrating all Akron ORM features.
"""

from akron import Akron

def demonstrate_akron_features():
    # Initialize database
    db = Akron("sqlite:///demo.db")
    
    print("🚀 Akron ORM Feature Demonstration\n")
    
    # ===== TABLE CREATION =====
    print("1. Creating tables with relationships...")
    
    # Users table
    db.create_table("users", {
        "id": "int",
        "name": "str",
        "email": "str",
        "age": "int",
        "active": "bool",
        "created_at": "str"
    })
    
    # Posts table with foreign key
    db.create_table("posts", {
        "id": "int",
        "title": "str",
        "content": "str",
        "user_id": "int->users.id",  # Foreign key syntax
        "views": "int",
        "published": "bool"
    })
    
    # Orders table for aggregation examples
    db.create_table("orders", {
        "id": "int",
        "user_id": "int->users.id",
        "amount": "float",
        "status": "str",
        "created_at": "str"
    })
    
    print("✅ Tables created with relationships\n")
    
    # ===== BASIC CRUD OPERATIONS =====
    print("2. Basic CRUD Operations...")
    
    # Single insert
    user1_id = db.insert("users", {
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "age": 28,
        "active": True,
        "created_at": "2024-01-15"
    })
    print(f"Inserted user with ID: {user1_id}")
    
    # Bulk insert
    user_ids = db.bulk_insert("users", [
        {"name": "Bob Smith", "email": "bob@example.com", "age": 32, "active": True, "created_at": "2024-01-16"},
        {"name": "Carol Davis", "email": "carol@example.com", "age": 25, "active": False, "created_at": "2024-01-17"},
        {"name": "David Wilson", "email": "david@example.com", "age": 45, "active": True, "created_at": "2024-01-18"}
    ])
    print(f"Bulk inserted users with IDs: {user_ids}")
    
    # Find records
    active_users = db.find("users", {"active": True})
    print(f"Found {len(active_users)} active users")
    
    # Find one record
    alice = db.find_one("users", {"name": "Alice Johnson"})
    print(f"Found user: {alice['name']} ({alice['email']})")
    
    # Update records
    updated_count = db.update("users", {"name": "Alice Johnson"}, {"age": 29})
    print(f"Updated {updated_count} records")
    
    print("✅ Basic CRUD completed\n")
    
    # ===== ADVANCED QUERYING =====
    print("3. Advanced Query Features...")
    
    # Insert some posts for demonstration
    db.bulk_insert("posts", [
        {"title": "Getting Started with Python", "content": "Python basics...", "user_id": user1_id, "views": 150, "published": True},
        {"title": "Advanced SQL Techniques", "content": "SQL tips...", "user_id": user_ids[0], "views": 230, "published": True},
        {"title": "Draft Post", "content": "Work in progress...", "user_id": user1_id, "views": 5, "published": False},
        {"title": "Machine Learning Guide", "content": "ML fundamentals...", "user_id": user_ids[1], "views": 890, "published": True}
    ])
    
    # Advanced filtering with QueryBuilder
    popular_posts = db.query("posts").where(
        views__gt=100,
        published=True
    ).order_by("-views").limit(3).all()
    
    print(f"Popular posts (views > 100):")
    for post in popular_posts:
        print(f"  - {post['title']}: {post['views']} views")
    
    # Pagination
    page1_users = db.query("users").order_by("name").paginate(page=1, per_page=2).all()
    print(f"Page 1 users: {[u['name'] for u in page1_users]}")
    
    # Complex filtering
    young_active_users = db.query("users").where(
        age__lt=30,
        active=True
    ).order_by("age").all()
    young_users_display = [f"{u['name']} ({u['age']})" for u in young_active_users]
    print(f"Young active users: {young_users_display}")
    
    print("✅ Advanced querying completed\n")
    
    # ===== AGGREGATIONS =====
    print("4. Aggregation Functions...")
    
    # Insert some orders
    db.bulk_insert("orders", [
        {"user_id": user1_id, "amount": 99.99, "status": "completed", "created_at": "2024-01-20"},
        {"user_id": user1_id, "amount": 149.50, "status": "completed", "created_at": "2024-01-21"},
        {"user_id": user_ids[0], "amount": 75.25, "status": "completed", "created_at": "2024-01-22"},
        {"user_id": user_ids[1], "amount": 200.00, "status": "pending", "created_at": "2024-01-23"}
    ])
    
    # Simple aggregations
    total_users = db.count("users")
    active_users_count = db.count("users", {"active": True})
    print(f"Total users: {total_users}, Active: {active_users_count}")
    
    # Complex aggregations
    user_stats = db.aggregate("orders", 
                             {"total_amount": "sum", "order_count": "count"}, 
                             filters={"status": "completed"},
                             group_by=["user_id"])
    
    print("Order statistics by user:")
    for stat in user_stats:
        print(f"  User {stat['user_id']}: {stat['order_count']} orders, ${stat['total_amount']:.2f} total")
    
    print("✅ Aggregations completed\n")
    
    # ===== TRANSACTIONS =====
    print("5. Transaction Management...")
    
    try:
        with db.transaction():
            # Create a new user and their first post atomically
            new_user_id = db.insert("users", {
                "name": "Emma Thompson",
                "email": "emma@example.com", 
                "age": 27,
                "active": True,
                "created_at": "2024-01-25"
            })
            
            db.insert("posts", {
                "title": "My First Post",
                "content": "Hello, world!",
                "user_id": new_user_id,
                "views": 1,
                "published": True
            })
            
            print(f"✅ Transaction completed: Created user {new_user_id} with first post")
            
    except Exception as e:
        print(f"❌ Transaction failed: {e}")
    
    # ===== INDEXES =====
    print("6. Index Management...")
    
    # Create indexes for better performance
    db.create_index("users", "email", unique=True)
    db.create_index("posts", ["user_id", "published"])
    db.create_index("orders", "created_at")
    
    print("✅ Indexes created for better query performance\n")
    
    # ===== RAW SQL =====
    print("7. Raw SQL Execution...")
    
    # Complex query with raw SQL
    user_post_stats = db.raw("""
        SELECT u.name, u.email, 
               COUNT(p.id) as post_count,
               AVG(p.views) as avg_views
        FROM users u
        LEFT JOIN posts p ON u.id = p.user_id
        WHERE u.active = 1
        GROUP BY u.id, u.name, u.email
        ORDER BY post_count DESC
    """)
    
    print("User post statistics:")
    for stat in user_post_stats:
        avg_views = stat['avg_views'] or 0
        print(f"  {stat['name']}: {stat['post_count']} posts, {avg_views:.1f} avg views")
    
    print("✅ Raw SQL executed\n")
    
    # ===== CONVENIENCE METHODS =====
    print("8. Convenience Methods...")
    
    # Check existence
    has_admin = db.exists("users", {"email": "admin@example.com"})
    print(f"Admin user exists: {has_admin}")
    
    # Get or create
    admin_user, created = db.get_or_create(
        "users",
        {"email": "admin@example.com"},
        {"name": "Administrator", "age": 35, "active": True, "created_at": "2024-01-26"}
    )
    print(f"Admin user {'created' if created else 'found'}: {admin_user['name']}")
    
    # Upsert (update or insert)
    updated_admin = db.upsert(
        "users",
        {"email": "admin@example.com"},
        {"name": "System Administrator", "age": 36}
    )
    print(f"Upserted admin: {updated_admin['name']} (age {updated_admin['age']})")
    
    print("✅ Convenience methods demonstrated\n")
    
    # ===== SERIALIZATION =====
    print("9. Data Serialization...")
    
    # Get some data
    sample_users = db.query("users").limit(2).all()
    
    # Convert to JSON
    json_data = db.to_json(sample_users)
    print(f"Sample users as JSON: {json_data[:100]}...")
    
    print("✅ Serialization completed\n")
    
    # ===== CLEANUP =====
    print("10. Cleanup and Summary...")
    
    final_stats = {
        "total_users": db.count("users"),
        "total_posts": db.count("posts"),
        "total_orders": db.count("orders"),
        "published_posts": db.count("posts", {"published": True})
    }
    
    print("Final database statistics:")
    for key, value in final_stats.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    
    # Close connection
    db.close()
    print("\n🎉 Akron ORM demonstration completed successfully!")


if __name__ == "__main__":
    demonstrate_akron_features()
