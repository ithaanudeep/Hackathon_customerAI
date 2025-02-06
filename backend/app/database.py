import json
from couchbase.cluster import Cluster, ClusterOptions
from couchbase.auth import PasswordAuthenticator
from couchbase.collection import InsertOptions
from app.config import COUCHBASE_HOST, COUCHBASE_USER, COUCHBASE_PASSWORD, COUCHBASE_BUCKET

#def get_couchbase_connection():
auth = PasswordAuthenticator(COUCHBASE_USER, COUCHBASE_PASSWORD)
cluster = Cluster(f"couchbases://{COUCHBASE_HOST}", ClusterOptions(auth))
bucket = cluster.bucket(COUCHBASE_BUCKET)
    #return bucket.default_collection()

collection = bucket.default_collection()

def load_footwear_data():
    with open("footway_cs_dataset.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    for item in data:
        doc_id = f"footwear:{item['id']}"
        collection.upsert(doc_id, item)
    print("Footwear dataset loaded successfully!")