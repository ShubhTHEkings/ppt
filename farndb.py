#!/usr/bin/env python3
"""
FarnDB - A lightweight JSON-based database utility
Simple file-based database for small to medium applications
"""

import json
import os
import time
from typing import Dict, List, Any, Optional
from pathlib import Path


class FarnDB:
    """A simple JSON-based database for lightweight applications"""
    
    def __init__(self, db_path: str = "farndb.json"):
        """
        Initialize FarnDB with a database file path
        
        Args:
            db_path (str): Path to the JSON database file
        """
        self.db_path = Path(db_path)
        self.data = {}
        self._load_data()
    
    def _load_data(self) -> None:
        """Load data from the JSON file"""
        if self.db_path.exists():
            try:
                with open(self.db_path, 'r') as f:
                    self.data = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load database file: {e}")
                self.data = {}
        else:
            self.data = {}
    
    def _save_data(self) -> None:
        """Save data to the JSON file"""
        try:
            # Create directory if it doesn't exist
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write data with backup
            temp_path = self.db_path.with_suffix('.tmp')
            with open(temp_path, 'w') as f:
                json.dump(self.data, f, indent=2)
            
            # Atomic rename
            temp_path.replace(self.db_path)
        except IOError as e:
            print(f"Error: Could not save database file: {e}")
    
    def create_collection(self, collection_name: str) -> None:
        """
        Create a new collection (table)
        
        Args:
            collection_name (str): Name of the collection to create
        """
        if collection_name not in self.data:
            self.data[collection_name] = []
            self._save_data()
    
    def insert(self, collection_name: str, document: Dict[str, Any]) -> str:
        """
        Insert a document into a collection
        
        Args:
            collection_name (str): Name of the collection
            document (Dict): Document to insert
            
        Returns:
            str: ID of the inserted document
        """
        self.create_collection(collection_name)
        
        # Add timestamp and ID
        doc_id = str(int(time.time() * 1000000))  # Microsecond timestamp as ID
        document['_id'] = doc_id
        document['_created'] = time.time()
        document['_modified'] = time.time()
        
        self.data[collection_name].append(document)
        self._save_data()
        
        return doc_id
    
    def find(self, collection_name: str, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Find documents in a collection
        
        Args:
            collection_name (str): Name of the collection
            query (Dict, optional): Query criteria
            
        Returns:
            List[Dict]: List of matching documents
        """
        if collection_name not in self.data:
            return []
        
        documents = self.data[collection_name]
        
        if query is None:
            return documents
        
        # Simple query matching
        results = []
        for doc in documents:
            match = True
            for key, value in query.items():
                if key not in doc or doc[key] != value:
                    match = False
                    break
            if match:
                results.append(doc)
        
        return results
    
    def find_one(self, collection_name: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Find one document in a collection
        
        Args:
            collection_name (str): Name of the collection
            query (Dict): Query criteria
            
        Returns:
            Dict or None: Matching document or None
        """
        results = self.find(collection_name, query)
        return results[0] if results else None
    
    def update(self, collection_name: str, query: Dict[str, Any], update_data: Dict[str, Any]) -> int:
        """
        Update documents in a collection
        
        Args:
            collection_name (str): Name of the collection
            query (Dict): Query criteria
            update_data (Dict): Data to update
            
        Returns:
            int: Number of documents updated
        """
        if collection_name not in self.data:
            return 0
        
        updated_count = 0
        for doc in self.data[collection_name]:
            match = True
            for key, value in query.items():
                if key not in doc or doc[key] != value:
                    match = False
                    break
            
            if match:
                doc.update(update_data)
                doc['_modified'] = time.time()
                updated_count += 1
        
        if updated_count > 0:
            self._save_data()
        
        return updated_count
    
    def delete(self, collection_name: str, query: Dict[str, Any]) -> int:
        """
        Delete documents from a collection
        
        Args:
            collection_name (str): Name of the collection
            query (Dict): Query criteria
            
        Returns:
            int: Number of documents deleted
        """
        if collection_name not in self.data:
            return 0
        
        original_count = len(self.data[collection_name])
        
        # Filter out matching documents
        self.data[collection_name] = [
            doc for doc in self.data[collection_name]
            if not all(doc.get(key) == value for key, value in query.items())
        ]
        
        deleted_count = original_count - len(self.data[collection_name])
        
        if deleted_count > 0:
            self._save_data()
        
        return deleted_count
    
    def list_collections(self) -> List[str]:
        """
        List all collections in the database
        
        Returns:
            List[str]: List of collection names
        """
        return list(self.data.keys())
    
    def drop_collection(self, collection_name: str) -> bool:
        """
        Drop a collection
        
        Args:
            collection_name (str): Name of the collection to drop
            
        Returns:
            bool: True if collection was dropped, False if it didn't exist
        """
        if collection_name in self.data:
            del self.data[collection_name]
            self._save_data()
            return True
        return False
    
    def count(self, collection_name: str, query: Optional[Dict[str, Any]] = None) -> int:
        """
        Count documents in a collection
        
        Args:
            collection_name (str): Name of the collection
            query (Dict, optional): Query criteria
            
        Returns:
            int: Number of matching documents
        """
        return len(self.find(collection_name, query))
    
    def backup(self, backup_path: str) -> bool:
        """
        Create a backup of the database
        
        Args:
            backup_path (str): Path for the backup file
            
        Returns:
            bool: True if backup was successful
        """
        try:
            import shutil
            shutil.copy2(self.db_path, backup_path)
            return True
        except Exception as e:
            print(f"Backup failed: {e}")
            return False


# Convenience functions for default database instance
_default_db = None

def get_db(db_path: str = "farndb.json") -> FarnDB:
    """Get the default database instance"""
    global _default_db
    if _default_db is None:
        _default_db = FarnDB(db_path)
    return _default_db

def insert(collection_name: str, document: Dict[str, Any]) -> str:
    """Insert into default database"""
    return get_db().insert(collection_name, document)

def find(collection_name: str, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Find in default database"""
    return get_db().find(collection_name, query)

def find_one(collection_name: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Find one in default database"""
    return get_db().find_one(collection_name, query)

def update(collection_name: str, query: Dict[str, Any], update_data: Dict[str, Any]) -> int:
    """Update in default database"""
    return get_db().update(collection_name, query, update_data)

def delete(collection_name: str, query: Dict[str, Any]) -> int:
    """Delete from default database"""
    return get_db().delete(collection_name, query)