from pymongo import MongoClient
from datetime import datetime
# Initialize MongoDB Client
client = MongoClient('mongodb://localhost:27017/')

# Create or select a database called 'mydatabase'
db = client['mydatabase']

# Create or select a collection called 'mycollection'
collection = db['mycollection']




# # # Execute the $push operation
# collection.update_one(
#     {"key": "my-secret-key"}, 
#     {"$push": {"conversation_history": {
#                 "Date": datetime.now(),
#                 "conversation": ['"role": "system", "content": "Hi, How can I assist you today?"']
#             }}
#     }
# )
# Insert a document into the collection
# insert_data = {
#     "key": "your-secret-key",
#     "conversation_history":{"Date":"","conversation":[]},
# }
# insert_result = collection.insert_one(insert_data)

# # Find the document with the corresponding key
# document = collection.find_one({"key": "your-secret-key"})

# # Check if 'conversation_history' is not an array and reset it
# if document and "conversation_history" in document and not isinstance(document["conversation_history"], list):
#     collection.update_one(
#         {"key": "your-secret-key"},
#         {"$set": {"conversation_history": []}}
#     )


# print(f"Inserted document with ID: {insert_result.inserted_id}")
# collection.update_one({"key": "your-secret-key"}, {"$push": {"conversation_history": {"Date":datetime.now(),
#                             "conversation":['"role": "system", "content": "Hi, How can I assist you today?"']}}})
# # Query the database to find documents where age is 30
# query = {"key": "your-secret-key"}
# query_result = collection.find(query)
# # # # # Print the query results
# for document in query_result:
#     for doc in document['conversation_history']:
#         print(doc)
    

# query = {"key": "your-secret-key"}
# query_result = collection.find(query)
# # # # # Print the query results
# for document in query_result:
#     print(document)
#     break

# print(collection.find({'key':'your-secret-key'}))

# Update a document
# update_query = {"key": "another-secret-key"}
# new_values = {"$set": {"city": "San Francisco"}}
# update_result = collection.update_one(update_query, new_values)
# print(f"Modified {update_result.modified_count} document(s)")

# # Delete a document
# delete_query = {"key": "your-secret-key"}
# delete_result = collection.delete_one(delete_query)
# print(f"Deleted {delete_result.deleted_count} document(s)")