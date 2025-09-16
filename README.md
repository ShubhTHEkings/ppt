# ppt
🚀 Live Deployment  This project is live and running on an **Amazon AWS EC2** instance.

## 🗄️ FarnDB - Lightweight JSON Database

FarnDB is a simple, lightweight JSON-based database perfect for small to medium applications. It provides a MongoDB-like interface with file-based persistence.

### ✨ Features

- **Simple API**: Easy-to-use CRUD operations
- **JSON Storage**: Human-readable file format
- **Collections**: Organize data into collections (like tables)
- **Automatic IDs**: Auto-generated unique document IDs
- **Timestamps**: Automatic creation and modification timestamps
- **Atomic Writes**: Safe file operations with backup
- **CLI Tool**: Command-line interface for database operations
- **Lightweight**: No external dependencies

### 🚀 Quick Start

```python
import farndb

# Initialize database
db = farndb.FarnDB("myapp.json")

# Insert a document
user_id = db.insert("users", {
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30
})

# Find documents
users = db.find("users", {"age": 30})
user = db.find_one("users", {"name": "John Doe"})

# Update documents
db.update("users", {"name": "John Doe"}, {"age": 31})

# Delete documents
db.delete("users", {"name": "John Doe"})

# Count documents
count = db.count("users")
```

### 🖥️ CLI Usage

```bash
# List collections
python3 farndb_cli.py list

# Insert a document
python3 farndb_cli.py insert users '{"name": "Alice", "age": 25}'

# Find documents
python3 farndb_cli.py find users --query '{"age": 25}'

# Update documents
python3 farndb_cli.py update users '{"name": "Alice"}' '{"age": 26}'

# Count documents
python3 farndb_cli.py count users

# Backup database
python3 farndb_cli.py backup backup.json
```

### 📝 Examples

Run the example script to see FarnDB in action:

```bash
python3 example.py
```

This will create sample data and demonstrate all the basic operations.

### 🏗️ Use Cases

- **Prototyping**: Quick data storage for proof-of-concepts
- **Small Apps**: Perfect for applications with moderate data needs
- **Configuration**: Store application settings and configurations
- **Caching**: Simple data caching solution
- **Development**: Local development database
- **Embedded**: Lightweight database for embedded applications

### 📁 File Structure

```
farndb.py      # Main FarnDB library
farndb_cli.py  # Command-line interface  
example.py     # Usage examples
README.md      # Documentation
```
