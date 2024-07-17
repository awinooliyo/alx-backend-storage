## 0x01. NoSQL

## What is NoSQL?
NoSQL (Not Only SQL) databases are a category of database systems that do not adhere to the traditional relational database management system (RDBMS) structure based on tables and SQL for querying.

## Difference between SQL and NoSQL
SQL databases are relational databases that use structured query language (SQL) for defining and manipulating data. NoSQL databases are non-relational and offer flexible schema designs suitable for handling large amounts of unstructured or semi-structured data.

## ACID Properties
ACID (Atomicity, Consistency, Isolation, Durability) is a set of properties that guarantee reliable database transactions:
- **Atomicity**: Ensures that transactions are all or nothing.
- **Consistency**: Ensures that data remains in a consistent state before and after transactions.
- **Isolation**: Ensures that multiple transactions can occur simultaneously without affecting each other.
- **Durability**: Ensures that once a transaction is committed, it remains permanently stored even in case of system failure.

## Document Storage
NoSQL databases like MongoDB use a document-based model for storing data. Documents are JSON-like data structures that contain key-value pairs and can vary in structure within the same collection.

## Types of NoSQL Databases
1. **Document Stores**: Store data in flexible, JSON-like documents (e.g., MongoDB).
2. **Key-Value Stores**: Store data as key-value pairs (e.g., Redis).
3. **Column Family Stores**: Store data in columns rather than rows (e.g., Cassandra).
4. **Graph Databases**: Store data in graph structures (e.g., Neo4j).

## Benefits of NoSQL Databases
- **Scalability**: Easily scale horizontally to handle large volumes of data.
- **Flexibility**: Can handle various types of data, including semi-structured and unstructured data.
- **Performance**: Optimized for read and write operations in distributed environments.
- **Schema-less**: No need to define a schema upfront, allowing for agile development and flexibility in data models.

## Querying NoSQL Databases
### MongoDB Example (Python)
```python
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Access database
db = client['mydb']

# Access collection
collection = db['mycollection']

# Querying example
for doc in collection.find():
    print(doc)

# Close connection
client.close()
