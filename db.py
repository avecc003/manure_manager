# db.py
from dataclasses import dataclass
from google.cloud import firestore

# Initialize Firestore client
db = firestore.Client()

@dataclass
class Poll:
    id: str
    guild_id: str
    user_id: str
    title: str
    poll_id: str

def get_collection(collection_name):
    return db.collection(collection_name)

def get_document(collection_name, document_id):
    return db.collection(collection_name).document(document_id).get()

def set_document(collection_name, document_id, data={}):
    return db.collection(collection_name).document(document_id).set(data)

def update_document(collection_name, document_id, data):
    return db.collection(collection_name).document(document_id).update(data)

def delete_document(collection_name, document_id):
    return db.collection(collection_name).document(document_id).delete()

def get_by_guild_and_user(guild_id, user_id):
    db_polls = db.collection("polls").where("guild_id", "==", guild_id).where("user_id", "==", user_id).get()
    polls = []

    for poll_doc in db_polls:
        data = poll_doc.to_dict()
        polls.append(Poll(poll_doc.id,
                        data["guild_id"], 
                        data["user_id"], 
                        data["title"], 
                        data["poll_id"])) 
    return polls