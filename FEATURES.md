# Akron ORM - Complete Feature Guide

## Overview
Akron is a universal Python ORM that provides a simple, intuitive interface for database operations across SQLite, MySQL, PostgreSQL, and MongoDB. This guide covers all available features with practical examples.

## Table of Contents
- [Basic CRUD Operations](#basic-crud-operations)
- [Advanced Querying](#advanced-querying)
- [Filtering & Operators](#filtering--operators)
- [Sorting & Pagination](#sorting--pagination)
- [Joins & Relationships](#joins--relationships)
- [Aggregations](#aggregations)
- [Transactions](#transactions)
- [Bulk Operations](#bulk-operations)
- [Constraints & Validation](#constraints--validation)
- [Indexes](#indexes)
- [Raw SQL](#raw-sql)
- [Convenience Methods](#convenience-methods)
- [Serialization](#serialization)

## Basic CRUD Operations

### Create Tables
```python
from akron import Akron

db = Akron("sqlite:///myapp.db")

# Simple table
db.create_table("users", {
    "id": "int",
    "name": "str",
    "email": "str",
    "age": "int",
    "active": "bool"
})

# Table with foreign keys
db.create_table("posts", {
    "id": "int",
    "title": "str",
    "content": "str",
    "user_id": "int->users.id",  # Foreign key syntax
    "published": "bool"
})
```

### Insert Records
```python
# Single insert
user_id = db.insert("users", {
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "active": True
})

# Bulk insert
user_ids = db.bulk_insert("users", [
    {"name": "Alice", "email": "alice@example.com", "age": 25, "active": True},
    {"name": "Bob", "email": "bob@example.com", "age": 35, "active": False}
])
```

### Read Records
```python
# Find all
all_users = db.find("users")

# Find with filters
active_users = db.find("users", {"active": True})

# Find one record
john = db.find_one("users", {"name": "John Doe"})
```

### Update Records
```python
# Update matching records
updated_count = db.update("users", {"name": "John Doe"}, {"age": 31})

# Bulk update
db.bulk_update("users", [
    {"filters": {"id": 1}, "values": {"age": 32}},
    {"filters": {"id": 2}, "values": {"active": True}}
])
```

### Delete Records
```python
# Delete matching records
deleted_count = db.delete("users", {"active": False})
```

## Advanced Querying

### QueryBuilder Interface
```python
# Use the fluent QueryBuilder for complex queries
users = db.query("users").where(
    age__gte=18,
    active=True
).order_by("-created_at").limit(10).all()

# Get first result
youngest_user = db.query("users").order_by("age").first()

# Count results
adult_count = db.query("users").where(age__gte=18).count()
```

## Filtering & Operators

### Comparison Operators
```python
# Greater than
adults = db.query("users").where(age__gt=17).all()

# Less than or equal
young_users = db.query("users").where(age__lte=25).all()

# Not equal
active_users = db.query("users").where(status__ne="inactive").all()

# IN operator
specific_users = db.query("users").where(id__in=[1, 2, 3]).all()

# LIKE operator
johns = db.query("users").where(name__like="%john%").all()

# NULL checks
users_without_email = db.query("users").where(email__isnull=True).all()
```

### Multiple Conditions
```python
# All conditions must match (AND)
filtered_users = db.query("users").where(
    age__gte=18,
    age__lte=65,
    active=True,
    name__like="%smith%"
).all()
```

## Sorting & Pagination

### Sorting
```python
# Single field ascending
users = db.query("users").order_by("name").all()

# Single field descending (use minus prefix)
users = db.query("users").order_by("-age").all()

# Multiple fields
users = db.query("users").order_by("-age", "name").all()
```

### Pagination
```python
# Using limit and offset
page1 = db.query("users").limit(10).offset(0).all()
page2 = db.query("users").limit(10).offset(10).all()

# Using pagination helper
page1 = db.query("users").paginate(page=1, per_page=10).all()
page2 = db.query("users").paginate(page=2, per_page=10).all()
```

## Joins & Relationships

### Foreign Key Relationships
```python
# Define relationships in table schema
db.create_table("posts", {
    "id": "int",
    "title": "str",
    "user_id": "int->users.id"  # Foreign key to users.id
})

# Query with joins using raw SQL
user_posts = db.raw("""
    SELECT u.name, p.title, p.created_at
    FROM users u
    JOIN posts p ON u.id = p.user_id
    WHERE u.active = 1
    ORDER BY p.created_at DESC
""")
```

### QueryBuilder Joins
```python
# Add joins to QueryBuilder (basic implementation)
posts_with_users = db.query("posts").join(
    "users",
    "posts.user_id = users.id"
).select("posts.title", "users.name").all()
```

## Aggregations

### Simple Counting
```python
# Count all records
total_users = db.count("users")

# Count with filters
active_users = db.count("users", {"active": True})

# Count with QueryBuilder
young_adults = db.query("users").where(age__gte=18, age__lt=30).count()
```

### Group By Aggregations
```python
# Aggregate functions
stats = db.aggregate("orders", {
    "total_amount": "sum",
    "order_count": "count", 
    "avg_amount": "avg"
}, group_by=["user_id"])

# With filters
completed_stats = db.aggregate("orders", {
    "total": "sum",
    "count": "count"
}, filters={"status": "completed"}, group_by=["user_id"])
```

## Transactions

### Automatic Transaction Management
```python
# Context manager (recommended)
with db.transaction():
    user_id = db.insert("users", {"name": "Alice", "email": "alice@example.com"})
    db.insert("posts", {"title": "Hello World", "user_id": user_id})
    # Automatically commits on success, rolls back on error
```

### Manual Transaction Control
```python
# Manual control
db.begin_transaction()
try:
    user_id = db.insert("users", {"name": "Bob"})
    db.insert("posts", {"title": "Bob's Post", "user_id": user_id})
    db.commit()
except Exception:
    db.rollback()
    raise
```

## Bulk Operations

### Bulk Insert
```python
# Insert many records efficiently
users = [
    {"name": f"User {i}", "email": f"user{i}@example.com", "age": 20 + i}
    for i in range(100)
]
user_ids = db.bulk_insert("users", users)
```

### Bulk Update
```python
# Update multiple records with different values
updates = [
    {"filters": {"id": 1}, "values": {"age": 25}},
    {"filters": {"id": 2}, "values": {"age": 30}},
    {"filters": {"id": 3}, "values": {"active": False}}
]
updated_count = db.bulk_update("users", updates)
```

## Constraints & Validation

### Database Constraints
```python
# Foreign key constraints are enforced
db.create_table("posts", {
    "id": "int",
    "user_id": "int->users.id"  # Must reference existing user
})

# Unique constraints via indexes
db.create_index("users", "email", unique=True)
```

### Application-Level Validation
```python
# Check constraints before operations
if not db.exists("users", {"id": user_id}):
    raise ValueError("User does not exist")

# Validate with get_or_create
user, created = db.get_or_create("users", 
    {"email": "new@example.com"},
    defaults={"name": "New User", "age": 25}
)
```

## Indexes

### Create Indexes
```python
# Single column index
db.create_index("users", "email", unique=True)

# Multi-column index  
db.create_index("posts", ["user_id", "published"])

# Index on multiple single columns
db.create_index("orders", "created_at")
db.create_index("orders", "status")
```

### Drop Indexes
```python
db.drop_index("idx_users_email")
```

## Raw SQL

### Execute Custom Queries
```python
# SELECT queries
results = db.raw("SELECT * FROM users WHERE age > ?", (25,))

# Complex joins and aggregations
user_stats = db.raw("""
    SELECT 
        u.name,
        COUNT(p.id) as post_count,
        AVG(p.views) as avg_views
    FROM users u
    LEFT JOIN posts p ON u.id = p.user_id
    GROUP BY u.id, u.name
    ORDER BY post_count DESC
""")

# INSERT/UPDATE/DELETE operations
db.raw("UPDATE users SET last_login = ? WHERE id = ?", (datetime.now(), user_id))
```

## Convenience Methods

### Existence Checks
```python
# Check if records exist
has_admin = db.exists("users", {"role": "admin"})

if db.exists("users", {"email": email}):
    print("Email already registered")
```

### Get or Create
```python
# Get existing or create new
user, created = db.get_or_create("users",
    {"email": "admin@example.com"},
    defaults={"name": "Administrator", "role": "admin"}
)

if created:
    print("New admin user created")
else:
    print("Admin user already exists")
```

### Upsert (Update or Insert)
```python
# Update existing or insert new
user = db.upsert("users",
    {"email": "john@example.com"},
    {"name": "John Smith", "age": 30, "active": True}
)
```

## Serialization

### Convert to JSON
```python
# Convert query results to JSON
users = db.find("users", {"active": True})
users_json = db.to_json(users)

# Single record
user = db.find_one("users", {"id": 1})
user_json = db.to_json(user)
```

### Dictionary Conversion
```python
# Already returns dictionaries, but for consistency
users_dict = db.to_dict(users)
```

## Error Handling

### Built-in Error Types
```python
from akron.exceptions import AkronError, TableNotFoundError

try:
    db.insert("nonexistent_table", {"name": "test"})
except TableNotFoundError:
    print("Table does not exist")
except AkronError as e:
    print(f"Database error: {e}")
```

### Constraint Violations
```python
try:
    # This will fail if email is not unique
    db.insert("users", {"email": "existing@example.com", "name": "Test"})
except AkronError as e:
    if "UNIQUE constraint failed" in str(e):
        print("Email already exists")
```

## Performance Best Practices

### Use Bulk Operations
```python
# Instead of multiple inserts
for user_data in user_list:
    db.insert("users", user_data)  # Slow

# Use bulk insert
db.bulk_insert("users", user_list)  # Fast
```

### Create Appropriate Indexes
```python
# Index frequently queried columns
db.create_index("users", "email", unique=True)
db.create_index("posts", ["user_id", "created_at"])

# Index foreign key columns
db.create_index("posts", "user_id")
```

### Use Transactions for Related Operations
```python
# Group related operations in transactions
with db.transaction():
    user_id = db.insert("users", user_data)
    db.bulk_insert("posts", posts_data)
    db.insert("profiles", profile_data)
```

### Limit Result Sets
```python
# Use pagination for large result sets
recent_posts = db.query("posts").order_by("-created_at").limit(20).all()

# Count before fetching if needed
if db.count("posts") > 1000:
    posts = db.query("posts").limit(100).all()
```

## Database-Specific Features

### SQLite
- File-based storage
- In-memory databases (`:memory:`)
- AUTOINCREMENT primary keys
- Foreign key constraints

### MySQL  
- Connection pooling
- Multiple storage engines
- Advanced indexing options

### PostgreSQL
- Advanced data types
- Full-text search capabilities  
- JSON/JSONB support

### MongoDB
- Document-based storage
- Flexible schema
- Nested objects and arrays

## Complete Example

```python
from akron import Akron

# Initialize database
db = Akron("sqlite:///blog.db")

# Create schema
db.create_table("users", {
    "id": "int",
    "username": "str", 
    "email": "str",
    "created_at": "str"
})

db.create_table("posts", {
    "id": "int",
    "title": "str",
    "content": "str", 
    "user_id": "int->users.id",
    "published": "bool",
    "views": "int",
    "created_at": "str"
})

# Create indexes
db.create_index("users", "email", unique=True)
db.create_index("posts", ["user_id", "published"])

# Insert data with transaction
with db.transaction():
    # Create user
    user_id = db.insert("users", {
        "username": "johndoe",
        "email": "john@example.com", 
        "created_at": "2024-01-15"
    })
    
    # Create user's posts
    db.bulk_insert("posts", [
        {
            "title": "Getting Started",
            "content": "Welcome to my blog...",
            "user_id": user_id,
            "published": True,
            "views": 150,
            "created_at": "2024-01-16"
        },
        {
            "title": "Advanced Tips", 
            "content": "Here are some tips...",
            "user_id": user_id,
            "published": True,
            "views": 89,
            "created_at": "2024-01-17"
        }
    ])

# Query data
popular_posts = db.query("posts").where(
    published=True,
    views__gt=100
).order_by("-views").all()

# Aggregate data
user_stats = db.aggregate("posts", {
    "post_count": "count",
    "total_views": "sum"
}, filters={"published": True}, group_by=["user_id"])

# Raw SQL for complex queries
top_authors = db.raw("""
    SELECT u.username, COUNT(p.id) as posts, SUM(p.views) as total_views
    FROM users u
    JOIN posts p ON u.id = p.user_id  
    WHERE p.published = 1
    GROUP BY u.id
    ORDER BY total_views DESC
    LIMIT 10
""")

# Close connection
db.close()
```

This comprehensive feature set makes Akron ORM suitable for both simple scripts and complex applications, providing intuitive syntax while maintaining powerful capabilities across different database systems.
