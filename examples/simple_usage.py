"""
Simple Akron ORM Usage Guide - Easy Syntax Examples
"""

from akron import Akron

# Initialize database connection
db = Akron("sqlite:///myapp.db")

# ===== SIMPLE TABLE CREATION =====
db.create_table("users", {
    "id": "int",
    "name": "str", 
    "email": "str",
    "age": "int",
    "active": "bool"
})

# Create table with foreign keys
db.create_table("posts", {
    "id": "int",
    "title": "str",
    "content": "str",
    "user_id": "int->users.id",  # Foreign key to users table
    "published": "bool"
})

# ===== BASIC OPERATIONS =====

# Insert single record
user_id = db.insert("users", {
    "name": "John Doe",
    "email": "john@example.com", 
    "age": 30,
    "active": True
})

# Insert multiple records at once
user_ids = db.bulk_insert("users", [
    {"name": "Alice", "email": "alice@example.com", "age": 25, "active": True},
    {"name": "Bob", "email": "bob@example.com", "age": 35, "active": False}
])

# Find all records
all_users = db.find("users")

# Find with filters  
active_users = db.find("users", {"active": True})

# Find one record
john = db.find_one("users", {"name": "John Doe"})

# Update records
db.update("users", {"name": "John Doe"}, {"age": 31})

# Delete records
db.delete("users", {"active": False})

# Count records
total_users = db.count("users")
young_users = db.count("users", {"age__lt": 30})

# ===== ADVANCED QUERIES =====

# Filter with operators
adults = db.query("users").where(
    age__gte=18,           # age >= 18
    name__like="%john%"    # name contains "john"
).all()

# Sorting and pagination
users_page1 = db.query("users").order_by("-age", "name").paginate(page=1, per_page=10).all()

# Get first matching record
youngest_user = db.query("users").order_by("age").first()

# Complex filtering
power_users = db.query("posts").where(
    published=True,
    views__gt=1000
).order_by("-views").limit(5).all()

# ===== AGGREGATION =====

# Simple count
post_count = db.query("posts").where(published=True).count()

# Group by aggregations
stats_by_user = db.aggregate("posts", 
    {"post_count": "count", "avg_views": "avg"}, 
    group_by=["user_id"]
)

# ===== TRANSACTIONS =====

# Automatic transaction management
with db.transaction():
    user_id = db.insert("users", {"name": "Alice", "email": "alice@example.com"})
    db.insert("posts", {"title": "Hello World", "user_id": user_id, "published": True})
    # If any operation fails, everything rolls back automatically

# ===== CONVENIENCE METHODS =====

# Check if record exists
has_admin = db.exists("users", {"email": "admin@example.com"})

# Get existing or create new
admin, created = db.get_or_create(
    "users",
    {"email": "admin@example.com"},
    defaults={"name": "Administrator", "age": 35, "active": True}
)

# Update existing or insert new
updated_user = db.upsert("users", 
    {"email": "john@example.com"}, 
    {"name": "John Smith", "age": 32}
)

# ===== RAW SQL FOR COMPLEX QUERIES =====

# Execute raw SQL when needed
results = db.raw("""
    SELECT u.name, COUNT(p.id) as post_count
    FROM users u
    LEFT JOIN posts p ON u.id = p.user_id  
    GROUP BY u.id, u.name
    ORDER BY post_count DESC
""")

# ===== INDEXING FOR PERFORMANCE =====

# Create indexes
db.create_index("users", "email", unique=True)
db.create_index("posts", ["user_id", "published"])

# ===== SERIALIZATION =====

# Convert to JSON
users_json = db.to_json(all_users)

# Close connection when done
db.close()

print("✅ All operations completed successfully!")
