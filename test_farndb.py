#!/usr/bin/env python3
"""
Simple tests for FarnDB functionality
"""

import os
import tempfile
import farndb


def test_basic_operations():
    """Test basic CRUD operations"""
    print("🧪 Testing basic operations...")
    
    # Create a temporary database
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
        db_path = f.name
    
    try:
        db = farndb.FarnDB(db_path)
        
        # Test insert
        doc_id = db.insert("test", {"name": "Test User", "value": 42})
        assert doc_id is not None
        print("✅ Insert: OK")
        
        # Test find
        docs = db.find("test")
        assert len(docs) == 1
        assert docs[0]["name"] == "Test User"
        print("✅ Find: OK")
        
        # Test find_one
        doc = db.find_one("test", {"name": "Test User"})
        assert doc is not None
        assert doc["value"] == 42
        print("✅ Find One: OK")
        
        # Test update
        updated = db.update("test", {"name": "Test User"}, {"value": 100})
        assert updated == 1
        doc = db.find_one("test", {"name": "Test User"})
        assert doc["value"] == 100
        print("✅ Update: OK")
        
        # Test count
        count = db.count("test")
        assert count == 1
        print("✅ Count: OK")
        
        # Test delete
        deleted = db.delete("test", {"name": "Test User"})
        assert deleted == 1
        count = db.count("test")
        assert count == 0
        print("✅ Delete: OK")
        
        # Test collections
        db.insert("collection1", {"data": "test1"})
        db.insert("collection2", {"data": "test2"})
        collections = db.list_collections()
        assert "test" in collections
        assert "collection1" in collections
        assert "collection2" in collections
        print("✅ Collections: OK")
        
        # Test drop collection
        dropped = db.drop_collection("collection1")
        assert dropped == True
        collections = db.list_collections()
        assert "collection1" not in collections
        print("✅ Drop Collection: OK")
        
    finally:
        # Clean up
        if os.path.exists(db_path):
            os.unlink(db_path)
    
    print("🎉 All basic tests passed!")


def test_persistence():
    """Test data persistence"""
    print("\n🧪 Testing persistence...")
    
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
        db_path = f.name
    
    try:
        # Create database and insert data
        db1 = farndb.FarnDB(db_path)
        db1.insert("users", {"name": "Alice", "age": 30})
        db1.insert("users", {"name": "Bob", "age": 25})
        
        # Create new instance and verify data is loaded
        db2 = farndb.FarnDB(db_path)
        users = db2.find("users")
        assert len(users) == 2
        
        names = [user["name"] for user in users]
        assert "Alice" in names
        assert "Bob" in names
        print("✅ Persistence: OK")
        
    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)
    
    print("🎉 Persistence test passed!")


def test_convenience_functions():
    """Test convenience functions"""
    print("\n🧪 Testing convenience functions...")
    
    # Test with temporary file
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
        db_path = f.name
    
    try:
        # Use convenience functions
        doc_id = farndb.insert("test", {"name": "Convenience Test"})
        assert doc_id is not None
        
        docs = farndb.find("test")
        assert len(docs) == 1
        
        doc = farndb.find_one("test", {"name": "Convenience Test"})
        assert doc is not None
        
        updated = farndb.update("test", {"name": "Convenience Test"}, {"updated": True})
        assert updated == 1
        
        deleted = farndb.delete("test", {"name": "Convenience Test"})
        assert deleted == 1
        
        print("✅ Convenience Functions: OK")
        
    finally:
        # Clean up default database
        if os.path.exists("farndb.json"):
            os.unlink("farndb.json")
        if os.path.exists(db_path):
            os.unlink(db_path)
    
    print("🎉 Convenience functions test passed!")


def main():
    print("🚀 FarnDB Test Suite")
    print("=" * 40)
    
    test_basic_operations()
    test_persistence()
    test_convenience_functions()
    
    print("\n🎊 All tests passed successfully!")
    print("FarnDB is working correctly!")


if __name__ == "__main__":
    main()