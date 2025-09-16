#!/usr/bin/env python3
"""
FarnDB CLI - Command Line Interface for FarnDB
Simple command-line tool to interact with FarnDB databases
"""

import argparse
import json
import sys
import farndb
from typing import Dict, Any


def print_table(data, title="Results"):
    """Print data in a simple table format"""
    if not data:
        print(f"No data found.")
        return
    
    print(f"\n📊 {title}")
    print("-" * 50)
    
    if isinstance(data, list):
        for i, item in enumerate(data, 1):
            print(f"#{i}: {json.dumps(item, indent=2)}")
    else:
        print(json.dumps(data, indent=2))


def main():
    parser = argparse.ArgumentParser(description="FarnDB CLI - Lightweight JSON Database Tool")
    parser.add_argument("--db", default="farndb.json", help="Database file path")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Insert command
    insert_parser = subparsers.add_parser("insert", help="Insert a document")
    insert_parser.add_argument("collection", help="Collection name")
    insert_parser.add_argument("data", help="JSON data to insert")
    
    # Find command
    find_parser = subparsers.add_parser("find", help="Find documents")
    find_parser.add_argument("collection", help="Collection name")
    find_parser.add_argument("--query", help="JSON query (optional)")
    find_parser.add_argument("--limit", type=int, help="Limit results")
    
    # Update command
    update_parser = subparsers.add_parser("update", help="Update documents")
    update_parser.add_argument("collection", help="Collection name")
    update_parser.add_argument("query", help="JSON query to match documents")
    update_parser.add_argument("data", help="JSON data to update")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete documents")
    delete_parser.add_argument("collection", help="Collection name")
    delete_parser.add_argument("query", help="JSON query to match documents")
    
    # Count command
    count_parser = subparsers.add_parser("count", help="Count documents")
    count_parser.add_argument("collection", help="Collection name")
    count_parser.add_argument("--query", help="JSON query (optional)")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List collections")
    
    # Drop command
    drop_parser = subparsers.add_parser("drop", help="Drop a collection")
    drop_parser.add_argument("collection", help="Collection name")
    
    # Backup command
    backup_parser = subparsers.add_parser("backup", help="Backup database")
    backup_parser.add_argument("path", help="Backup file path")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        db = farndb.FarnDB(args.db)
        
        if args.command == "insert":
            try:
                data = json.loads(args.data)
                doc_id = db.insert(args.collection, data)
                print(f"✅ Inserted document with ID: {doc_id}")
            except json.JSONDecodeError:
                print("❌ Error: Invalid JSON data")
                sys.exit(1)
        
        elif args.command == "find":
            query = {}
            if args.query:
                try:
                    query = json.loads(args.query)
                except json.JSONDecodeError:
                    print("❌ Error: Invalid JSON query")
                    sys.exit(1)
            
            results = db.find(args.collection, query)
            if args.limit:
                results = results[:args.limit]
            
            print_table(results, f"Documents in '{args.collection}'")
            print(f"\n📈 Total: {len(results)} document(s)")
        
        elif args.command == "update":
            try:
                query = json.loads(args.query)
                data = json.loads(args.data)
                count = db.update(args.collection, query, data)
                print(f"✅ Updated {count} document(s)")
            except json.JSONDecodeError:
                print("❌ Error: Invalid JSON data")
                sys.exit(1)
        
        elif args.command == "delete":
            try:
                query = json.loads(args.query)
                count = db.delete(args.collection, query)
                print(f"✅ Deleted {count} document(s)")
            except json.JSONDecodeError:
                print("❌ Error: Invalid JSON query")
                sys.exit(1)
        
        elif args.command == "count":
            query = {}
            if args.query:
                try:
                    query = json.loads(args.query)
                except json.JSONDecodeError:
                    print("❌ Error: Invalid JSON query")
                    sys.exit(1)
            
            count = db.count(args.collection, query)
            print(f"📊 Count: {count} document(s) in '{args.collection}'")
        
        elif args.command == "list":
            collections = db.list_collections()
            if collections:
                print("\n📁 Collections:")
                for collection in collections:
                    count = db.count(collection)
                    print(f"   {collection}: {count} document(s)")
            else:
                print("📁 No collections found")
        
        elif args.command == "drop":
            if db.drop_collection(args.collection):
                print(f"✅ Dropped collection '{args.collection}'")
            else:
                print(f"❌ Collection '{args.collection}' not found")
        
        elif args.command == "backup":
            if db.backup(args.path):
                print(f"✅ Backup created: {args.path}")
            else:
                print(f"❌ Backup failed")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()