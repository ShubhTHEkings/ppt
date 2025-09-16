#!/usr/bin/env python3
"""
FarnDB Example Usage
Demonstrates basic operations with FarnDB
"""

import farndb

def main():
    print("🗄️  FarnDB Example Usage")
    print("=" * 40)
    
    # Initialize database
    db = farndb.FarnDB("example.json")
    
    # Create some sample data
    print("\n1. Inserting sample users...")
    users = [
        {"name": "Alice", "age": 30, "email": "alice@example.com"},
        {"name": "Bob", "age": 25, "email": "bob@example.com"},
        {"name": "Charlie", "age": 35, "email": "charlie@example.com"}
    ]
    
    user_ids = []
    for user in users:
        user_id = db.insert("users", user)
        user_ids.append(user_id)
        print(f"   Added user: {user['name']} (ID: {user_id})")
    
    # Find all users
    print("\n2. Finding all users...")
    all_users = db.find("users")
    for user in all_users:
        print(f"   {user['name']} ({user['age']}) - {user['email']}")
    
    # Find specific user
    print("\n3. Finding user named 'Alice'...")
    alice = db.find_one("users", {"name": "Alice"})
    if alice:
        print(f"   Found: {alice['name']} - {alice['email']}")
    
    # Update user
    print("\n4. Updating Alice's age...")
    updated = db.update("users", {"name": "Alice"}, {"age": 31})
    print(f"   Updated {updated} user(s)")
    
    # Verify update
    alice_updated = db.find_one("users", {"name": "Alice"})
    if alice_updated:
        print(f"   Alice's new age: {alice_updated['age']}")
    
    # Insert some posts
    print("\n5. Adding posts...")
    posts = [
        {"title": "Hello World", "author": "Alice", "content": "This is my first post!"},
        {"title": "FarnDB Tutorial", "author": "Bob", "content": "How to use FarnDB effectively"},
        {"title": "Database Tips", "author": "Alice", "content": "Some useful database tips"}
    ]
    
    for post in posts:
        post_id = db.insert("posts", post)
        print(f"   Added post: {post['title']} by {post['author']}")
    
    # Find posts by author
    print("\n6. Finding posts by Alice...")
    alice_posts = db.find("posts", {"author": "Alice"})
    for post in alice_posts:
        print(f"   '{post['title']}' - {post['content'][:30]}...")
    
    # Count documents
    print("\n7. Document counts...")
    user_count = db.count("users")
    post_count = db.count("posts")
    print(f"   Users: {user_count}")
    print(f"   Posts: {post_count}")
    
    # List collections
    print("\n8. Collections in database...")
    collections = db.list_collections()
    for collection in collections:
        count = db.count(collection)
        print(f"   {collection}: {count} documents")
    
    # Delete a post
    print("\n9. Deleting 'Hello World' post...")
    deleted = db.delete("posts", {"title": "Hello World"})
    print(f"   Deleted {deleted} post(s)")
    
    # Final counts
    print("\n10. Final counts...")
    for collection in db.list_collections():
        count = db.count(collection)
        print(f"    {collection}: {count} documents")
    
    print("\n✅ FarnDB example completed!")
    print("📁 Check 'example.json' to see the stored data")

if __name__ == "__main__":
    main()